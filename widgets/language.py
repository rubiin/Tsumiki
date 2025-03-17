from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box

from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


class LanguageWidget(ButtonWidget):
    """A widget to display the current language."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="language", **kwargs)

        self.config = widget_config["language"]

        self.box = Box()
        self.children = (self.box,)

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config["truncation_size"],
                suffix="",
            ),
            style_classes="panel-text",
        )

        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={
                "style_classes": "panel-icon",
            },
        )

        self.box.children = (self.icon, self.lang)

        if self.config["tooltip"]:
            self.set_tooltip_text(f"Language: {self.lang.get_label()}")
