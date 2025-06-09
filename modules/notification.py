from fabric.notifications import (
    Notification,
    NotificationAction,
    NotificationCloseReason,
)
from fabric.utils import bulk_connect, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Gdk, GdkPixbuf, GLib
from loguru import logger

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircleImage
from shared.grid import Grid
from utils.colors import Colors
from utils.icons import symbolic_icons
from utils.monitors import HyprlandWithMonitors
from utils.widget_settings import BarConfig
from utils.widget_utils import get_icon


class NotificationPopup(Window):
    """A widget to grab and display notifications."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        self._server = notification_service

        self.widget_config = widget_config

        self.config = widget_config["modules"]["notification"]

        self.hyprland_monitor = HyprlandWithMonitors()

        self.ignored_apps = helpers.unique_list(self.config["ignored"])

        self.notifications = Box(
            v_expand=True,
            h_expand=True,
            style="margin: 1px 0 1px 1px;",
            orientation="v",
            spacing=5,
        )
        self._server.connect("notification-added", self.on_new_notification)

        super().__init__(
            anchor=self.config["anchor"],
            layer="overlay",
            all_visible=True,
            monitor=HyprlandWithMonitors().get_current_gdk_monitor_id(),
            visible=True,
            exclusive=False,
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
        self._server.cache_notification(
            self.widget_config, notification, self.config["max_count"]
        )

        if self.config["play_sound"]:
            helpers.play_sound(
                get_relative_path(f"../assets/sounds/{self.config['sound_file']}.mp3")
            )


class NotificationWidget(EventBox):
    """A widget to display a notification."""

    def __init__(
        self,
        config,
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
            spacing=8, orientation="h", style_classes="notification-header"
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
                style_classes="summary",
                max_chars_width=16,
                ellipsization="end",
            ),
        )

        close_button = Button(
            style_classes="close-button",
            image=Image(
                name="close-icon",
                icon_name=helpers.check_icon_exists(
                    symbolic_icons["ui"]["close"],
                    symbolic_icons["ui"]["window_close"],
                ),
                icon_size=16,
            ),
            on_clicked=self.on_close_button_clicked,
        )

        header_container.pack_end(
            close_button,
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=4, orientation="h", style_classes="notification-body"
        )

        # Use provided image if available
        try:
            if image_pixbuf := self._notification.image_pixbuf:
                self._notification.image_pixbuf = None  # Release the full-size pixbuf
                body_container.add(
                    CircleImage(
                        pixbuf=image_pixbuf.scale_simple(
                            constants.NOTIFICATION_IMAGE_SIZE,
                            constants.NOTIFICATION_IMAGE_SIZE,
                            GdkPixbuf.InterpType.BILINEAR,
                        ),
                        size=constants.NOTIFICATION_IMAGE_SIZE,
                        h_expand=True,
                        v_expand=True,
                    ),
                )
        except GLib.GError:
            # If the image is not available, use the symbolic icon
            logger.warning(f"{Colors.WARNING}[Notification] Image not available.")

        body_container.add(
            Label(
                markup=helpers.parse_markup(self._notification.body),
                v_align="start",
                h_expand=True,
                h_align="start",
                style_classes="body",
                max_chars_width=34,
                ellipsization="end",
            ),
        )

        actions_len = len(self._notification.actions)
        actions_count = min(actions_len, self.config["max_actions"])

        self.actions_container_grid = Grid(
            orientation="h",
            name="notification-action-box",
            h_expand=True,
            column_homogeneous=True,
            row_homogeneous=True,
            column_spacing=4,
        )

        for i, action in enumerate(notification.actions):
            action_button = ActionButton(action, i, actions_count)
            self.actions_container_grid.attach(action_button, i, 0, 1, 1)

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

        if self.config["auto_dismiss"]:
            self.start_timeout()

    def on_close_button_clicked(self, *_):
        self._notification.close("dismissed-by-user")
        self.stop_timeout()

    def start_timeout(self):
        self.stop_timeout()
        self._timeout_id = GLib.timeout_add(self.get_timeout(), self.close_notification)

    def stop_timeout(self):
        if self._timeout_id is not None:
            GLib.source_remove(self._timeout_id)
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
            else self.config["timeout"]
        )

    def pause_timeout(self):
        self.stop_timeout()

    def resume_timeout(self):
        self.start_timeout()

    def on_hover(self, *_):
        self.pause_timeout()
        self.set_pointer_cursor(self, "hand2")

        if self.config["dismiss_on_hover"]:
            self.close_notification()

    def on_unhover(self, *_):
        self.resume_timeout()
        self.set_pointer_cursor(self, "arrow")

    @staticmethod
    def set_pointer_cursor(widget, cursor_name):
        window = widget.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(widget.get_display(), cursor_name)
            window.set_cursor(cursor)


class NotificationRevealer(Revealer):
    """A widget to reveal a notification."""

    def __init__(self, config, notification: Notification, **kwargs):
        self.notification_box = NotificationWidget(config, notification)
        self._notification = notification

        super().__init__(
            child=Box(
                style="margin: 12px;",
                children=[self.notification_box],
            ),
            transition_duration=config["transition_duration"],
            transition_type=config["transition_type"],
            **kwargs,
        )

        self.connect("notify::child-revealed", self.on_child_revealed)
        self._notification.connect("closed", self.on_resolved)

    def on_child_revealed(self, *_):
        if not self.get_child_revealed():
            self.destroy()

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
            on_clicked=self.on_clicked,
            style_classes="notification-action",
            **kwargs,
        )

        self.action = action

        if action_number == 0:
            self.add_style_class("start-action")
        elif action_number == total_actions - 1:
            self.add_style_class("end-action")
        else:
            self.add_style_class("middle-action")

    def on_clicked(self, *_):
        self.action.invoke()
        self.action.parent.close("dismissed-by-user")
