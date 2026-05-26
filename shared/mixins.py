"""
Reusable mixins for reducing code duplication across widgets.

These mixins provide common patterns used throughout the codebase
"""

from collections import deque
from typing import Callable

from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

from utils.widget_utils import get_bar_graph, nerd_font_icon


class PopoverMixin:
    """
    Mixin for lazy popover initialization.
    """

    _popup = None
    _popover_content_factory: Callable | None = None

    def setup_popover(
        self,
        content_factory: Callable,
        connect_clicked: bool = True,
        on_close_callback: Callable | None = None,
    ) -> None:
        """
        Setup lazy popover initialization.

        Args:
            content_factory: Callable that returns the popover content widget
            connect_clicked: Whether to auto-connect "clicked" signal
            on_close_callback: Optional callback when popover closes
        """
        self._popover_content_factory = content_factory
        self._popover_on_close = on_close_callback

        if connect_clicked:
            self.connect("clicked", self.show_popover)

    def show_popover(self, *_) -> None:
        """Show the popover, creating it lazily on first use."""
        if self._popup is None and self._popover_content_factory is not None:
            from shared.popover import Popover

            self._popup = Popover(
                content=self._popover_content_factory(),
                point_to=self,
            )

            if self._popover_on_close:
                self._popup.connect("popover-closed", self._popover_on_close)
            else:
                self._popup.connect(
                    "popover-closed", lambda *_: self.remove_style_class("active")
                )

        if self._popup:
            self._popup.open()
            self.add_style_class("active")

    def hide_popover(self) -> None:
        """Hide the popover if it exists."""
        if self._popup:
            self._popup.hide()
            self.remove_style_class("active")

    def toggle_popover(self) -> None:
        """Toggle popover visibility."""
        if self._popup and self._popup.get_visible():
            self.hide_popover()
        else:
            self.show_popover()

    @property
    def popup(self):
        """Property for backward compatibility with existing code."""
        return self._popup

    @popup.setter
    def popup(self, value):
        """Setter for backward compatibility."""
        self._popup = value


class StatDisplayMixin:
    """
    Mixin for stats widgets (CPU, GPU, Memory, Storage) that share
    common display modes: label, graph, and progress (circular).
    """

    __slots__ = (
        "_graph_maxlen",
        "current_mode",
        "graph_values",
        "icon",
        "level_label",
        "progress_bar",
    )

    _stat_icon: str = "󰕸"
    _stat_name: str = "stat"

    def setup_stat_display(self, container) -> None:
        """
        Setup the display mode (graph, progress, or label) based on config.
        """
        self.current_mode = self.config.get("mode", "label")

        if self.current_mode == "graph":
            self._setup_graph_mode(container)
        elif self.current_mode == "progress":
            self._setup_progress_mode(container)
        else:
            self._setup_label_mode(container)

    def _setup_graph_mode(self, container) -> None:
        """Setup graph display mode with bar characters."""
        self._graph_maxlen = self.config.get("graph_length", 4)
        self.graph_values = deque(maxlen=self._graph_maxlen)
        self.level_label = Label(
            label="0%",
            style_classes=["panel-text"],
        )
        container.children = self.level_label

    def _setup_progress_mode(self, container) -> None:
        """Setup circular progress bar display mode."""
        self.progress_bar = CircularProgressBar(
            name="stat-circle",
            line_style="round",
            line_width=2,
            size=28,
            start_angle=150,
            end_angle=390,
        )

        self.icon = nerd_font_icon(
            icon=self.config.get("icon", self._stat_icon),
            props={"style_classes": ["panel-font-icon", "overlay-icon"]},
        )

        container.children = (
            Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
        )

    def _setup_label_mode(self, container) -> None:
        """Setup text label display mode with icon."""
        self.icon = nerd_font_icon(
            icon=self.config.get("icon", self._stat_icon),
            props={"style_classes": ["panel-font-icon"]},
        )

        self.level_label = Label(
            label="0%",
            style_classes=["panel-text"],
        )
        container.children = (self.icon, self.level_label)

    def update_stat_display(self, value: float, label_text: str) -> None:
        """
        Update the stat display based on current mode.

        Args:
            value: The stat value (0-100 for percentage)
            label_text: Text to display in label mode
        """
        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(value))
            self.level_label.set_label("".join(self.graph_values))
        elif self.current_mode == "progress":
            self.progress_bar.set_value(value / 100.0)
        else:
            self.level_label.set_label(label_text)
