import os

import gi
from fabric.utils import (
    bulk_connect,
)
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from gi.repository import Gdk, GdkPixbuf, GLib, Gray, Gtk

from shared import ButtonWidget, Grid, HoverButton, Popover, Separator
from utils.icons import symbolic_icons

gi.require_version("Gray", "0.1")


def resolve_icon(item, icon_size: int = 16):
    pixmap = Gray.get_pixmap_for_pixmaps(item.get_icon_pixmaps(), icon_size)

    try:
        if pixmap is not None:
            return pixmap.as_pixbuf(icon_size, GdkPixbuf.InterpType.HYPER)
        else:
            icon_name = item.get_icon_name()
            icon_theme_path = item.get_icon_theme_path()

            # Use custom theme path if available
            if icon_theme_path:
                custom_theme = Gtk.IconTheme.new()
                custom_theme.prepend_search_path(icon_theme_path)
                try:
                    return custom_theme.load_icon(
                        icon_name,
                        icon_size,
                        Gtk.IconLookupFlags.FORCE_SIZE,
                    )
                except GLib.Error:
                    # Fallback to default theme if custom path fails
                    return Gtk.IconTheme.get_default().load_icon(
                        icon_name,
                        icon_size,
                        Gtk.IconLookupFlags.FORCE_SIZE,
                    )
            else:
                if os.path.exists(icon_name):  # for some apps, the icon_name is a path
                    return GdkPixbuf.Pixbuf.new_from_file_at_size(
                        icon_name, width=icon_size, height=icon_size
                    )
                else:
                    return Gtk.IconTheme.get_default().load_icon(
                        icon_name,
                        icon_size,
                        Gtk.IconLookupFlags.FORCE_SIZE,
                    )
    except GLib.Error:
        # Fallback to 'image-missing' icon
        return Gtk.IconTheme.get_default().load_icon(
            "image-missing",
            icon_size,
            Gtk.IconLookupFlags.FORCE_SIZE,
        )


class SystemTrayMenu(Box):
    """A widget to display additional system tray items in a grid."""

    def __init__(self, config, **kwargs):
        super().__init__(
            name="system-tray-menu",
            orientation="vertical",
            style_classes=["panel-menu"],
            **kwargs,
        )

        self.config = config

        # Create a grid for the items
        self.grid = Grid(
            row_spacing=8,
            column_spacing=12,
            margin_top=6,
            margin_bottom=6,
            margin_start=12,
            margin_end=12,
        )
        self.add(self.grid)

        self.row = 0
        self.column = 0
        self.max_columns = 3

    def add_item(self, item):
        button = self.do_bake_item_button(item)

        # Connect signals
        bulk_connect(
            item,
            {
                "removed",
                lambda *args: button.destroy(),
                "icon-changed",
                lambda icon_item: self.do_update_item_button(icon_item, button),
            },
        )

        button.show_all()
        self.grid.attach(button, self.column, self.row, 1, 1)
        self.column += 1
        if self.column >= self.max_columns:
            self.column = 0
            self.row += 1

    def do_bake_item_button(self, item: Gray.Item) -> HoverButton:
        button = HoverButton(
            style_classes="flat", toottip_text=item.get_property("title")
        )
        button.connect(
            "button-press-event",
            lambda button, event: self.on_button_click(button, item, event),
        )
        self.do_update_item_button(item, button)
        return button

    def do_update_item_button(self, item: Gray.Item, button: HoverButton):
        pixbuf = resolve_icon(
            item=item,
        )
        button.set_image(Image(pixbuf=pixbuf, pixel_size=self.config["icon_size"]))

    def on_button_click(self, button, item: Gray.Item, event):
        if event.button in (1, 3):
            menu = item.get_property("menu")
            if menu:
                menu.popup_at_widget(
                    button,
                    Gdk.Gravity.SOUTH,
                    Gdk.Gravity.NORTH,
                    event,
                )
            else:
                item.context_menu(event.x, event.y)


class SystemTrayWidget(ButtonWidget):
    """A widget to display the system tray items."""

    def __init__(self, **kwargs):
        super().__init__(name="system_tray", **kwargs)

        # Create main tray box and toggle icon
        self.tray_box = Box(name="system-tray-box", orientation="horizontal", spacing=2)
        self.toggle_icon = Image(
            icon_name=symbolic_icons["ui"]["arrow"]["down"],
            icon_size=self.config["icon_size"],
            style_classes=["panel-font-icon", "toggle-icon"],
        )

        # Set children directly in Box to avoid double styling
        self.box.children = (self.tray_box, Separator(), self.toggle_icon)

        # Create popup menu for hidden items
        self.popup_menu = SystemTrayMenu(config=self.config)

        self.popup = Popover(
            content=self.popup_menu,
            point_to=self,
        )

        # Initialize watcher
        self.watcher = Gray.Watcher()
        self.watcher.connect("item-added", self.on_item_added)

        # Load existing items
        for item_id in self.watcher.get_items():
            self.on_item_added(self.watcher, item_id)

        # Connect click handler
        self.connect("clicked", self.handle_click)

    # show or hide the popup menu
    def handle_click(self, *_):
        visible = self.popup.get_visible()
        if visible:
            self.popup.hide()
            self.toggle_icon.set_from_icon_name(
                symbolic_icons["ui"]["arrow"]["down"], self.config["icon_size"]
            )
            self.toggle_icon.get_style_context().remove_class("active")
        else:
            self.popup.open()
            self.toggle_icon.set_from_icon_name(
                symbolic_icons["ui"]["arrow"]["up"], self.config["icon_size"]
            )
            self.toggle_icon.get_style_context().add_class("active")

    def on_item_added(self, _, identifier: str):
        item = self.watcher.get_item_for_identifier(identifier)
        if not item:
            return

        # Get item title for matching
        title = item.get_property("title") or ""

        # Check if item should be ignored completely
        ignored_list = self.config.get("ignored", [])

        if any(x.lower() in title.lower() for x in ignored_list):
            return

        # Check if item should be hidden in popover
        hidden_list = self.config.get("hidden", [])
        is_hidden = any(x.lower() in title.lower() for x in hidden_list)

        # Add to appropriate container
        if is_hidden:
            self.popup_menu.add_item(item)
        else:
            button = HoverButton(
                style_classes="flat", tooltip_text=title, margin_start=2, margin_end=2
            )
            button.connect(
                "button-press-event",
                lambda button, event: self.popup_menu.on_button_click(
                    button, item, event
                ),
            )

            pixbuf = resolve_icon(
                item=item,
            )
            button.set_image(Image(pixbuf=pixbuf, pixel_size=self.config["icon_size"]))

            # Connect signals
            item.connect("removed", lambda *args: button.destroy())
            item.connect(
                "icon-changed",
                lambda icon_item: self.popup_menu.do_update_item_button(
                    icon_item, button
                ),
            )

            button.show_all()
            self.tray_box.pack_start(button, False, False, 0)
