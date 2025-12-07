"""
Settings GUI for Tsumiki
"""

from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.entry import Entry
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.stack import Stack
from fabric.widgets.window import Window
from gi.repository import Gtk

from shared.buttons import HoverButton
from utils.config import configuration, theme_config, widget_config
from utils.constants import ASSETS_DIR
from utils.functions import write_json_file
from utils.types import (
    Anchor,
    Bar_Location,
    Data_Unit,
    Dock_Behavior,
    Layer,
    Orientation,
    Reveal_Animations,
    Temperature_Unit,
    Widget_Mode,
    get_literal_values,
)


class SettingsGUI(Window):
    """Settings window for Tsumiki configuration."""

    _instance = None
    _visible = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        super().__init__(
            title="Tsumiki Settings",
            name="settings-window",
            size=(700, 550),
            **kwargs,
        )

        self.set_resizable(False)
        self.config = dict(widget_config)
        self.theme = dict(theme_config)
        self.modified = False

        # Main layout
        root_box = Box(orientation="v", spacing=10, style="margin: 10px;")
        self.add(root_box)

        # Content with sidebar
        main_content = Box(
            orientation="h",
            spacing=6,
            v_expand=True,
            h_expand=True,
        )
        root_box.add(main_content)

        # Tab stack
        self.tab_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=250,
            v_expand=True,
            h_expand=True,
        )

        # Create tabs
        self._setup_tabs()

        # Tab switcher (sidebar)
        tab_switcher = Gtk.StackSwitcher()
        tab_switcher.set_stack(self.tab_stack)
        tab_switcher.set_orientation(Gtk.Orientation.VERTICAL)
        tab_switcher.set_name("settings-sidebar")
        main_content.add(tab_switcher)
        main_content.add(self.tab_stack)

        # Button box
        button_box = Box(orientation="h", spacing=10, h_align="end")

        reset_btn = HoverButton(
            label="Reset",
            name="settings-reset-btn",
            on_clicked=self._on_reset,
        )
        button_box.add(reset_btn)

        close_btn = HoverButton(
            label="Close",
            name="settings-close-btn",
            on_clicked=self._on_close,
        )
        button_box.add(close_btn)

        self.save_btn = HoverButton(
            label="Apply & Save",
            name="settings-save-btn",
            on_clicked=self._on_save,
        )
        self.save_btn.set_sensitive(False)
        button_box.add(self.save_btn)

        root_box.add(button_box)

        # Connect close event
        self.connect("delete-event", self._on_delete)

    def _setup_tabs(self):
        """Setup all tabs in the stack."""
        self.tab_stack.add_titled(self._create_general_tab(), "general", "󰒓 General")
        self.tab_stack.add_titled(self._create_modules_tab(), "modules", "󰒍 Modules")
        self.tab_stack.add_titled(self._create_widgets_tab(), "widgets", "󰕰 Widgets")
        self.tab_stack.add_titled(self._create_theme_tab(), "theme", "󰸌 Theme")
        self.tab_stack.add_titled(self._create_about_tab(), "about", "󰋽 About")

    def _refresh_tabs(self):
        """Refresh all tab contents with current config."""
        current_tab = self.tab_stack.get_visible_child_name()

        for child in self.tab_stack.get_children():
            self.tab_stack.remove(child)

        self._setup_tabs()
        self.tab_stack.set_visible_child_name(current_tab)
        self.show_all()

    def _create_scrolled_container(self) -> tuple[ScrolledWindow, Box]:
        """Create a scrolled window with a vbox inside."""
        vbox = Box(orientation="v", spacing=15, style="margin: 15px;")

        scrolled = ScrolledWindow(
            h_scrollbar_policy="never",
            v_scrollbar_policy="automatic",
            h_expand=True,
            v_expand=True,
            propagate_width=False,
            propagate_height=False,
        )
        scrolled.add(vbox)
        return scrolled, vbox

    def _create_section_header(self, text: str) -> Label:
        """Create a section header label."""
        return Label(
            markup=f"<b>{text}</b>",
            h_align="start",
            name="settings-section-header",
        )

    def _create_label(self, text: str) -> Label:
        """Create a standard label for settings."""
        return Label(
            label=text.replace("_", " ").title(),
            h_align="start",
            v_align="center",
            h_expand=True,
        )

    def _create_grid(self, margin_bottom: int = 0) -> Gtk.Grid:
        """Create a standard grid for settings."""
        return Gtk.Grid(
            column_spacing=20,
            row_spacing=8,
            margin_start=10,
            margin_top=5,
            margin_bottom=margin_bottom,
            column_homogeneous=False,
        )

    def _create_expander(self, label: str) -> Gtk.Expander:
        """Create a GTK expander for nested settings."""
        expander = Gtk.Expander(label=label, expanded=False, name="settings-expander")
        return expander

    def _create_switch(self, active: bool, on_change=None) -> Gtk.Switch:
        """Create a GTK switch."""
        switch = Gtk.Switch(
            active=active, halign=Gtk.Align.START, valign=Gtk.Align.CENTER
        )
        if on_change:
            switch.connect("notify::active", on_change)
        return switch

    def _create_combo(
        self, options: list, active: str, on_change=None
    ) -> Gtk.ComboBoxText:
        """Create a combo box."""
        combo = Gtk.ComboBoxText(halign=Gtk.Align.START, valign=Gtk.Align.CENTER)
        for opt in options:
            combo.append_text(opt)
        try:
            combo.set_active(options.index(active))
        except ValueError:
            combo.set_active(0)
        if on_change:
            combo.connect("changed", on_change)
        return combo

    def _create_spinbutton(
        self, value: int, min_val: int, max_val: int, on_change=None
    ) -> Gtk.SpinButton:
        """Create a spin button."""
        adj = Gtk.Adjustment(
            value=value,
            lower=min_val,
            upper=max_val,
            step_increment=1,
            page_increment=10,
        )
        spin = Gtk.SpinButton(adjustment=adj, climb_rate=1, digits=0)
        spin.set_value(value)
        if on_change:
            spin.connect("value-changed", on_change)
        return spin

    def _create_general_tab(self):
        """Create the general settings tab."""
        scrolled, vbox = self._create_scrolled_container()
        general = self.config.get("general", {})

        vbox.add(self._create_section_header("General Settings"))

        grid = self._create_grid()
        vbox.add(grid)

        for row, (key, value) in enumerate(general.items()):
            grid.attach(self._create_label(key), 0, row, 1, 1)

            if isinstance(value, bool):
                widget = self._create_switch(
                    value,
                    lambda sw, _, k=key: self._update_config(
                        "general", k, sw.get_active()
                    ),
                )
            else:
                widget = Label(label=str(value), h_align="start", h_expand=True)

            grid.attach(widget, 1, row, 1, 1)

        return scrolled

    def _create_nested_section(
        self, container: Box, nested_name: str, nested_config: dict, path: str
    ):
        """Create an expandable section for nested config."""
        expander = self._create_expander(nested_name.replace("_", " ").title())

        inner_box = Box(orientation="v", spacing=4, style="margin-left: 20px;")
        grid = self._create_grid()
        inner_box.add(grid)

        row = 0
        for key, value in nested_config.items():
            if isinstance(value, dict):
                # Handle deeper nesting recursively
                self._create_nested_section(inner_box, key, value, f"{path}.{key}")
            elif isinstance(value, list):
                continue  # Skip lists for now
            else:
                grid.attach(self._create_label(key), 0, row, 1, 1)
                nested_path = f"{path}.{nested_name}"
                widget = self._create_control(nested_path, key, value)
                grid.attach(widget, 1, row, 1, 1)
                row += 1

        expander.add(inner_box)
        container.add(expander)

    def _create_config_section(
        self, vbox: Box, section_name: str, config_items: dict, path_prefix: str
    ):
        """Create a configuration section with grid of controls."""
        vbox.add(self._create_section_header(section_name.replace("_", " ").title()))

        section_box = Box(orientation="v", spacing=4)
        grid = self._create_grid(margin_bottom=15)
        section_box.add(grid)

        row = 0
        for key, value in config_items.items():
            if isinstance(value, dict):
                # Create expandable section for nested config
                path = f"{path_prefix}.{section_name}"
                self._create_nested_section(section_box, key, value, path)
            elif isinstance(value, list):
                continue  # Skip lists for now
            else:
                grid.attach(self._create_label(key), 0, row, 1, 1)
                path = f"{path_prefix}.{section_name}"
                widget = self._create_control(path, key, value)
                grid.attach(widget, 1, row, 1, 1)
                row += 1

        vbox.add(section_box)

    def _create_modules_tab(self):
        """Create the modules settings tab."""
        scrolled, vbox = self._create_scrolled_container()
        modules = self.config.get("modules", {})

        for module_name, module_config in sorted(modules.items()):
            if isinstance(module_config, dict):
                self._create_config_section(vbox, module_name, module_config, "modules")

        return scrolled

    def _create_widgets_tab(self):
        """Create the widgets settings tab."""
        scrolled, vbox = self._create_scrolled_container()
        widgets = self.config.get("widgets", {})

        for widget_name, widget_cfg in sorted(widgets.items()):
            if isinstance(widget_cfg, dict):
                self._create_config_section(vbox, widget_name, widget_cfg, "widgets")

        return scrolled

    def _create_control(self, path: str, key: str, value) -> Gtk.Widget:
        """Create appropriate control for a value."""
        if isinstance(value, bool):
            return self._create_switch(
                value,
                lambda sw, _, p=path, k=key: self._update_config(p, k, sw.get_active()),
            )
        elif isinstance(value, int):
            return self._create_spinbutton(
                value,
                0,
                100,
                lambda sp, p=path, k=key: self._update_config(
                    p, k, int(sp.get_value())
                ),
            )
        elif isinstance(value, str):
            enum_options = self._get_enum_options(key)
            if enum_options:
                return self._create_combo(
                    enum_options,
                    value,
                    lambda cb, p=path, k=key: self._update_config(
                        p, k, cb.get_active_text()
                    ),
                )
            entry = Entry(text=value, h_expand=False)
            entry.set_width_chars(15)
            entry.connect(
                "changed",
                lambda e, p=path, k=key: self._update_config(p, k, e.get_text()),
            )
            return entry
        return Label(label=str(value), h_align="start")

    def _get_enum_options(self, key: str) -> list | None:
        """Get enum options for known keys."""
        enums = {
            "layer": get_literal_values(Layer),
            "anchor": get_literal_values(Anchor),
            "location": get_literal_values(Bar_Location),
            "orientation": get_literal_values(Orientation),
            "transition_type": get_literal_values(Reveal_Animations),
            "mode": get_literal_values(Widget_Mode),
            "behavior": get_literal_values(Dock_Behavior),
            "temperature_unit": get_literal_values(Temperature_Unit),
            "unit": get_literal_values(Data_Unit),
        }
        return enums.get(key)

    def _create_theme_tab(self):
        """Create the theme settings tab."""
        scrolled, vbox = self._create_scrolled_container()

        # Main theme sections
        self._create_theme_section(
            vbox, "matugen", self.theme.get("matugen", {}), "theme"
        )
        self._create_theme_section(
            vbox, "font", self.theme.get("font", {}), "theme"
        )
        self._create_theme_section(
            vbox, "bar", self.theme.get("bar", {}), "theme"
        )
        self._create_theme_section(
            vbox, "modules", self.theme.get("modules", {}), "theme"
        )

        return scrolled

    def _create_theme_section(
        self, container: Box, section_name: str, section_config: dict, path: str
    ):
        """Create a top-level section for theme config (no expander)."""
        # Add section header
        container.add(self._create_section_header(section_name.title()))

        section_box = Box(orientation="v", spacing=4)
        grid = self._create_grid(margin_bottom=15)
        section_box.add(grid)

        row = 0
        for key, value in section_config.items():
            if isinstance(value, dict):
                # for individual modules
                if section_name == "modules":
                    self._create_theme_module_section(
                        section_box, key, value, f"{path}.{section_name}"
                    )
                else:
                    # Handle deeper nesting with expanders for other sections
                    self._create_theme_nested_section(
                        section_box, key, value, f"{path}.{section_name}"
                    )
            elif isinstance(value, list):
                continue  # Skip lists for now
            else:
                grid.attach(self._create_label(key), 0, row, 1, 1)
                nested_path = f"{path}.{section_name}"
                widget = self._create_theme_control(nested_path, key, value)
                grid.attach(widget, 1, row, 1, 1)
                row += 1

        container.add(section_box)

    def _create_theme_module_section(
        self, container: Box, module_name: str, module_config: dict, path: str
    ):
        """Create a module section within the modules section (no expander)."""
        # Add module header
        container.add(
            self._create_section_header(module_name.replace("_", " ").title())
        )

        module_box = Box(orientation="v", spacing=4, style="margin-left: 20px;")
        grid = self._create_grid(margin_bottom=10)
        module_box.add(grid)

        row = 0
        for key, value in module_config.items():
            if isinstance(value, dict):
                # Handle deeper nesting with expanders (like shadow, border)
                self._create_theme_nested_section(
                    module_box, key, value, f"{path}.{module_name}"
                )
            elif isinstance(value, list):
                continue  # Skip lists for now
            else:
                grid.attach(self._create_label(key), 0, row, 1, 1)
                nested_path = f"{path}.{module_name}"
                widget = self._create_theme_control(nested_path, key, value)
                grid.attach(widget, 1, row, 1, 1)
                row += 1

        container.add(module_box)

    def _create_theme_nested_section(
        self, container: Box, section_name: str, section_config: dict, path: str
    ):
        """Create an expandable section for theme config."""
        expander = self._create_expander(section_name.replace("_", " ").title())

        inner_box = Box(orientation="v", spacing=4, style="margin-left: 20px;")
        grid = self._create_grid()
        inner_box.add(grid)

        row = 0
        for key, value in section_config.items():
            if isinstance(value, dict):
                # Handle deeper nesting recursively
                self._create_theme_nested_section(
                    inner_box, key, value, f"{path}.{section_name}"
                )
            elif isinstance(value, list):
                continue  # Skip lists for now
            else:
                grid.attach(self._create_label(key), 0, row, 1, 1)
                nested_path = f"{path}.{section_name}"
                widget = self._create_theme_control(nested_path, key, value)
                grid.attach(widget, 1, row, 1, 1)
                row += 1

        expander.add(inner_box)
        container.add(expander)

    def _create_theme_control(self, path: str, key: str, value) -> Gtk.Widget:
        """Create appropriate control for a theme value."""
        if isinstance(value, bool):
            return self._create_switch(
                value,
                lambda sw, _, p=path, k=key: self._update_theme(p, k, sw.get_active()),
            )
        elif isinstance(value, int):
            return self._create_spinbutton(
                value,
                0,
                10000,
                lambda sp, p=path, k=key: self._update_theme(
                    p, k, int(sp.get_value())
                ),
            )
        elif isinstance(value, str):
            # Special handling for wallpaper field
            if key == "wallpaper":
                return self._create_wallpaper_picker(path, key, value)

            enum_options = self._get_theme_enum_options(key)
            if enum_options:
                return self._create_combo(
                    enum_options,
                    value,
                    lambda cb, p=path, k=key: self._update_theme(
                        p, k, cb.get_active_text()
                    ),
                )
            entry = Entry(text=value, h_expand=False)
            entry.set_width_chars(15)
            entry.connect(
                "changed",
                lambda e, p=path, k=key: self._update_theme(p, k, e.get_text()),
            )
            return entry
        return Label(label=str(value), h_align="start")

    def _create_wallpaper_picker(self, path: str, key: str, value: str) -> Gtk.Widget:
        """Create a wallpaper file picker control."""
        # Create horizontal box for entry and button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # Create entry for path
        entry = Entry(text=value, h_expand=True)
        entry.connect(
            "changed",
            lambda e, p=path, k=key: self._update_theme(p, k, e.get_text()),
        )
        hbox.pack_start(entry, True, True, 0)

        # Create browse button
        browse_btn = HoverButton(label="Browse...", name="settings-browse-btn")
        browse_btn.connect("clicked", self._on_browse_wallpaper, entry, path, key)
        hbox.pack_start(browse_btn, False, False, 0)

        return hbox

    def _on_browse_wallpaper(self, button, entry, path: str, key: str):
        """Handle wallpaper file selection."""
        dialog = Gtk.FileChooserDialog(
            title="Select Wallpaper",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
        )

        # Add filters for image files
        filter_images = Gtk.FileFilter()
        filter_images.set_name("Image files")
        filter_images.add_mime_type("image/*")
        dialog.add_filter(filter_images)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)

        # Add buttons
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Select", Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if filename:
                entry.set_text(filename)
                self._update_theme(path, key, filename)

        dialog.destroy()

    def _get_theme_enum_options(self, key: str) -> list | None:
        """Get enum options for theme keys."""
        # Add theme-specific enums if needed
        theme_enums = {
            # Add any theme-specific enums here
        }
        return theme_enums.get(key)

    def _update_theme(self, path: str, key: str, value):
        """Update theme value at any nesting level."""
        parts = path.split(".")
        target = self.theme

        for part in parts[1:]:  # Skip 'theme' prefix
            if part not in target:
                target[part] = {}
            target = target[part]

        if target.get(key) != value:
            target[key] = value
            self.modified = True
            self.save_btn.set_sensitive(True)

    def _create_about_tab(self):
        """Create the about tab."""

        vbox = Box(orientation="v", spacing=18, style="margin: 30px;", h_align="center")

        # Logo
        logo = Image(
            image_file=f"{ASSETS_DIR}/images/logo.png",
            size=160,
            h_align="center",
            v_align="center",
        )
        vbox.add(logo)

        vbox.add(
            Label(
                label="A modular status bar for Hyprland, powered by Fabric.",
                h_align="center",
                style="margin-bottom: 12px;",
            )
        )

        repo_box = Box(orientation="h", spacing=6, h_align="center")
        repo_box.add(Label(label="GitHub:", h_align="start"))
        repo_box.add(
            Label(
                markup='<a href="https://github.com/rubiin/tsumiki">rubiin/tsumiki</a>'
            )
        )
        vbox.add(repo_box)

        return vbox

    def _update_config(self, path: str, key: str, value):
        """Update config value at any nesting level."""
        parts = path.split(".")
        target = self.config

        for part in parts:
            if part not in target:
                target[part] = {}
            target = target[part]

        if target.get(key) != value:
            target[key] = value
            self.modified = True
            self.save_btn.set_sensitive(True)

    def _on_save(self, *_):
        """Save configuration."""
        try:
            write_json_file(configuration.json_config_file, self.config)
            write_json_file(configuration.theme_file, self.theme)
            self.modified = False
            self.save_btn.set_sensitive(False)
            exec_shell_command_async(
                'notify-send "Tsumiki" "Configuration saved"',
                lambda _: None,
            )
        except Exception as e:
            exec_shell_command_async(
                f'notify-send "Tsumiki" "Failed to save: {e}"',
                lambda _: None,
            )

    def _on_reset(self, *_):
        """Reset to saved config."""
        self.config = dict(widget_config)
        self.theme = dict(theme_config)
        self.modified = False
        self.save_btn.set_sensitive(False)
        self._refresh_tabs()

    def _on_close(self, *_):
        """Close the window."""
        self.hide()
        SettingsGUI._visible = False

    def _on_delete(self, *_):
        """Handle window close."""
        self.hide()
        SettingsGUI._visible = False
        return True  # Prevent destruction

    def toggle(self):
        """Toggle window visibility."""
        if SettingsGUI._visible:
            self.hide()
            SettingsGUI._visible = False
        else:
            self.show_all()
            SettingsGUI._visible = True


def open_settings():
    """Open the settings GUI."""
    SettingsGUI().toggle()
