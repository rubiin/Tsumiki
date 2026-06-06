from typing import Iterable

from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget

from utils.config import widget_config


class BaseWidget(Widget):
    """A base widget class that can be extended for custom widgets."""

    @staticmethod
    def _merge_style_classes(
        defaults: list[str],
        style_classes: str | Iterable[str] | None,
    ) -> list[str]:
        merged = list(defaults)
        if style_classes is None:
            return merged

        if isinstance(style_classes, str):
            merged.append(style_classes)
        else:
            merged.extend(style_classes)
        return merged

    def _init_widget_settings(self, widget_name: str) -> None:
        self.config: dict = widget_config.get("widgets", {}).get(widget_name, {})
        self.general_config: dict = widget_config.get("general", {})
        self.tooltips_enabled = self.general_config.get("tooltips", True)

    def _connect_hover_reveal(self) -> None:
        if not self.config.get("hover_reveal", True):
            return

        bulk_connect(
            self,
            {
                "enter-notify-event": self._toggle_revealer,
                "leave-notify-event": self._toggle_revealer,
            },
        )

    def toggle(self):
        """Toggle the visibility of the bar."""
        if self.is_visible():
            self.hide()
        else:
            self.show()

    def toggle_css_class(self, class_name: str | Iterable[str], condition: bool):
        if condition and self.get_style_context().has_class(class_name):
            self.add_style_class(class_name)
        else:
            self.remove_style_class(class_name)

    def _toggle_revealer(self, *_):
        if hasattr(self, "revealer"):
            self.revealer.set_reveal_child(not self.revealer.get_reveal_child())

    def set_active_style(self, action: bool, *_) -> None:
        self.set_style_classes("") if not action else self.set_style_classes("active")


class BaseWindow(Window, BaseWidget):
    """A base window class that can be extended for custom windows."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BoxWidget(Box, BaseWidget):
    """A container for box widgets."""

    def __init__(self, spacing=None, style_classes=None, **kwargs):
        all_styles = self._merge_style_classes(["panel-box"], style_classes)

        super().__init__(
            spacing=4 if spacing is None else spacing,
            style_classes=all_styles,
            **kwargs,
        )

        widget_name = kwargs.get("name", "box")
        self._init_widget_settings(widget_name)


class EventBoxWidget(EventBox, BaseWidget):
    """A container for box widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes=["panel-eventbox"],
            **kwargs,
        )

        widget_name = kwargs.get("name", "eventbox")
        self._init_widget_settings(widget_name)
        self.container_box = Box(name="widget-container", style_classes=["panel-box"])
        self.add(
            self.container_box,
        )
        self._connect_hover_reveal()
        from utils.widget_utils import setup_cursor_hover

        setup_cursor_hover(self)


class ButtonWidget(Button, BaseWidget):
    """A container for button widgets. Only used for new widgets that are used on bar"""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes=["panel-button"],
            **kwargs,
        )

        widget_name = kwargs.get("name", "button")
        self._init_widget_settings(widget_name)

        self.container_box = Box(style_classes=["box"])
        self.add(self.container_box)
        self._connect_hover_reveal()

        self.connect(
            "state-flags-changed",
            lambda btn, *_: (
                btn.set_cursor("pointer")
                if btn.get_state_flags() & 2  # type: ignore
                else btn.set_cursor("default"),
            ),
        )


class WidgetGroup(BoxWidget):
    """A group of widgets that can be managed and styled together."""

    def __init__(self, children=None, spacing=4, style_classes=None, **kwargs):
        css_classes = self._merge_style_classes(["panel-module-group"], style_classes)

        super().__init__(
            spacing=spacing,
            style_classes=css_classes,
            orientation="h",  # Default to horizontal for panel layout
            **kwargs,
        )

        if children:
            for child in children:
                self.add(child)

    @classmethod
    def from_config(cls, config, widgets_list, main_config=None):
        from utils.widget_factory import WidgetResolver

        resolver = WidgetResolver(widgets_list)
        context = {"config": main_config} if main_config else {}

        widgets = resolver.batch_resolve(config.get("widgets", []), context)

        return cls(
            children=widgets,
            spacing=config.get("spacing", 4),
            style_classes=config.get("style_classes", []),
        )
