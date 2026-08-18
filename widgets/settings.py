"""Settings button widget to open the settings GUI."""

from fabric.widgets.label import Label

from modules.settings_gui import open_settings
from shared.widget_container import ButtonWidget
from utils.i18n import _
from utils.widget_utils import nerd_font_icon


class SettingsWidget(ButtonWidget):
    """A widget to open the settings panel."""

    def __init__(self, **kwargs):
        super().__init__(name="settings", **kwargs)

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰒓"),
            props={"style_classes": ["panel-font-icon"]},
        )

        if self.config.get("label", False):
            self.container_box.add(
                Label(label=_("widget.settings.label"), style_classes="panel-text")
            )

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            self.set_tooltip_text(_("widget.settings.tooltip"))

        self.connect("clicked", lambda *_: open_settings())
