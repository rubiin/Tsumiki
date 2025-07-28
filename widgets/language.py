from fabric.hyprland.widgets import HyprlandLanguage as Language
from fabric.utils import FormattedString, truncate

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class LanguageWidget(ButtonWidget):
    """A widget to display the current language."""

    def __init__(self, **kwargs):
        super().__init__(name="language", **kwargs)

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config.get("truncation_size", 10),
                suffix="",
            ),
            style_classes="panel-text",
        )

        if self.config.get("show_icon", True):
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": "panel-font-icon",
                },
            )
            self.box.add(self.icon)

        self.box.add(self.lang)

        if self.config.get("tooltip", False):
            self.set_tooltip_text(f"Language: {self.lang.get_label()}")
