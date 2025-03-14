import gi
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from gi.repository import Gdk, GdkPixbuf, GLib, Gray, Gtk

from shared.pop_over import PopOverWindow
from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig

gi.require_version("Gray", "0.1")


class SystemTrayMenu(Box):
    """A widget to display the system tray items."""

    def __init__(self, config, **kwargs) -> None:
        super().__init__(name="system-tray", **kwargs)

        self.config = config

        self.grid = Gtk.Grid(
            visible=True,
            row_spacing=20,
            column_spacing=20,
            column_homogeneous=True,
            row_homogeneous=True,
        )

        self.watcher = Gray.Watcher()
        self.watcher.connect("item-added", self.on_item_added)

        self.add(self.grid)

        # Initialize row and column trackers
        self.row = 0
        self.column = 0
        self.max_columns = 4  # 4 columns

    def add_to_grid(self, item):
        self.grid.attach(item, self.column, self.row, 1, 1)

        # Increment the column and row trackers
        self.column += 1
        if self.column >= self.max_columns:
            self.column = 0
            self.row += 1

    def on_item_added(self, _, identifier: str):
        item = self.watcher.get_item_for_identifier(identifier)

        if (
            self.config["ignored"]
            and item.get_property("title") in self.config["ignored"]
        ):
            return

        item_button = self.do_bake_item_button(item)
        item.connect("removed", lambda *args: item_button.destroy())
        item.connect(
            "icon-changed",
            lambda icon_item: self.do_update_item_button(icon_item, item_button),
        )
        item_button.show_all()
        self.add_to_grid(item_button)

    def do_bake_item_button(self, item: Gray.Item) -> Button:
        button = Button()
        # context menu handler
        button.connect(
            "button-press-event",
            lambda button, event: self.on_button_click(button, item, event),
        )
        button.set_tooltip_text(item.get_property("title"))

        self.do_update_item_button(item, button)

        return button

    def do_update_item_button(self, item: Gray.Item, item_button: Button):
        pixmap = Gray.get_pixmap_for_pixmaps(item.get_icon_pixmaps(), 24)

        try:
            pixbuf: GdkPixbuf.Pixbuf = (
                pixmap.as_pixbuf(self.config["icon_size"], GdkPixbuf.InterpType.HYPER)
                if pixmap is not None
                else Gtk.IconTheme()
                .get_default()
                .load_icon(
                    item.get_icon_name(),
                    self.config["icon_size"],
                    Gtk.IconLookupFlags.FORCE_SIZE,
                )
            )

        except GLib.GError:
            pixbuf = (
                Gtk.IconTheme()
                .get_default()
                .load_icon(
                    "image-missing",
                    self.config["icon_size"],
                    Gtk.IconLookupFlags.FORCE_SIZE,
                )
            )

        item_button.set_image(Image(pixbuf=pixbuf, pixel_size=self.config["icon_size"]))

    def on_button_click(self, button, item: Gray.Item, event):
        match event.button:
            case 1 | 3:
                menu = item.get_property("menu")
                menu.set_name("system-tray-menu")
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

    def __init__(self, widget_config: BarConfig, bar, **kwargs) -> None:
        super().__init__(
            image=Image(icon_name="pack-less-symbolic", icon_size=16), **kwargs
        )

        self.config = widget_config["system_tray"]
        self.set_tooltip_text("System Tray")

        popup = PopOverWindow(
            name="popup",
            parent=bar,
            child=(SystemTrayMenu(config=self.config)),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
