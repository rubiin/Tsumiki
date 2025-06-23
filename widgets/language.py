from fabric.hyprland.widgets import Language
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
                length=self.config["truncation_size"],
                suffix="",
            ),
            style_classes="panel-text",
        )

        if self.config["show_icon"]:
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={
                    "style_classes": "panel-font-icon",
                },
            )
            self.box.add(self.icon)

        self.box.add(self.lang)

        if self.config["tooltip"]:
            self.set_tooltip_text(f"Language: {self.lang.get_label()}")
