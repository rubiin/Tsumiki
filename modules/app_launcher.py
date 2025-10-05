import operator
from collections.abc import Iterator
from contextlib import suppress

from fabric.utils import DesktopApp, idle_add, logger, remove_handler
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.entry import Entry
from fabric.widgets.grid import Grid
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import Gdk, GLib, Gtk

from shared.popup import PopupWindow
from utils.app import AppUtils
from utils.widget_settings import BarConfig


class LauncherConfig:
    """Configuration validator and defaults for AppLauncher."""

    # Only essential constants
    DEFAULT_WIDTH = 280
    DEFAULT_HEIGHT = 320
    DEFAULT_ICON_SIZE = 30
    DEFAULT_GRID_COLUMNS = 3
    DEFAULT_ANCHOR = "center"
    DEFAULT_LAYOUT = "list"

    def __init__(self, config: BarConfig):
        self.raw_config = config.get("modules", {}).get("app_launcher", {})
        self._validate_and_set_defaults()

    def _validate_and_set_defaults(self):
        """Validate configuration and set defaults."""
        self.width = max(200, self.raw_config.get("width", self.DEFAULT_WIDTH))
        self.height = max(200, self.raw_config.get("height", self.DEFAULT_HEIGHT))

        icon_size = self.raw_config.get("icon_size", self.DEFAULT_ICON_SIZE)
        self.icon_size = max(16, min(128, icon_size))

        layout = self.raw_config.get("layout", self.DEFAULT_LAYOUT)
        self.layout_mode = layout if layout in ["list", "grid"] else self.DEFAULT_LAYOUT

        grid_cols = self.raw_config.get("grid_columns", self.DEFAULT_GRID_COLUMNS)
        self.grid_columns = max(1, min(10, grid_cols))

        self.anchor = self.raw_config.get("anchor", self.DEFAULT_ANCHOR)
        self.show_tooltips = bool(self.raw_config.get("tooltip", False))


class AppWidgetFactory:
    """Factory for creating application widgets in different layouts."""

    @staticmethod
    def create_widget(
        app: DesktopApp, layout_mode: str, icon_size: int, config: LauncherConfig
    ) -> Button:
        """Create an application widget based on layout mode."""
        if layout_mode == "grid":
            child_widget = AppWidgetFactory._create_grid_layout(app, icon_size, config)
        else:
            child_widget = AppWidgetFactory._create_list_layout(app, icon_size, config)

        return Button(
            style_classes=["launcher-button"],
            child=child_widget,
            tooltip_text=(app.description if config.show_tooltips else None),
        )

    @staticmethod
    def _create_grid_layout(
        app: DesktopApp, icon_size: int, config: LauncherConfig
    ) -> Box:
        """Create vertical layout for grid mode."""
        return Box(
            orientation="v",
            spacing=4,
            children=[
                Image(
                    pixbuf=app.get_icon_pixbuf(icon_size),
                    h_align="center",
                    name="icon",
                ),
                Label(
                    label=app.display_name or "Unknown",
                    v_align="center",
                    h_align="center",
                    max_width_chars=10,
                    ellipsization="end",
                ),
            ],
        )

    @staticmethod
    def _create_list_layout(
        app: DesktopApp, icon_size: int, config: LauncherConfig
    ) -> Box:
        """Create horizontal layout for list mode."""
        return Box(
            orientation="h",
            spacing=12,
            style_classes=["launcher-list-item"],
            children=[
                Image(
                    pixbuf=app.get_icon_pixbuf(icon_size),
                    h_align="start",
                    name="icon",
                ),
                Label(
                    label=app.display_name or "Unknown",
                    v_align="center",
                    h_align="center",
                ),
            ],
        )


class HandlerManager:
    """Context manager for handling GTK handlers safely."""

    def __init__(self, launcher):
        self.launcher = launcher
        self.old_handler = None

    def __enter__(self):
        # Remove old handler if exists and is valid
        if self.launcher._arranger_handler and self.launcher._arranger_handler > 0:
            # Check if the source still exists before removing
            main_context = GLib.MainContext.default()
            handler_id = self.launcher._arranger_handler
            if main_context.find_source_by_id(handler_id):
                try:
                    remove_handler(handler_id)
                    self.old_handler = handler_id
                except (GLib.Error, Exception):
                    # Handler removal failed, just continue silently
                    pass
        self.launcher._arranger_handler = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup is automatic, nothing to do
        pass

    def set_new_handler(self, handler_id):
        """Set the new handler ID."""
        self.launcher._arranger_handler = handler_id


class AppLauncher(PopupWindow):
    """Launcher widget for launching applications and commands."""

    def __init__(self, config: dict, **kwargs):
        # Initialize configuration with validation
        self.config = LauncherConfig(config)

        # Initialize remaining instance variables
        self._arranger_handler: int = 0
        self.app_util = AppUtils()
        self._all_apps = self.app_util.all_applications
        self._grid_position = 0  # Track current position in grid

        # Create widgets - viewport depends on layout mode
        if self.config.layout_mode == "grid":
            self.viewport = Grid(
                column_homogeneous=True, row_homogeneous=True, row_spacing=20
            )
        else:  # list mode
            self.viewport = Box(spacing=2, orientation="v")
        self.search_entry = Entry(
            name="launcher-prompt",
            placeholder="Search Applications...",
            h_expand=True,
            notify_text=lambda entry, *_: self.arrange_viewport(entry.get_text()),
        )

        # Add magnifying glass icon to the left (primary position)
        self.search_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, "system-search"
        )

        # Right icon (cross/clear)
        self.search_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, "edit-clear"
        )

        # Connect handler for icon clicks
        self.search_entry.connect("icon-press", self.on_icon_press)

        self.scrolled_window = ScrolledWindow(
            min_content_size=(self.config.width, self.config.height),
            max_content_size=(self.config.width, self.config.height),
            child=self.viewport,
        )

        # Enable kinetic scrolling
        with suppress(AttributeError):
            self.scrolled_window.set_kinetic_scrolling(True)

        # Create the main content
        launcher_content = Box(
            name="launcher-contents",
            spacing=2,
            orientation="v",
            size_request=(self.config.width, self.config.height),
            children=[
                # Header with search
                self.search_entry,
                # Apps list
                self.scrolled_window,
            ],
        )

        # Choose transition based on anchor
        transition = (
            "slide-up" if self.config.anchor.startswith("bottom") else "slide-down"
        )

        super().__init__(
            name="launcher",
            title="launcher",
            anchor=self.config.anchor,
            transition_type=transition,
            transition_duration=300,
            enable_inhibitor=True,
            child=launcher_content,
            **kwargs,
        )

        # Set up key handling
        self.connect("key-press-event", self.on_key_press)

    def on_icon_press(self, entry, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.search_entry.set_text("")

    def close_launcher(self):
        """Close the launcher."""
        self.popup_visible = False
        self.reveal_child.revealer.set_reveal_child(self.popup_visible)
        self.search_entry.set_text("")

    def on_key_press(self, _, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close_launcher()

    def _clear_viewport_safely(self):
        """Clear viewport widgets with proper error handling."""
        if self.config.layout_mode == "grid":
            try:
                children = [child for child in self.viewport]
                for child in children:
                    self.viewport.remove(child)
            except (AttributeError, TypeError) as e:
                # Log error and recreate grid as fallback
                logger.warning(f"Warning: Grid clear failed ({e}), recreating viewport")
                try:
                    self.viewport = Grid(
                        column_homogeneous=True,
                        row_homogeneous=True,
                    )
                    self.scrolled_window.set_child(self.viewport)
                except Exception as fallback_error:
                    logger.exception(
                        f"Error: Failed to recreate grid: {fallback_error}"
                    )
        else:
            # For list layout, simple clear
            self.viewport.children = []

    def arrange_viewport(self, query: str = ""):
        """Arrange viewport with filtered applications."""
        with HandlerManager(self) as handler_mgr:
            # Clear viewport safely
            self._clear_viewport_safely()
            self._grid_position = 0

            # Simple and efficient app filtering
            query_lower = query.casefold()
            filtered_apps_iter = iter(
                [
                    app
                    for app in self._all_apps
                    if query_lower
                    in (
                        (app.display_name or "")
                        + " "
                        + (app.name or "")
                        + " "
                        + (app.generic_name or "")
                    ).casefold()
                ]
            )
            should_resize = operator.length_hint(filtered_apps_iter) == len(
                self._all_apps
            )

            # Start lazy loading process
            handler_id = idle_add(
                lambda *args: self.add_next_application(*args)
                or (self.resize_viewport() if should_resize else False),
                filtered_apps_iter,
                pin=True,
            )
            handler_mgr.set_new_handler(handler_id)

        return False

    def add_next_application(self, apps_iter: Iterator[DesktopApp]):
        """Add the next application widget to the viewport."""
        if not (app := next(apps_iter, None)):
            return False

        app_widget = AppWidgetFactory.create_widget(
            app, self.config.layout_mode, self.config.icon_size, self.config
        )
        app_widget.on_clicked = lambda *_: (app.launch(), self.close_launcher())

        if self.config.layout_mode == "grid":
            row = self._grid_position // self.config.grid_columns
            col = self._grid_position % self.config.grid_columns
            self.viewport.attach(app_widget, col, row, 1, 1)
            self._grid_position += 1
        else:  # list mode
            self.viewport.add(app_widget)

        return True

    def resize_viewport(self):
        """Resize viewport to fit content."""
        try:
            allocation_width = self.viewport.get_allocation().width
            if allocation_width > 0:
                # Clear max_content_width constraint to avoid conflicts
                self.scrolled_window.set_max_content_width(-1)
                self.scrolled_window.set_min_content_width(allocation_width)
        except (AttributeError, TypeError):
            # Ignore resize errors
            pass
        return False

    def toggle(self):
        """Toggle launcher visibility."""
        if self.popup_visible:
            self.close_launcher()
        else:
            # Refresh apps list
            self._all_apps = self.app_util.all_applications
            self.search_entry.set_text("")

            # Focus search entry for filtering
            self.search_entry.grab_focus_without_selecting()

            # Show the popup using PopupWindow's method
            self.toggle_popup()

    def launch(self, command: str):
        self.search_entry.set_text(command)
