import re

from fabric.hyprland.widgets import HyprlandActiveWindow as ActiveWindow
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
                get_title=self._get_title,
            ),
        )

        # Add the ActiveWindow widget as a child
        self.container_box.children = self.active_window

    def _get_title(self, win_title: str, win_class: str):
        mappings_enabled = self.config.get("mappings", True)
        trunc = self.config.get("truncation", True)
        trunc_size = self.config.get("truncation_size", 50)

        if not mappings_enabled:
            return truncate(win_title, trunc_size) if trunc else win_title

        custom_map = self.config.get("title_map", [])
        icon_enabled = self.config.get("icon", True)

        if self.config.get("tooltip", True):
            self.set_tooltip_text(win_title)

        win_title = truncate(win_title, trunc_size) if trunc else win_title
        merged_titles = WINDOW_TITLE_MAP + (
            custom_map if isinstance(custom_map, list) else []
        )

        for pattern, icon, name in merged_titles:
            try:
                if re.search(pattern, win_class.lower()):
                    return f"{icon} {name}" if icon_enabled else name
            except re.error as e:
                logger.warning(f"[window_title] Invalid regex '{pattern}': {e}")

        fallback = (
            win_class.lower()
            if self.config.get("fallback", "class") == "class"
            else win_title
        )
        fallback = truncate(fallback, trunc_size) if trunc else fallback
        return f"󰣆 {fallback}"
