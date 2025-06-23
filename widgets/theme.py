import os
import threading

from fabric.utils import get_relative_path

from shared.widget_container import ButtonWidget
from utils.config import theme_config
from utils.functions import (
    copy_theme,
    recompile_and_apply_css,
    send_notification,
    update_theme_config,
)
from utils.widget_utils import nerd_font_icon


class ThemeSwitcherWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, **kwargs):
        super().__init__(name="theme_switcher", **kwargs)

        # Lock to prevent concurrent theme switching
        self._switching_lock = threading.Lock()
        self._is_switching = False

        theme_files = os.listdir(get_relative_path("../styles/themes"))

        # Remove the '.scss' part from each string in the list
        self.themes_list = [style.replace(".scss", "") for style in theme_files]

        # Get current theme from theme config, with fallback
        self.current_theme = theme_config.get("name", "catpuccin-mocha")

        # Ensure current theme is in the themes list, fallback to first available theme
        if self.current_theme not in self.themes_list:
            self.current_theme = self.themes_list[0] if self.themes_list else "catpuccin-mocha"

        self.children = nerd_font_icon(
            self.config["icon"],
            props={"style_classes": "panel-font-icon"},
        )
        self.set_tooltip_text(self.current_theme)
        self.connect("clicked", self.handle_click)

    ## Cycle through the themes on click
    def handle_click(self, *_):
        """Cycle through the themes."""
        if not self.themes_list:
            return  # No themes available

        try:
            current_index = self.themes_list.index(self.current_theme)
        except ValueError:
            # Current theme not in list, start from beginning
            current_index = -1

        self.current_theme = self.themes_list[
            (current_index + 1) % len(self.themes_list)
        ]

        if self.config["notify"]:
            send_notification("hydepanel", f"Theme switched to {self.current_theme}")
        copy_theme(self.current_theme)
        update_theme_config(self.current_theme)
        recompile_and_apply_css()
        self.set_tooltip_text(self.current_theme)
