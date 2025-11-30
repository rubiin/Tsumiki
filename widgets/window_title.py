import re

from fabric.hyprland.widgets import HyprlandActiveWindow as ActiveWindow
from fabric.utils import FormattedString, logger, truncate

from shared.widget_container import ButtonWidget
from utils.constants import WINDOW_TITLE_MAP

# Pre-compile regex patterns from WINDOW_TITLE_MAP at module load
_COMPILED_PATTERNS: dict[str, re.Pattern | None] = {}


def _get_compiled_pattern(pattern: str) -> re.Pattern | None:
    """Get or compile a regex pattern, caching the result."""
    if pattern not in _COMPILED_PATTERNS:
        try:
            _COMPILED_PATTERNS[pattern] = re.compile(pattern)
        except re.error:
            _COMPILED_PATTERNS[pattern] = None
    return _COMPILED_PATTERNS[pattern]


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

        win_class_lower = win_class.lower()
        for pattern, icon, name in merged_titles:
            compiled = _get_compiled_pattern(pattern)
            if compiled is None:
                logger.warning(f"[window_title] Invalid regex '{pattern}'")
                continue
            if compiled.search(win_class_lower):
                return f"{icon} {name}" if icon_enabled else name

        fallback = (
            win_class_lower
            if self.config.get("fallback", "class") == "class"
            else win_title.lower()
        )
        fallback = truncate(fallback, trunc_size) if trunc else fallback
        return f"󰣆 {fallback}"
