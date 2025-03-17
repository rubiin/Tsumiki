from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox

from utils.widget_utils import setup_cursor_hover


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


class EventBoxWidget(EventBox):
    """A container for box widgets."""

    def __init__(self, config, **kwargs):
        super().__init__(
            name="panel-eventbox",
            **kwargs,
        )

        widget_style = config["general"]["widget_style"]
        self.add_style_class(widget_style)
        setup_cursor_hover(self)

        # hacky way to add style class to the child widget. but honest work
        self.connect(
            "child-notify", lambda *_: self.children[0].add_style_class(widget_style)
        )


class ButtonWidget(Button):
    """A container for button widgets."""

    def __init__(self, config, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )

        if config:
            widget_style = config["general"]["widget_style"]
            self.add_style_class(widget_style)

        setup_cursor_hover(self)


class HoverButton(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        setup_cursor_hover(self)
