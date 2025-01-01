from fabric.notifications import Notification
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow

import utils.functions as helpers
from modules.notifications.notificationwidget import NotificationRevealer
from services import notification_service, notify_cache_service
from utils.monitors import HyprlandWithMonitors
from utils.widget_config import BarConfig


class NotificationPopup(WaylandWindow):
    """A widget to grab and display notifications."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        self._server = notification_service

        self.config = widget_config["notification"]

        self.hyprland_monitor = HyprlandWithMonitors()

        self.ignored_apps = helpers.unique_list(self.config["ignored"])

        self.notifications = Box(
            v_expand=True,
            h_expand=True,
            style="margin: 1px 0px 1px 1px;",
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

    def on_new_notification(self, fabric_notif, id):
        notification: Notification = fabric_notif.get_notification_from_id(id)

        # Check if the notification is in the "do not disturb" mode, hacky way
        if (
            notify_cache_service.dont_disturb
            or notification.app_name in self.ignored_apps
        ):
            return

        new_box = NotificationRevealer(notification)
        self.notifications.add(new_box)
        new_box.set_reveal_child(True)
        notify_cache_service.cache_notification(notification)
