from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox

from utils.config import widget_config
from utils.widget_utils import setup_cursor_hover


def get_style():
    widget_style = widget_config["general"]["widget_style"]
    return widget_style


class BoxWidget(Box):
    """A container for box widgets."""

    def __init__(self, spacing=None, style_classes=None, **kwargs):
        # Handle style classes
        all_styles = ["panel-box"]
        if style_classes:
            if isinstance(style_classes, str):
                all_styles.append(style_classes)
            else:
                all_styles.extend(style_classes)

        super().__init__(
            spacing=4 if spacing is None else spacing,
            style_classes=all_styles,
            **kwargs,
        )

        widget_style = get_style()
        self.add_style_class(widget_style)


class EventBoxWidget(EventBox):
    """A container for box widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            name="panel-eventbox",
            **kwargs,
        )

        widget_style = get_style()

        # hacky way to add style class to the child widget. but honest work
        self.connect(
            "child-notify", lambda *_: self.children[0].add_style_class(widget_style)
        )


class ButtonWidget(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )

        widget_style = get_style()

        setup_cursor_hover(self)

        self.add_style_class(widget_style)


class HoverButton(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        setup_cursor_hover(self)
