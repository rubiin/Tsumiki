"""
Settings GUI for Tsumiki
"""

from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.entry import Entry
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.stack import Stack
from fabric.widgets.window import Window
from gi.repository import Gtk

from shared.buttons import HoverButton
from utils.config import configuration, widget_config
from utils.functions import write_json_file


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

    def _create_config_section(
        self, vbox: Box, section_name: str, config_items: dict, path_prefix: str
    ):
        """Create a configuration section with grid of controls."""
        vbox.add(self._create_section_header(section_name.replace("_", " ").title()))

        grid = self._create_grid(margin_bottom=15)
        vbox.add(grid)

        row = 0
        for key, value in config_items.items():
            if isinstance(value, (dict, list)):
                continue

            grid.attach(self._create_label(key), 0, row, 1, 1)

            path = f"{path_prefix}.{section_name}"
            widget = self._create_control(path, key, value)
            grid.attach(widget, 1, row, 1, 1)
            row += 1

    def _create_modules_tab(self):
        """Create the modules settings tab."""
        scrolled, vbox = self._create_scrolled_container()
        modules = self.config.get("modules", {})

        for module_name, module_config in modules.items():
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
                10000,
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
            "layer": ["top", "bottom", "overlay", "background"],
            "anchor": [
                "top",
                "bottom",
                "center",
                "top-left",
                "top-right",
                "bottom-left",
                "bottom-right",
                "center-left",
                "center-right",
            ],
            "location": ["top", "bottom", "left", "right"],
            "orientation": ["horizontal", "vertical"],
            "transition_type": [
                "none",
                "crossfade",
                "slide-up",
                "slide-down",
                "slide-left",
                "slide-right",
            ],
            "layout": ["list", "grid"],
            "mode": ["label", "circular", "graph"],
            "behavior": ["always", "intellihide", "autohide"],
            "temperature_unit": ["celsius", "fahrenheit"],
            "unit": ["gb", "mb", "percent"],
            "clock_format": ["12h", "24h"],
        }
        return enums.get(key)

    def _create_about_tab(self):
        """Create the about tab."""
        vbox = Box(orientation="v", spacing=18, style="margin: 30px;")

        vbox.add(
            Label(
                markup="<b>Tsumiki</b>",
                h_align="start",
                style="font-size: 1.5em; margin-bottom: 8px;",
            )
        )

        vbox.add(
            Label(
                label="A modular status bar for Hyprland, powered by Fabric.",
                h_align="start",
                style="margin-bottom: 12px;",
            )
        )

        repo_box = Box(orientation="h", spacing=6, h_align="start")
        repo_box.add(Label(label="GitHub:", h_align="start"))
        repo_box.add(
            Label(
                markup='<a href="https://github.com/rubiin/tsumiki">https://github.com/rubiin/tsumiki</a>'
            )
        )
        vbox.add(repo_box)

        vbox.add(Box(v_expand=True))
        return vbox

    def _update_config(self, path: str, key: str, value):
        """Update config value."""
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
