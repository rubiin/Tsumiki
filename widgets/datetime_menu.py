from fabric.notifications import Notification
from fabric.utils import GdkPixbuf, GLib, Gtk, bulk_connect, logger, math
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.separator import Separator

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared.buttons import HoverButton
from shared.circle_image import CircularImage
from shared.list import ListBox
from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.icons import get_text_icon
from utils.widget_utils import get_icon, nerd_font_icon


class DateMenuNotification(Box):
    """A widget to display a notification."""

    def __init__(
        self,
        id: int,
        notification: Notification,
        **kwargs,
    ):
        widget_name = kwargs.pop("name", "datemenu-notification-box")
        super().__init__(
            size=(constants.NOTIFICATION_WIDTH, -1),
            name=widget_name,
            h_expand=True,
            spacing=8,
            orientation="v",
            **kwargs,
        )

        self._notification = notification
        self._id = id

        header_container = Box(
            spacing=8, orientation="h", style_classes=["notification-header"]
        )

        title = self._notification.summary or notification.app_name
        header_container.children = (
            get_icon(notification.app_icon),
            Label(
                markup=helpers.parse_markup(str(title)),
                h_align="start",
                h_expand=True,
                line_wrap="word-char",
                style_classes=["summary"],
                name="date-menu-notification-summary",
            ),
        )
        close_button = Button(
            name="close-button",
            v_align="start",
            style_classes=["close-button"],
            child=nerd_font_icon(
                icon=get_text_icon("ui.window_close"),
                props={"style_classes": ["panel-font-icon", "close-icon"]},
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
            spacing=15,
            orientation="h",
            style_classes=["notification-body"],
            v_align="start",
            h_align="start",
        )

        notification_image_size = math.ceil(0.75 * constants.NOTIFICATION_IMAGE_SIZE)

        # Try to get cached pixbuf first, fall back to deserializing
        try:
            cached_pixbuf = notification_service.get_cached_pixbuf(
                self._id, notification_image_size
            )
            if cached_pixbuf:
                body_container.add(
                    CircularImage(
                        pixbuf=cached_pixbuf,
                        h_expand=True,
                        v_expand=True,
                        size=notification_image_size,
                    ),
                )
            elif image_pixbuf := self._notification.image_pixbuf:
                scaled = image_pixbuf.scale_simple(
                    notification_image_size,
                    notification_image_size,
                    GdkPixbuf.InterpType.BILINEAR,
                )
                if scaled:
                    # Cache for future use
                    notification_service.cache_pixbuf(
                        self._id, scaled, notification_image_size
                    )
                    body_container.add(
                        CircularImage(
                            pixbuf=scaled,
                            h_expand=True,
                            v_expand=True,
                            size=notification_image_size,
                        ),
                    )
                del image_pixbuf
        except GLib.GError:
            # If the image is not available, use the symbolic icon
            logger.warning(f"{Colors.WARNING}[Notification] Image not available.")

        body_container.add(
            Label(
                markup=helpers.parse_markup(self._notification.body or ""),
                v_align="start",
                h_align="start",
                name="date-menu-notification-body",
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
        config: dict,
        **kwargs,
    ):
        super().__init__(
            name="date-menu",
            orientation="h",
            **kwargs,
        )

        self.config = config
        self.pixel_size = 13
        self.notification_enabled = config.get("notification", True)

        if self.notification_enabled:
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
            self.grouped_entries: list[tuple[str, list[Notification]]] = []
            self._app_expand_state: dict[str, bool] = {}
            self._rebuild_grouped_entries()
            self._load_next_batch()

            # Placeholder for when there are no notifications
            self.placeholder = Box(
                style_classes=["placeholder"],
                orientation="v",
                h_align="center",
                v_align="center",
                v_expand=True,
                h_expand=True,
                visible=len(self.all_notifications) == 0,
                children=(
                    nerd_font_icon(
                        icon=get_text_icon("notifications.checked"),
                        props={
                            "style_classes": ["panel-font-icon", "placeholder-icon"],
                        },
                    ),
                    Label(
                        label="Your all caught up!",
                        style_classes=["placeholder-text"],
                    ),
                ),
            )

            self.dnd_switch = Gtk.Switch(
                name="notification-switch",
                active=False,
                valign=Gtk.Align.CENTER,
                visible=True,
            )

            notification_column_header = Box(
                style_classes=["header"],
                orientation="h",
                children=(
                    Label(label="Do Not Disturb", name="dnd-text"),
                    self.dnd_switch,
                ),
            )

            self.clear_icon = nerd_font_icon(
                name="clear-icon",
                icon=get_text_icon("trash.empty")
                if len(self.all_notifications) == 0
                else get_text_icon("trash.full"),
                props={"style_classes": ["panel-font-icon"]},
            )

            self.clear_button = HoverButton(
                name="clear-button",
                v_align="center",
                child=self.clear_icon,
            )
            self.clear_button.connect("clicked", self._handle_clear_click)

            notification_column_header.pack_end(
                self.clear_button,
                False,
                False,
                0,
            )

            self.scrolled_window = ScrolledWindow(
                v_expand=True,
                style_classes=["notification-scrollable"],
                v_scrollbar_policy="automatic",
                h_scrollbar_policy="never",
                child=Box(children=(self.placeholder, self.notifications_listbox)),
            )

            vadj = self.scrolled_window.get_vadjustment()
            vadj.connect("value-changed", self.on_scroll)

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
                style_classes=["date-column"],
                orientation="v",
                children=(
                    DateTime(
                        "%H:%M"
                        if self.config.get("clock_format", "24h") == "24h"
                        else "%I:%M",
                        name="clock",
                    ),
                    Box(
                        style_classes=["calendar"],
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

        if self.notification_enabled:
            bulk_connect(
                notification_service,
                {
                    "notification-added": self.on_new_notification,
                    "notification-closed": self.on_notification_closed,
                    "clear_all": self.on_clear_all_notifications,
                    "dnd": self.on_dnd_switch,
                },
            )

            self.dnd_switch.connect("notify::active", self.on_dnd_switch_toggled)

    def _handle_clear_click(self, *_):
        """Handle clear button click."""

        self.notifications_listbox.remove_all()
        self.all_notifications.clear()
        self.grouped_entries.clear()
        self.loaded_count = 0

        notification_service.clear_all_notifications()
        self.clear_icon.set_label(get_text_icon("trash.empty"))

    def _notification_id(self, notification: Notification) -> int | None:
        """Get notification ID for both serialized and deserialized objects."""
        if hasattr(notification, "__getitem__"):
            try:
                return int(notification["id"])
            except Exception:
                pass

        notif_id = getattr(notification, "id", None)
        if notif_id is None:
            return None

        try:
            return int(notif_id)
        except (TypeError, ValueError):
            return None

    def _notification_app_name(self, notification: Notification) -> str:
        """Resolve a stable app name used for grouping."""
        app_name = getattr(notification, "app_name", None)
        if not app_name and hasattr(notification, "__getitem__"):
            try:
                app_name = notification["app_name"]
            except Exception:
                app_name = None

        return str(app_name or "Unknown")

    def _rebuild_grouped_entries(self):
        """Build app-wise deck entries."""
        grouped: dict[str, list[Notification]] = {}

        for notification in self.all_notifications:
            app_name = self._notification_app_name(notification)
            if app_name not in grouped:
                grouped[app_name] = []
            grouped[app_name].append(notification)

        # Keep newest notification at top in each app deck.
        for app_name in grouped:
            grouped[app_name].sort(
                key=lambda n: self._notification_id(n) or 0,
                reverse=True,
            )

        # Order app decks by most recent notification first.
        app_order = sorted(
            grouped,
            key=lambda app: self._notification_id(grouped[app][0]) or 0,
            reverse=True,
        )

        entries: list[tuple[str, list[Notification]]] = []
        for app_name in app_order:
            entries.append((app_name, grouped[app_name]))
            self._app_expand_state.setdefault(app_name, False)

        removed_apps = set(self._app_expand_state) - set(app_order)
        for app_name in removed_apps:
            self._app_expand_state.pop(app_name, None)

        self.grouped_entries = entries

    def _reload_grouped_list(self):
        """Refresh the listbox from grouped entries."""
        self.notifications_listbox.remove_all()
        self.loaded_count = 0
        self._rebuild_grouped_entries()
        self._load_next_batch()

        has_notifications = len(self.all_notifications) > 0
        self.placeholder.set_visible(not has_notifications)
        self.notifications_listbox.set_visible(has_notifications)
        self.clear_icon.set_label(
            get_text_icon("trash.full")
            if has_notifications
            else get_text_icon("trash.empty")
        )

    def _bake_group_deck(
        self,
        app_name: str,
        notifications: list[Notification],
    ) -> Gtk.ListBoxRow:
        """Create one collapsible deck row for a single app group."""
        if len(notifications) == 1:
            single_notification = DateMenuNotification(
                notification=notifications[0],
                id=self._notification_id(notifications[0]) or 0,
            )
            return Gtk.ListBoxRow(
                visible=True,
                selectable=False,
                activatable=False,
                name="notification-group-row",
                child=single_notification,
            )

        expanded = self._app_expand_state.get(app_name, False)

        chevron_icon = nerd_font_icon(
            icon=get_text_icon("chevron.down" if expanded else "chevron.right"),
            props={"style_classes": ["panel-font-icon", "group-chevron"]},
        )

        title = Label(
            label=app_name,
            h_align="start",
            h_expand=True,
            visible=expanded,
            style_classes=["notification-group-title"],
        )

        header_content = Box(
            name="notification-group-header",
            style_classes=["notification-group-header"],
            orientation="h",
            h_expand=True,
            visible=expanded,
            children=(title,),
        )

        top_notification = DateMenuNotification(
            notification=notifications[0],
            id=self._notification_id(notifications[0]) or 0,
            style_classes=["notification-group-top"],
        )

        peek_layers = tuple(
            Box(
                name="notification-group-peek-layer",
                style_classes=["notification-group-peek-layer"],
                h_expand=True,
                orientation="h",
            )
            for _ in range(min(2, max(0, len(notifications) - 1)))
        )

        peek_box = Box(
            name="notification-group-peek",
            orientation="v",
            spacing=3,
            visible=(not expanded and len(notifications) > 1),
            children=peek_layers,
        )

        items_box = Box(
            name="notification-group-items",
            orientation="v",
            spacing=8,
            children=tuple(
                DateMenuNotification(
                    notification=notification,
                    id=self._notification_id(notification) or 0,
                )
                for notification in notifications[1:]
            ),
        )

        revealer = Revealer(
            child=items_box,
            reveal_child=expanded,
            transition_type="slide_down",
            transition_duration=220,
        )

        toggle_button = Button(
            name="notification-group-top-toggle",
            child=chevron_icon,
            h_align="end",
            v_align="start",
        )

        toggle_row = Box(
            name="notification-group-toggle-row",
            orientation="h",
            h_expand=True,
            children=(Box(h_expand=True), toggle_button),
        )

        deck = Box(
            name="notification-group-deck",
            orientation="v",
            spacing=0,
            children=(header_content, toggle_row, top_notification, peek_box, revealer),
        )

        if expanded:
            deck.add_style_class("group-expanded")

        def _toggle_group(*_):
            expanded = not self._app_expand_state.get(app_name, False)
            self._app_expand_state[app_name] = expanded
            revealer.set_reveal_child(expanded)
            peek_box.set_visible(not expanded and len(notifications) > 1)
            header_content.set_visible(expanded)
            if expanded:
                deck.add_style_class("group-expanded")
            else:
                deck.remove_style_class("group-expanded")
            chevron_icon.set_label(
                get_text_icon("chevron.down" if expanded else "chevron.right")
            )

        toggle_button.connect(
            "clicked",
            _toggle_group,
        )

        click_surface = EventBox()
        click_surface.add(deck)

        row = Gtk.ListBoxRow(
            visible=True,
            selectable=False,
            activatable=False,
            name="notification-group-row",
            child=click_surface,
        )

        click_surface.connect("button-press-event", _toggle_group)

        return row

    def _load_next_batch(self):
        """Load the next batch of notifications into the listbox."""
        if self.loading or self.loaded_count >= len(self.grouped_entries):
            return

        self.loading = True

        items_to_add = min(
            self.batch_size,
            len(self.grouped_entries) - self.loaded_count,
        )
        for i in range(self.loaded_count, self.loaded_count + items_to_add):
            app_name, notifications = self.grouped_entries[i]
            self.notifications_listbox.add(
                self._bake_group_deck(app_name, notifications)
            )

        self.loaded_count += items_to_add
        self.loading = False

    def on_scroll(self, adjustment: Gtk.Adjustment):
        """Load more notifications when user scrolls near the bottom."""
        value = adjustment.get_value()
        upper = adjustment.get_upper()
        page_size = adjustment.get_page_size()

        if value + page_size >= upper - 50:
            self._load_next_batch()

    def on_dnd_switch_toggled(self, switch: Gtk.Switch, state):
        notification_service.dont_disturb = switch.get_active()

    def on_dnd_switch(self, _, value, *args):
        self.dnd_switch.set_active(value)

    def on_clear_all_notifications(self, *_):
        """Handle clearing all notifications."""
        self.all_notifications.clear()
        self.grouped_entries.clear()
        self._app_expand_state.clear()
        self.loaded_count = 0
        self.clear_icon.set_label(get_text_icon("trash.empty"))
        self.placeholder.set_visible(True)
        self.notifications_listbox.set_visible(False)
        self.notifications_listbox.remove_all()

    def on_notification_closed(self, _, id, reason):
        """Handle notification being closed."""
        if reason not in {"dismissed-by-user", "dismissed-by-limit"}:
            return

        self.all_notifications = [
            n for n in self.all_notifications if self._notification_id(n) != id
        ]
        self._reload_grouped_list()

    def on_new_notification(self, fabric_notification, id):
        if notification_service.dont_disturb:
            return

        fabric_notification: Notification = (
            fabric_notification.get_notification_from_id(id)
        )

        self.all_notifications.insert(0, fabric_notification)
        self._reload_grouped_list()


class DateTimeWidget(ButtonWidget, PopoverMixin):
    """A widget to power off the system."""

    def __init__(self, **kwargs):
        super().__init__(name="date_time", **kwargs)

        notification_config = self.config.get("notification", {})

        if notification_config.get("enabled", True):
            self.notification_indicator = nerd_font_icon(
                icon=get_text_icon("notifications.noisy"),
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
                    self.config.get("date_format", "%m-%d %H:%M"), name="date-time"
                ),
                transition_duration=self.config.get("reveal_duration", 500),
                transition_type="slide_right",
            )
            self.container_box.add(self.revealer)
        else:
            self.container_box.add(
                DateTime(
                    self.config.get("date_format", "%m-%d %H:%M"), name="date-time"
                )
            )

        self.setup_popover(lambda: DateNotificationMenu(config=self.config))

    def on_notification_count(self, _, value, *args):
        if value > 0:
            self.count_label.set_text(str(value))
            self.count_label.set_visible(True)
        else:
            self.count_label.set_visible(False)

    def on_dnd_switch(self, _, value, *args):
        if value:
            self.notification_indicator.set_label(
                get_text_icon("notifications.silent"),
            )

        else:
            self.notification_indicator.set_label(
                get_text_icon("notifications.noisy"),
            )
