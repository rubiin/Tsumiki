import os

from fabric.utils import get_relative_path

from shared.widget_container import ButtonWidget
from utils.functions import copy_theme, send_notification
from utils.widget_utils import nerd_font_icon


class ThemeSwitcherWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, **kwargs):
        super().__init__(name="theme_switcher", **kwargs)

        theme_files = os.listdir(get_relative_path("../styles/themes"))

        # Remove the '.scss' part from each string in the list
        self.themes_list = [style.replace(".scss", "") for style in theme_files]

        self.current_theme = "some_default_theme"  # TODO: Set a default theme

        self.children = nerd_font_icon(
            self.config["icon"],
            props={"style_classes": "panel-font-icon"},
        )
        self.set_tooltip_text(self.current_theme)
        self.connect("clicked", self.handle_click)

    ## Cycle through the themes on click
    def handle_click(self, *_):
        """Cycle through the themes."""
        self.current_theme = self.themes_list[
            (self.themes_list.index(self.current_theme) + 1) % len(self.themes_list)
        ]

        if self.config["notify"]:
            send_notification("hydepanel", f"Theme switched to {self.current_theme}")
        copy_theme(self.current_theme)
        self.set_tooltip_text(self.current_theme)
