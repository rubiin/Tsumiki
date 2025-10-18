import gi
from fabric.notifications import (
    Notification,
    NotificationAction,
    NotificationCloseReason,
)
from fabric.utils import (
    bulk_connect,
    invoke_repeater,
    logger,
    remove_handler,
)
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.eventbox import EventBox
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget
from gi.repository import Gdk, GdkPixbuf, GLib

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircularImage
from utils.colors import Colors
from utils.icons import text_icons
from utils.widget_settings import BarConfig
from utils.widget_utils import get_icon, nerd_font_icon

gi.require_versions({"Gdk": "3.0", "GdkPixbuf": "2.0"})


class NotificationPopup(Window):
    """A widget to grab and display notifications."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        self._server = notification_service

        self.widget_config = widget_config

        self.config = widget_config.get("modules", {}).get("notification", {})

        self.ignored_apps = helpers.unique_list(self.config.get("ignored", []))

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

    def on_new_notification(self, fabric_notification, id):
        notification: Notification = fabric_notification.get_notification_from_id(id)

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

        if self.config.get("persist", True):
            self._server.cache_notification(
                self.widget_config, notification, self.config.get("max_count", 3)
            )

        if self.config.get("play_sound", False):
            helpers.play_sound(self.sound_file)


class NotificationWidget(EventBox):
    """A widget to display a notification."""

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

        self.progress_timeout = CircularProgressBar(
            name="notification-circular-progress-bar",
            size=27,
            min_value=0,
            max_value=1,
            radius_color=True,
        )

        self.notification_box = Box(
            spacing=8,
            name="notification",
            orientation="v",
        )

        if notification.urgency == 2:
            self.notification_box.add_style_class("critical")

        bulk_connect(
            self,
            {
                "button-press-event": self.on_button_press,
                "enter-notify-event": self.on_hover,
                "leave-notify-event": self.on_unhover,
            },
        )

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

        overlay = Overlay(
            child=self.progress_timeout,
            overlays=Button(
                v_align="center",
                h_align="center",
                style_classes=["close-button"],
                child=nerd_font_icon(
                    icon=text_icons["ui"]["window_close"],
                    props={
                        "style_classes": ["panel-font-icon", "close-icon"],
                    },
                ),
                on_clicked=self.on_close_button_clicked,
            ),
        )

        header_container.pack_end(
            overlay,
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=4,
            orientation="h",
            style_classes=["notification-body"],
            v_align="start",
            h_align="start",
        )

        # Use provided image if available
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
            # If the image is not available, use the symbolic icon
            logger.warning(f"{Colors.WARNING}[Notification] Image not available.")

        body_container.add(
            Label(
                markup=helpers.parse_markup(self._notification.body),
                v_align="start",
                h_align="start",
                style_classes=["body"],
                line_wrap="word-char",
                max_chars_width=38,
                lines=10,
            ),
        )

        actions_len = len(self._notification.actions)
        actions_count = min(actions_len, self.config.get("max_actions", 3))

        self.actions_container_grid = Grid(
            orientation="h",
            name="notification-action-box",
            h_expand=True,
            row_homogeneous=True,
            column_spacing=4,
        )

        self.actions_container_grid.attach_flow(
            [
                ActionButton(action, i, actions_count)
                for i, action in enumerate(notification.actions)
            ],
            3,  # Number of columns for actions
        )

        # Add the header, body, and actions to the notification box
        self.notification_box.children = (
            header_container,
            body_container,
            self.actions_container_grid,
        )

        # Add the notification box to the EventBox
        self.add(self.notification_box)

        # Destroy this widget once the notification is closed
        self._notification.connect(
            "closed",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.stop_timeout(),
                self.destroy(),
            ),
        )

        if self.config.get("auto_dismiss", False):
            self.start_timeout()

    def on_close_button_clicked(self, *_):
        self._notification.close("dismissed-by-user")
        self.stop_timeout()

    def start_timeout(self):
        self.stop_timeout()
        self._timeout_id = GLib.timeout_add(self.get_timeout(), self.close_notification)

    def stop_timeout(self):
        if self._timeout_id is not None:
            remove_handler(self._timeout_id)
            self._timeout_id = None

    def close_notification(self):
        self._notification.close("expired")
        self.stop_timeout()
        return False

    def on_button_press(self, _, event):
        if event.button != 1:
            self._notification.close("dismissed-by-user")
            self.stop_timeout()

    def get_timeout(self):
        return (
            self._notification.timeout
            if self._notification.timeout != -1
            else self.config.get("timeout", 3000)
        )

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
    """A widget to reveal a notification."""

    def __init__(self, config: dict, notification: Notification, **kwargs):
        self.notification_box = NotificationWidget(config, notification)
        self.timeout = config.get("timeout", 3000)
        self.notification_box.progress_timeout.max_value = self.timeout
        self._notification = notification

        super().__init__(
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

    def animate_popup_timeout(self):
        time = self.timeout

        def do_animate():
            nonlocal time
            self.notification_box.progress_timeout.value = time
            if not self.child_revealed:
                return False
            if time <= 0:
                return False
            time -= 10
            return True

        invoke_repeater(10, do_animate)

    def on_child_revealed(self, *_):
        if not self.get_child_revealed():
            self.destroy()
        else:
            if self.timeout > 0:
                self.animate_popup_timeout()

    def on_resolved(
        self,
        notification: Notification,
        reason: NotificationCloseReason,
    ):
        self.set_reveal_child(False)
        self.destroy()


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
