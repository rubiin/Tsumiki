"""Settings button widget to open the settings GUI."""

from fabric.widgets.label import Label

from modules.settings_gui import SettingsGUI
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class SettingsWidget(ButtonWidget):
    """A widget to open the settings panel."""

    def __init__(self, **kwargs):
        super().__init__(name="settings", **kwargs)

        self._settings_window = None

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰒓"),
            props={"style_classes": ["panel-font-icon"]},
        )

        if self.config.get("label", False):
            self.container_box.add(
                Label(label="Settings", style_classes=["panel-text"])
            )

        if self.config.get("tooltip", True):
            self.set_tooltip_text("Open Settings")

        self.connect("clicked", self.on_click)

    def on_click(self, *_):
        """Open the settings window."""
        if self._settings_window is None:
            self._settings_window = SettingsGUI()

        self._settings_window.toggle()
