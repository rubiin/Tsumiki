from fabric.notifications import (
    Notification,
    NotificationAction,
    Notifications,
)
from fabric.utils import (
    Gdk,
    GdkPixbuf,
    GLib,
    bulk_connect,
    invoke_repeater,
    logger,
    remove_handler,
)
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircularImage
from utils.colors import Colors
from utils.icons import get_text_icon
from utils.widget_settings import BarConfig
from utils.widget_utils import create_progress, get_icon, nerd_font_icon

# Swipe threshold for dismissing notifications (normalized: 0.0 to 1.0)
_SWIPE_DISMISS_THRESHOLD = 0.35


class NotificationPopup(Window):
    """A widget to grab and display notifications."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        self._server = notification_service

        self.widget_config = widget_config

        self.config = widget_config.get("modules", {}).get("notification", {})

        self.ignored_apps = helpers.unique_list(self.config.get("ignored", []))

        self.persist = self.config.get("persist", {})

        if self.config.get("play_sound", False):
            self.sound_file = f"{constants.ASSETS_DIR}/sounds/{self.config.get('sound_file', 'notification4')}.mp3"  # noqa: E501

        self.notifications = Box(
            v_expand=True,
            h_expand=True,
            style="margin: 1px 0 1px 1px;",
            orientation="v",
            spacing=5,
        )
        self._server.connect("notification-added", self.on_new_notification)

        super().__init__(
            anchor=self.config.get("anchor", "center"),
            layer="overlay",
            all_visible=True,
            visible=True,
            exclusive=False,
            title="tsumiki-notifications",
            child=self.notifications,
            **kwargs,
        )

    def on_new_notification(self, fabric_notification: Notifications, id):
        notification = fabric_notification.get_notification_from_id(id)

        # Check if the notification is in the "do not disturb" mode, hacky way
        if self._server.dont_disturb or notification.app_name in self.ignored_apps:
            return

        new_box = NotificationRevealer(self.config, notification)
        self.notifications.add(new_box)
        new_box.set_reveal_child(True)

        logger.info(
            f"{Colors.INFO}[Notification] New notification from "
            f"{Colors.OKGREEN}{notification.app_name}"
        )

        if self.persist.get("enabled", True):
            if notification.urgency == 0 and not self.persist.get("low", True):
                return
            if notification.urgency == 1 and not self.persist.get("normal", True):
                return
            if notification.urgency == 2 and not self.persist.get("critical", True):
                return

            self._server.cache_notification(
                self.widget_config, notification, self.persist.get("max_count", 100)
            )

        if self.config.get("play_sound", False):
            helpers.play_sound(self.sound_file)


class NotificationWidget(EventBox):
    """A widget to display a notification with swipe-to-dismiss support."""

    def __init__(
        self,
        config: dict,
        notification: Notification,
        **kwargs,
    ):
        super().__init__(
            size=(constants.NOTIFICATION_WIDTH, -1),
            name="notification-eventbox",
            **kwargs,
        )

        self.config = config
        self._notification = notification
        self._timeout_id = None
        self._time_remaining = 0

        # Swipe gesture state
        self._drag_start_x: float | None = None
        self._drag_start_y: float | None = None
        self._is_dragging = False
        self._swipe_offset = 0.0

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
        )

        self.progress_timeout = create_progress(
            name="notification-circular-progress-bar",
            line_width=3,
            min_value=0,
            max_value=1,
            radius_color=True,
            invert=True,
            start_angle=-90,
            size=27,
        )

        self.notification_box = Box(
            spacing=8,
            name="notification",
            orientation="v",
        )

        if notification.urgency == 2:
            self.notification_box.add_style_class("critical")

        self._wire_events()

        body_text = self._notification.body or ""
        max_collapsed_lines = self.config.get("max_lines", 4)
        max_expanded_lines = self.config.get("max_expanded_lines", 20)
        is_long_content = (
            body_text.count("\n") + 1 > max_collapsed_lines or len(body_text) > 150
        )

        header = self._build_header(
            notification, is_long_content, max_collapsed_lines, max_expanded_lines
        )
        body = self._build_body(
            notification, is_long_content, max_collapsed_lines, max_expanded_lines
        )
        self.actions_container_grid = self._build_actions(notification)

        self.notification_box.children = (header, body, self.actions_container_grid)
        self.add(self.notification_box)

        self._notification.connect("closed", lambda *_: self.stop_timeout())

    def _wire_events(self):
        """Connect all input event handlers."""
        bulk_connect(
            self,
            {
                "button-press-event": self.on_button_press,
                "button-release-event": self._on_button_release,
                "motion-notify-event": self._on_motion_notify,
                "enter-notify-event": self.on_hover,
                "leave-notify-event": self.on_unhover,
            },
        )

    def _build_header(
        self,
        notification: Notification,
        is_long_content: bool,
        max_collapsed_lines: int,
        max_expanded_lines: int,
    ) -> Box:
        """Build notification header: icon, summary, optional expand, close."""
        header_container = Box(
            spacing=8, orientation="h", style_classes=["notification-header"]
        )

        header_container.children = (
            get_icon(notification.app_icon),
            Label(
                markup=helpers.parse_markup(
                    self._notification.summary
                    if self._notification.summary
                    else notification.app_name,
                ),
                h_align="start",
                style_classes=["summary"],
                max_chars_width=30,
                line_wrap="word-char",
            ),
        )

        self.expand_button = None
        if is_long_content:
            self._is_expanded = False
            self.expand_button = Button(
                style_classes=["expand-button"],
                child=nerd_font_icon(
                    icon=get_text_icon("chevron.down"),
                    props={"style_classes": ["panel-font-icon", "expand-icon"]},
                ),
                on_clicked=lambda *_: self._toggle_expand(
                    max_collapsed_lines, max_expanded_lines
                ),
            )

        overlay = Overlay(
            child=self.progress_timeout,
            overlays=Button(
                v_align="center",
                h_align="center",
                style_classes=["close-button"],
                child=nerd_font_icon(
                    icon=get_text_icon("ui.window_close"),
                    props={"style_classes": ["panel-font-icon", "close-icon"]},
                ),
                on_clicked=self.on_close_button_clicked,
            ),
        )

        header_container.pack_end(overlay, False, False, 0)
        if self.expand_button:
            header_container.pack_end(self.expand_button, False, False, 0)

        return header_container

    def _build_body(
        self,
        notification: Notification,
        is_long_content: bool,
        max_collapsed_lines: int,
        max_expanded_lines: int,
    ) -> Box:
        """Build notification body: optional image and expandable text label."""
        body_text = self._notification.body or ""
        body_container = Box(
            spacing=4,
            orientation="h",
            style_classes=["notification-body"],
            v_align="start",
            h_align="start",
        )

        try:
            if image_pixbuf := self._notification.image_pixbuf:
                body_container.add(
                    CircularImage(
                        pixbuf=image_pixbuf.scale_simple(
                            constants.NOTIFICATION_IMAGE_SIZE,
                            constants.NOTIFICATION_IMAGE_SIZE,
                            GdkPixbuf.InterpType.BILINEAR,
                        ),
                        h_expand=True,
                        v_expand=True,
                        size=constants.NOTIFICATION_IMAGE_SIZE,
                    ),
                )
                del image_pixbuf
        except GLib.GError:
            logger.exception(f"{Colors.WARNING}[Notification] Image not available.")

        if is_long_content:
            self.body_label = Label(
                markup=helpers.parse_markup(body_text),
                v_align="start",
                h_align="start",
                style_classes=["body"],
                line_wrap="word-char",
                max_chars_width=38,
            )
            self.body_label.set_lines(max_collapsed_lines)
            self.body_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
            body_container.add(self.body_label)
        else:
            body_container.add(
                Label(
                    markup=helpers.parse_markup(body_text),
                    v_align="start",
                    h_align="start",
                    style_classes=["body"],
                    line_wrap="word-char",
                    max_chars_width=38,
                ),
            )

        return body_container

    def _build_actions(self, notification: Notification) -> Grid:
        """Build the actions grid from notification actions."""
        actions_count = min(
            len(self._notification.actions), self.config.get("max_actions", 3)
        )
        grid = Grid(
            orientation="h",
            name="notification-action-box",
            h_expand=True,
            row_homogeneous=True,
            column_spacing=4,
        )
        grid.attach_flow(
            [
                ActionButton(action, i, actions_count)
                for i, action in enumerate(notification.actions)
            ],
            3,
        )
        return grid

    def _toggle_expand(self, collapsed_lines: int, expanded_lines: int):
        """Toggle between collapsed and expanded body text."""
        self._is_expanded = not self._is_expanded
        if self._is_expanded:
            self.body_label.set_lines(expanded_lines)
            self.expand_button.get_child().set_label(get_text_icon("chevron.up"))
        else:
            self.body_label.set_lines(collapsed_lines)
            self.expand_button.get_child().set_label(get_text_icon("chevron.down"))

    def on_close_button_clicked(self, *_):
        self._notification.close("dismissed-by-user")
        self.stop_timeout()

    def start_timeout(self):
        self.stop_timeout()
        self._time_remaining = self.get_timeout()
        self.progress_timeout.max_value = self._time_remaining
        self._timeout_id = invoke_repeater(10, self._timer_tick)

    def _timer_tick(self) -> bool:
        """Single unified tick: update progress bar and close when expired."""
        self.progress_timeout.value = self._time_remaining

        if self._time_remaining <= 0:
            self.close_notification()
            return False
        self._time_remaining -= 10
        return True

    def stop_timeout(self):
        if self._timeout_id is not None:
            remove_handler(self._timeout_id)
            self._timeout_id = None

    def close_notification(self):
        self._notification.close("expired")
        self.stop_timeout()
        return False

    def on_button_press(self, widget, event):
        """Handle button press - start drag tracking for swipe gestures."""
        if event.button == 1:
            # Left click: start tracking for potential swipe
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self._is_dragging = False
            self._swipe_offset = 0.0
            return True
        else:
            # Right/middle click: dismiss immediately
            self._notification.close("dismissed-by-user")
            self.stop_timeout()
            return True

    def _render_swipe_progress(self, dx: float, widget_width: int):
        """Update swipe offset state and apply visual translation + fade."""
        self._swipe_offset = dx / widget_width
        self.notification_box.set_margin_start(int(dx) if dx > 0 else 0)
        self.notification_box.set_margin_end(int(-dx) if dx < 0 else 0)
        opacity = max(0.3, 1.0 - abs(self._swipe_offset))
        self.notification_box.set_opacity(opacity)

    def _on_motion_notify(self, widget, event):
        """Handle mouse motion for swipe gesture."""
        if self._drag_start_x is None:
            return False

        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y

        if abs(dx) > 10 and abs(dx) > abs(dy):
            self._is_dragging = True
            self.pause_timeout()
            alloc = widget.get_allocation()
            if alloc.width > 0:
                self._render_swipe_progress(dx, alloc.width)

        return True

    def _on_button_release(self, widget, event):
        """Handle button release - complete swipe gesture if threshold met."""
        if self._drag_start_x is None:
            return False

        if self._is_dragging:
            if abs(self._swipe_offset) >= _SWIPE_DISMISS_THRESHOLD:
                self._notification.close("dismissed-by-user")
            else:
                self._reset_swipe_position()

        # Reset drag state
        self._drag_start_x = None
        self._drag_start_y = None
        self._is_dragging = False
        self._swipe_offset = 0.0

        return True

    def _reset_swipe_position(self):
        """Reset the notification position after an incomplete swipe."""
        self.notification_box.set_margin_start(0)
        self.notification_box.set_margin_end(0)
        self.notification_box.set_opacity(1.0)
        self.resume_timeout()

    def get_timeout(self):
        if self.config.get("respect_expire", True) and self._notification.timeout != -1:
            return self._notification.timeout

        if isinstance(self.config.get("timeout"), dict):
            urgency = self._notification.urgency
            if urgency == 0:
                return self.config.get("timeout", {}).get("low", 3000)
            elif urgency == 1:
                return self.config.get("timeout", {}).get("normal", 8000)
            elif urgency == 2:
                return self.config.get("timeout", {}).get("critical", 15000)

    def pause_timeout(self):
        self.stop_timeout()

    def resume_timeout(self):
        self.start_timeout()

    def on_hover(self, *_):
        self.pause_timeout()
        self.set_pointer_cursor(self, "hand2")

        if self.config.get("dismiss_on_hover", False):
            self.close_notification()

    def on_unhover(self, *_):
        self.resume_timeout()
        self.set_pointer_cursor(self, "arrow")

    @staticmethod
    def set_pointer_cursor(widget: Widget, cursor_name: str):
        window = widget.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(widget.get_display(), cursor_name)
            window.set_cursor(cursor)


class NotificationRevealer(Revealer):
    """A widget to reveal a notification with open/close animations."""

    def __init__(self, config: dict, notification: Notification, **kwargs):
        self.notification_box = NotificationWidget(config, notification)
        self.timeout = self.notification_box.get_timeout()
        self._notification = notification
        self._is_closing = False

        super().__init__(
            name="notification-revealer",
            child=Box(
                style="margin: 12px;",
                children=[self.notification_box],
            ),
            transition_duration=config.get("transition_duration", 200),
            transition_type=config.get("transition_type", "slide-up"),
            **kwargs,
        )

        self.connect("notify::child-revealed", self.on_child_revealed)

        self._notification.connect("closed", self.on_resolved)

    def on_child_revealed(self, *_):
        if not self.get_child_revealed():
            self.destroy()
        else:
            if self.timeout > 0:
                self.notification_box.start_timeout()

    def on_resolved(
        self,
        *_,
    ):
        if self._is_closing:
            return
        self._is_closing = True
        # Trigger close animation - destroy happens in on_child_revealed
        self.set_reveal_child(False)


class ActionButton(HoverButton):
    """A button widget to represent a notification action."""

    def __init__(
        self,
        action: NotificationAction,
        action_number: int,
        total_actions: int,
        **kwargs,
    ):
        super().__init__(
            label=action.label,
            h_expand=True,
            on_clicked=self.on_click,
            style_classes=["notification-action"],
            **kwargs,
        )

        self.action = action

        if action_number == 0:
            self.add_style_class("start-action")
        elif action_number == total_actions - 1:
            self.add_style_class("end-action")
        else:
            self.add_style_class("middle-action")

    def on_click(self, *_):
        self.action.invoke()
        self.action.parent.close("dismissed-by-user")
