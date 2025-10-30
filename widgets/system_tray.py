import gi
from fabric.system_tray.widgets import SystemTrayItem, get_tray_watcher
from fabric.utils import (
    bulk_connect,
)
from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.separator import Separator

from shared.widget_container import ButtonWidget
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon

gi.require_versions({"Gtk": "3.0", "GdkPixbuf": "2.0", "Gdk": "3.0"})


class SystemTrayMenu(Box):
    """A widget to display additional system tray items in a grid."""

    def __init__(self, config: dict, parent_widget=None, **kwargs):
        super().__init__(
            name="system-tray-menu",
            orientation="vertical",
            style_classes=["panel-menu"],
            **kwargs,
        )

        self.config = config
        self.parent_widget = parent_widget

        self.icon_size = config.get("icon_size", 16)

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

    def add_item(self, item: SystemTrayItem):
        self.grid.attach(item, self.column, self.row, 1, 1)
        self.column += 1
        if self.column >= self.max_columns:
            self.column = 0
            self.row += 1

        # Update parent widget visibility if parent is available
        if self.parent_widget:
            self.parent_widget.update_visibility()

    def on_item_removed(self, button: ButtonWidget):
        """Handle when an item is removed from the menu."""
        button.destroy()
        # Update parent widget visibility if parent is available
        if self.parent_widget:
            self.parent_widget.update_visibility()


class SystemTrayWidget(ButtonWidget):
    """A widget to display the system tray items."""

    def __init__(self, **kwargs):
        super().__init__(name="system_tray", **kwargs)

        # Create main tray box and toggle icon
        self.tray_box = Box(name="system-tray-box", orientation="horizontal", spacing=2)

        self.icon_size = self.config.get("icon_size", 16)

        self.toggle_icon = nerd_font_icon(
            icon=text_icons["chevron"]["down"],
            props={
                "style_classes": ["panel-font-icon"],
            },
        )

        # Set children directly in Box to avoid double styling
        self.container_box.children = (self.tray_box, Separator(), self.toggle_icon)

        # Create popup menu for hidden items
        self.popup_menu = SystemTrayMenu(config=self.config, parent_widget=self)

        self.popup = None

        self._watcher = get_tray_watcher()

        bulk_connect(
            self._watcher,
            {
                "item-added": self.on_item_added,
                "item-removed": self.on_item_removed,
            },
        )

        # # Load existing items
        for item_id in self._watcher.items:
            self.on_item_added(self._watcher, item_id)

        # Connect click handler
        self.connect("clicked", self.on_click)

        # Initial visibility check
        self.update_visibility()

    # show or hide the popup menu
    def on_click(self, *_):
        if self.popup is None:
            from shared.popover import Popover

            self.popup = Popover(
                content=self.popup_menu,
                point_to=self,
            )
            self.popup.connect(
                "popover-closed", lambda *_: self.remove_style_class("active")
            )

        visible = self.popup.get_visible()

        self.toggle_css_class("active", not visible)

        if visible:
            self.popup.hide()
            self.toggle_icon.set_label(text_icons["chevron"]["down"])

        else:
            self.popup.open()
            self.toggle_icon.set_label(text_icons["chevron"]["up"])
            self.add_style_class("active")

    def update_visibility(self):
        """Update widget visibility based on configuration and item count."""
        hide_when_empty = self.config.get("hide_when_empty", False)

        if not hide_when_empty:
            self.set_visible(True)
            return

        # Check if there are any visible items in the tray
        has_visible_items = len(self.tray_box.get_children()) > 0
        # Check if there are items in the popup menu
        has_hidden_items = len(self.popup_menu.grid.get_children()) > 0

        # Widget is visible if there are any items (visible or hidden)
        self.set_visible(has_visible_items or has_hidden_items)

    def on_item_removed(self, _, identifier: str):
        """Handle when an item is removed from the system tray."""
        # Update visibility after an item is removed
        self.update_visibility()

    def on_item_button_removed(self, button: ButtonWidget):
        """Handle when a button is removed from the main tray."""
        button.destroy()
        self.update_visibility()

    def on_item_added(self, _, item_identifier: str):
        item = self._watcher.items.get(item_identifier)
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
        button = SystemTrayItem(item=item, icon_size=self.icon_size)

        # Add to appropriate container
        if is_hidden:
            self.popup_menu.add_item(button)
        else:
            self.tray_box.pack_start(button, False, False, 0)

        # Update visibility after adding an item
        self.update_visibility()
