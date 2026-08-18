from fabric.utils import logger

from services import style_service
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.functions import send_notification
from utils.widget_utils import nerd_font_icon


class ThemeSwitcherWidget(ButtonWidget):
    """A widget to cycle through available themes."""

    def __init__(self, **kwargs):
        super().__init__(name="theme_switcher", **kwargs)

        self._style_service = style_service

        # Get current theme from service
        self._current_theme = self._style_service.current_theme

        self.children = nerd_font_icon(
            icon=self.config.get("icon"),
            props={"style_classes": ["panel-font-icon"]},
        )
        self.set_tooltip_text(self._current_theme)
        self.connect("clicked", self.on_click)

        # Keep tooltip in sync with theme changes
        self._style_service.connect("theme_changed", self._on_theme_changed)

    def _on_theme_changed(self, _service, theme_name: str):
        """Update tooltip when the theme changes externally."""
        self._current_theme = theme_name
        self.set_tooltip_text(theme_name)

    def on_click(self, *_):
        """Cycle to the next theme via StyleService."""
        if not self._style_service.available_themes:
            logger.warning(f"{Colors.WARNING}[ThemeSwitcher] No themes available")
            return

        new_theme = self._style_service.next_theme()

        if self.config.get("notify", True):
            send_notification("Tsumiki", _('widget.theme.switched', theme=new_theme))

        self.set_tooltip_text(new_theme)
