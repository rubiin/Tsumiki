import time
from typing import List

from fabric.notifications import Notification
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GdkPixbuf, GLib, Gtk
from loguru import logger

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircleImage
from shared.list import ListBox
from shared.popover import Popover
from shared.separator import Separator
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.functions import uptime
from utils.icons import text_icons
from utils.widget_utils import get_icon, nerd_font_icon, util_fabricator


class DateMenuNotification(Box):
    """A widget to display a notification."""

    def __init__(
        self,
        id: int,
        notification: Notification,
        **kwargs,
    ):
        super().__init__(
            size=(constants.NOTIFICATION_WIDTH, -1),
            name="datemenu-notification-box",
            h_expand=True,
            spacing=8,
            orientation="v",
            **kwargs,
        )

        self._notification = notification
        self._id = id

        header_container = Box(
            spacing=8, orientation="h", style_classes="notification-header"
        )

        header_container.children = (
            get_icon(notification.app_icon),
            Label(
                markup=helpers.parse_markup(
                    str(
                        self._notification.summary
                        if self._notification.summary
                        else notification.app_name,
                    )
                ),
                h_align="start",
                h_expand=True,
                line_wrap="word-char",
                style_classes="summary",
                style="font-size: 13.5px;",
            ),
        )
        close_button = Button(
            style_classes="close-button",
            child=nerd_font_icon(
                icon=text_icons["ui"]["window_close"],
                props={
                    "style_classes": ["panel-font-icon", "close-icon"],
                },
            ),
            on_clicked=self.clear_notification,
        )

        header_container.pack_end(
            close_button,
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=15, orientation="h", style_classes="notification-body"
        )

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
                style="font-size: 13.5px;",
                line_wrap="word-char",
                chars_width=20,
                max_chars_width=40,
            ),
        )

        # Add the header, body, and actions to the notification box
        self.children = (
            header_container,
            body_container,
        )

        # Handle notification signals
        self._notification.connect("closed", self.on_notification_closed)

    def on_notification_closed(self, notification, reason):
        """Handle notification being closed."""
        if reason in ["dismissed-by-user", "dismissed-by-limit"]:
            self.destroy()

    def clear_notification(self, *_):
        notification_service.remove_notification(self._id)
        self.destroy()


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(
        self,
        config,
        **kwargs,
    ):
        super().__init__(
            name="date-menu",
            orientation="h",
            **kwargs,
        )

        self.config = config

        self.pixel_size = 13

        self.clock_label = Label(
            label=time.strftime("%H:%M")
            if self.config["clock_format"] == "24h"
            else time.strftime("%I:%M"),
            style_classes="clock",
        )

        notifications: List[Notification] = notification_service.get_deserialized()

        self.notifications_listbox = ListBox(
            name="notification-list",
            orientation="v",
            h_align="center",
            spacing=8,
            h_expand=True,
            visible=len(notifications) > 0,
        )

        for value in notifications:
            notification_item = Gtk.ListBoxRow(
                visible=True, name="notification-list-item"
            )
            notification_item.add(
                DateMenuNotification(notification=value, id=value["id"])
            )
            self.notifications_listbox.add(notification_item)

        self.uptime = Label(style_classes="uptime", visible=config["uptime"])

        # Placeholder for when there are no notifications
        self.placeholder = Box(
            style_classes="placeholder",
            orientation="v",
            h_align="center",
            v_align="center",
            v_expand=True,
            h_expand=True,
            visible=len(notifications) == 0,  # visible if no notifications
            children=(
                nerd_font_icon(
                    icon="󱇥",
                    props={
                        "style_classes": ["panel-font-icon", "placeholder-icon"],
                    },
                ),
                Label(label="Your all caught up!", style_classes="placeholder-text"),
            ),
        )

        # Header for the notification column
        self.dnd_switch = Gtk.Switch(
            name="notification-switch",
            active=False,
            valign=Gtk.Align.CENTER,
            visible=True,
        )

        notification_column_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label(label="Do Not Disturb", name="dnd-text"), self.dnd_switch),
        )

        self.clear_icon = nerd_font_icon(
            name="clear-icon",
            icon=text_icons["trash"]["empty"]
            if len(notifications) == 0
            else text_icons["trash"]["full"],
            props={
                "style_classes": ["panel-font-icon"],
            },
        )

        self.clear_button = HoverButton(
            name="clear-button",
            v_align="center",
            child=Box(children=(self.clear_icon,)),
        )

        def handle_clear_click(*_):
            """Handle clear button click."""

            self.notifications_listbox.remove_all()

            notification_service.clear_all_notifications()
            self.clear_icon.set_label(text_icons["trash"]["empty"])

        self.clear_button.connect(
            "clicked",
            handle_clear_click,
        )

        notification_column_header.pack_end(
            self.clear_button,
            False,
            False,
            0,
        )

        if config["notification"]:
            # Notification body column
            notification_column = Box(
                name="notification-column",
                orientation="v",
                children=(
                    notification_column_header,
                    ScrolledWindow(
                        v_expand=True,
                        style_classes="notification-scrollable",
                        v_scrollbar_policy="automatic",
                        h_scrollbar_policy="never",
                        child=Box(
                            children=(self.placeholder, self.notifications_listbox)
                        ),
                    ),
                ),
            )
            self.add(notification_column)

        self.add(Separator())

        if config["calendar"]:
            date_column = Box(
                style_classes="date-column",
                orientation="v",
                children=(
                    Box(
                        style_classes="clock-box",
                        orientation="v",
                        children=(self.clock_label, self.uptime),
                    ),
                    Box(
                        style_classes="calendar",
                        v_expand=True,
                        children=(
                            Gtk.Calendar(
                                visible=True,
                                hexpand=True,
                                halign=Gtk.Align.CENTER,
                            )
                        ),
                    ),
                ),
            )

            self.add(date_column)

        bulk_connect(
            notification_service,
            {
                "notification-added": self.on_new_notification,
                "notification-closed": self.on_notification_closed,
                "clear_all": self.on_clear_all_notifications,
                "dnd": self.on_dnd_switch,
            },
        )

        self.dnd_switch.connect("notify::active", self.on_dnd_switch)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def on_dnd_switch(self, _, value, *args):
        self.dnd_switch.set_active(value)

    def on_clear_all_notifications(self, *_):
        """Handle clearing all notifications."""
        self.clear_icon.set_label(text_icons["trash"]["empty"])
        self.placeholder.set_visible(True)
        self.notifications_listbox.set_visible(False)

    def on_notification_closed(self, _, id, reason):
        """Handle notification being closed."""

        for child in self.notifications_listbox.get_children():
            is_target = (
                isinstance(child, DateMenuNotification)
                and child._notification["id"] == id
            )
            if is_target:
                if reason in ["dismissed-by-user", "dismissed-by-limit"]:
                    self._remove_notification(child)
                break

    def _remove_notification(self, widget):
        self.notifications_listbox.remove(widget)
        widget.destroy()  # Ensure the object is freed

        return False

    def on_new_notification(self, fabric_notification, id):
        if notification_service.dont_disturb:
            return

        fabric_notification: Notification = (
            fabric_notification.get_notification_from_id(id)
        )

        self.clear_icon.set_label(
            text_icons["trash"]["full"],
        )

        notification_item = Gtk.ListBoxRow(visible=True)
        notification_item.add(
            DateMenuNotification(
                notification=fabric_notification,
                id=id,
            )
        )

        self.notifications_listbox.add(
            notification_item,
        )

        self.placeholder.set_visible(False)
        self.notifications_listbox.set_visible(True)

    def update_ui(self, fabricator, value):
        self.clock_label.set_text(
            time.strftime("%H:%M")
            if self.config["clock_format"] == "24h"
            else time.strftime("%I:%M"),
        )
        self.uptime.set_text(f"uptime: {uptime()}")
        return True


class DateTimeWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, **kwargs):
        super().__init__(name="date_time", **kwargs)

        notification_config = self.config["notification"]

        popup = Popover(
            content=DateNotificationMenu(config=self.config),
            point_to=self,
        )

        self.notification_indicator = nerd_font_icon(
            icon=text_icons["notifications"]["noisy"],
            name="notification-indicator",
            props={
                "style_classes": ["panel-font-icon"],
                "visible": notification_config["enabled"],
            },
        )

        self.count_label = Label(
            name="notification-count",
            label=str(notification_service.count),
            v_align="start",
            visible=notification_config["enabled"] and notification_config["count"],
        )

        if (
            notification_config["hide_count_on_zero"]
            and notification_service.count == 0
        ):
            self.count_label.set_visible(False)

        self.notification_indicator_box = Box(
            children=(self.notification_indicator, self.count_label)
        )

        self.connect(
            "clicked",
            popup.open,
        )

        self.children = Box(
            spacing=10,
            v_align="center",
            children=(
                self.notification_indicator_box,
                DateTime(self.config["format"], name="date-time"),
            ),
        )

        bulk_connect(
            notification_service,
            {
                "notification_count": self.on_notification_count,
                "dnd": self.on_dnd_switch,
            },
        )

    def on_notification_count(self, _, value, *args):
        if value > 0:
            self.count_label.set_text(str(value))
            self.count_label.set_visible(str(value))
        else:
            self.count_label.set_visible(False)

    def on_dnd_switch(self, _, value, *args):
        if value:
            self.notification_indicator.set_label(
                text_icons["notifications"]["silent"],
            )

        else:
            self.notification_indicator.set_label(
                text_icons["notifications"]["noisy"],
            )
