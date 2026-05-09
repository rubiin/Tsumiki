from fabric.hyprland.widgets import HyprlandLanguage
from fabric.utils import FormattedString, logger, truncate
from fabric.widgets.label import Label

try:
    from fabric.i3.widgets import I3Language
except Exception:
    I3Language = None

from shared.widget_container import ButtonWidget
from utils.functions import get_window_manager_backend
from utils.widget_utils import nerd_font_icon


class LanguageWidget(ButtonWidget):
    """A widget to display the current language."""

    def __init__(self, **kwargs):
        super().__init__(name="language", **kwargs)

        backend = get_window_manager_backend()

        if backend == "sway" and I3Language is not None:
            language_widget = I3Language
        elif backend == "i3":
            language_widget = None
            logger.warning(
                "[language] i3 does not expose keyboard layout change events; "
                "showing fallback label"
            )
        else:
            language_widget = HyprlandLanguage

        if language_widget is None:
            self.lang = Label(
                label=self.config.get("fallback_label", "N/A"),
                style_classes=["panel-text"],
            )
        else:
            self.lang = language_widget(
                formatter=FormattedString(
                    "{truncate(language,length,suffix)}",
                    truncate=truncate,
                    length=self.config.get("truncation_size", 10),
                    suffix="",
                ),
                style_classes=["panel-text"],
            )

        if self.config.get("show_icon", True):
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": ["panel-font-icon"],
                },
            )
            self.container_box.add(self.icon)

        self.container_box.add(self.lang)

        if self.config.get("tooltip", False):
            self.set_tooltip_text(f"Language: {self.lang.get_label()}")
