import os
import re

from fabric.hyprland.widgets import ActiveWindow
from fabric.utils import FormattedString, truncate
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.constants import WINDOW_TITLE_MAP


class WindowTitleWidget(ButtonWidget):
    """a widget that displays the title of the active window."""

    def __init__(self, **kwargs):
        super().__init__(name="window_title", **kwargs)

        # Create an ActiveWindow widget to track the active window
        self.active_window = ActiveWindow(
            name="window",
            formatter=FormattedString(
                "{ get_title(win_title, win_class) }",
                get_title=self.get_title,
            ),
        )

        # Add the ActiveWindow widget as a child
        self.box.children = self.active_window

    def get_title(self, win_title: str, win_class: str):
        trunc = self.config.get("truncation", True)
        trunc_size = self.config.get("truncation_size", 50)
        custom_map = self.config.get("title_map", [])
        icon_enabled = self.config.get("icon", True)

        win_title = truncate(win_title, trunc_size) if trunc else win_title
        merged_titles = WINDOW_TITLE_MAP + (
            custom_map if isinstance(custom_map, list) else []
        )

        if not os.path.exists("some.log"):
            with open("some.log", "w") as log_file:
                log_file.write(f"Window Title: {win_title}\n")
                log_file.write(f"Window Class: {win_class}\n")
                log_file.write(f"Custom Map: {custom_map}\n")

        for pattern, icon, name in merged_titles:
            try:
                if re.search(pattern, win_class.lower()):
                    return f"{icon} {name}" if icon_enabled else name
            except re.error as e:
                logger.warning(f"[window_title] Invalid regex '{pattern}': {e}")

        fallback = win_class.lower()
        fallback = truncate(fallback, trunc_size) if trunc else fallback
        return f"󰣆 {fallback}"
