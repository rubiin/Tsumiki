import gi
from fabric.notifications import Notification
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.separator import Separator
from gi.repository import GdkPixbuf, GLib, Gtk
from loguru import logger

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircularImage
from shared.list import ListBox
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.icons import text_icons
from utils.widget_utils import get_icon, nerd_font_icon

gi.require_versions({"Gtk": "3.0", "GdkPixbuf": "2.0"})


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
            on_clicked=self.remove_notification,
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
                h_expand=True,
                h_align="start",
                style="font-size: 13.5px;",
                line_wrap="word-char",
                chars_width=20,
                max_chars_width=45,
            ),
        )

        # Add the header, body, and actions to the notification box
        self.children = (
            header_container,
            body_container,
        )

    def remove_notification(self, *_):
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

        if config.get("notification", True):
            self.all_notifications: list[Notification] = (
                notification_service.get_deserialized()
            )

            self.notifications_listbox = ListBox(
                name="notification-list",
                orientation="v",
                h_align="center",
                spacing=8,
                h_expand=True,
                visible=len(self.all_notifications) > 0,
            )

            self.loaded_count = 0

            self.loading = False
            self.batch_size = 8  # how many to load per scroll

            self._load_next_batch()

            # Placeholder for when there are no notifications
            self.placeholder = Box(
                style_classes="placeholder",
                orientation="v",
                h_align="center",
                v_align="center",
                v_expand=True,
                h_expand=True,
                visible=len(self.all_notifications) == 0,  # visible if no notifications
                children=(
                    nerd_font_icon(
                        icon=text_icons["notifications"]["checked"],
                        props={
                            "style_classes": ["panel-font-icon", "placeholder-icon"],
                        },
                    ),
                    Label(
                        label="Your all caught up!", style_classes="placeholder-text"
                    ),
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
                children=(
                    Label(label="Do Not Disturb", name="dnd-text"),
                    self.dnd_switch,
                ),
            )

            self.clear_icon = nerd_font_icon(
                name="clear-icon",
                icon=text_icons["trash"]["empty"]
                if len(self.all_notifications) == 0
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

            self.clear_button.connect(
                "clicked",
                self._handle_clear_click,
            )

        notification_column_header.pack_end(
            self.clear_button,
            False,
            False,
            0,
        )
        self.scrolled_window = ScrolledWindow(
            v_expand=True,
            style_classes="notification-scrollable",
            v_scrollbar_policy="automatic",
            h_scrollbar_policy="never",
            child=Box(children=(self.placeholder, self.notifications_listbox)),
        )

        # Attach scroll listener
        if self.scrolled_window:
            vadj = self.scrolled_window.get_vadjustment()
            vadj.connect("value-changed", self.on_scroll)

        # Notification body column
        notification_column = Box(
            name="notification-column",
            orientation="v",
            children=(
                notification_column_header,
                self.scrolled_window,
            ),
        )
        self.add(notification_column)

        self.add(Separator())

        if config.get("calendar", True):
            date_column = Box(
                style_classes="date-column",
                orientation="v",
                children=(
                    DateTime(
                        "%H:%M"
                        if self.config.get("clock_format", "24h") == "24h"
                        else "%I:%M",
                        name="clock",
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

        if self.dnd_switch:
            self.dnd_switch.connect("notify::active", self.on_dnd_switch_toggled)

    def _handle_clear_click(self, *_):
        """Handle clear button click."""

        self.notifications_listbox.remove_all()

        notification_service.clear_all_notifications()
        self.clear_icon.set_label(text_icons["trash"]["empty"])

    def _load_next_batch(self):
        """Load the next batch of notifications into the listbox."""
        if self.loading or self.loaded_count >= len(self.all_notifications):
            return

        self.loading = True

        items_to_add = min(
            self.batch_size, len(self.all_notifications) - self.loaded_count
        )
        for i in range(self.loaded_count, self.loaded_count + items_to_add):
            notification_item = self._bake_notification(self.all_notifications[i])
            self.notifications_listbox.add(notification_item)

        self.loaded_count += items_to_add
        self.loading = False

    def on_scroll(self, adjustment):
        """Load more notifications when user scrolls near the bottom."""
        value = adjustment.get_value()
        upper = adjustment.get_upper()
        page_size = adjustment.get_page_size()

        if value + page_size >= upper - 50:
            self._load_next_batch()

    def on_dnd_switch_toggled(self, switch, state):
        notification_service.dont_disturb = switch.get_active()

    def on_dnd_switch(self, _, value, *args):
        self.dnd_switch.set_active(value)

    def on_clear_all_notifications(self, *_):
        """Handle clearing all notifications."""
        self.clear_icon.set_label(text_icons["trash"]["empty"])
        self.placeholder.set_visible(True)
        self.notifications_listbox.set_visible(False)

    def _bake_notification(self, notification):
        """Create a notification widget from a Notification object."""

        def on_child_destroyed(widget, row):
            row.destroy()

        item = DateMenuNotification(
            notification=notification,
            id=notification["id"],
        )

        row = Gtk.ListBoxRow(visible=True, name="notification-list-item", child=item)
        item.connect("destroy", on_child_destroyed, row)

        return row

    def on_notification_closed(self, _, id, reason):
        """Handle notification being closed."""

        for row in self.notifications_listbox.get_children():
            item = row.get_child()  # unwrap the ListBoxRow to get the actual widget
            if isinstance(item, DateMenuNotification) and item._id == id:
                if reason in {"dismissed-by-user", "dismissed-by-limit"}:
                    self._remove_notification(row)
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

        notification_item = self._bake_notification(
            fabric_notification,
        )

        self.notifications_listbox.insert(notification_item, 0)

        self.placeholder.set_visible(False)
        self.notifications_listbox.set_visible(True)


class DateTimeWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, **kwargs):
        super().__init__(name="date_time", **kwargs)

        notification_config = self.config["notification"]

        self.popup = None

        if notification_config.get("enabled", True):
            self.notification_indicator = nerd_font_icon(
                icon=text_icons["notifications"]["noisy"],
                name="notification-indicator",
                props={
                    "style_classes": ["panel-font-icon"],
                    "visible": notification_config.get("enabled", True),
                },
            )

            self.count_label = Label(
                name="notification-count",
                label=str(notification_service.count),
                v_align="start",
                visible=notification_config.get("enabled", True)
                and notification_config.get("count", True),
            )

            if (
                notification_config.get("hide_count_on_zero", False)
                and notification_service.count == 0
            ):
                self.count_label.set_visible(False)

            self.notification_indicator_box = Box(
                children=(self.notification_indicator, self.count_label)
            )

            bulk_connect(
                notification_service,
                {
                    "notification_count": self.on_notification_count,
                    "dnd": self.on_dnd_switch,
                },
            )

            self.container_box.add(self.notification_indicator_box)

        if self.config.get("hover_reveal", True):
            self.revealer = Revealer(
                child=DateTime(
                    self.config.get("format", "%m-%d %H:%M"), name="date-time"
                ),
                transition_duration=self.config.get("reveal_duration", 500),
                transition_type="slide_right",
            )
            self.container_box.add(self.revealer)
        else:
            self.container_box.add(
                DateTime(self.config.get("format", "%m-%d %H:%M"), name="date-time")
            )

        self.connect(
            "clicked",
            self.show_popover,
        )

    def on_notification_count(self, _, value, *args):
        if value > 0:
            self.count_label.set_text(str(value))
            self.count_label.set_visible(True)
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

    def show_popover(self, *_):
        """Show the popover."""
        if self.popup is None:
            from shared.popover import Popover

            self.popup = Popover(
                content=DateNotificationMenu(config=self.config),
                point_to=self,
            )
        self.popup.open()
