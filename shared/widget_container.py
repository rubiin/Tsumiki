from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.widget import Widget

from utils.config import widget_config


class ToggleableWidget(Widget):
    """A widget that can be toggled on and off."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle(self):
        """Toggle the visibility of the bar."""
        if self.is_visible():
            self.hide()
        else:
            self.show()


class BoxWidget(Box, ToggleableWidget):
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

        widget_name = kwargs.get("name", "box")
        self.config = widget_config["widgets"].get(widget_name, {})


class EventBoxWidget(EventBox, ToggleableWidget):
    """A container for box widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-eventbox",
            **kwargs,
        )

        widget_name = kwargs.get("name", "eventbox")
        self.config = widget_config["widgets"].get(widget_name, {})

        self.box = Box(style_classes="panel-box")
        self.add(
            self.box,
        )


class ButtonWidget(Button, ToggleableWidget):
    """A container for button widgets. Only used for new widgets that are used on bar"""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )

        widget_name = kwargs.get("name", "button")
        self.config = widget_config["widgets"].get(widget_name, {})

        self.box = Box()
        self.add(self.box)


4


class WidgetGroup(BoxWidget):
    """A group of widgets that can be managed and styled together."""

    def __init__(self, children=None, spacing=4, style_classes=None, **kwargs):
        # Build our list of CSS classes
        css_classes = ["panel-module-group"]

        # Add any custom style classes
        if style_classes:
            if isinstance(style_classes, str):
                css_classes.append(style_classes)
            elif isinstance(style_classes, list):
                css_classes.extend(style_classes)

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
    def from_config(cls, config, widgets_map):
        children = []
        for widget_name in config.get("widgets", []):
            if widget_name in widgets_map:
                # Create widget instance using the constructor from widgets_map
                # Pass both widget_config and bar to the widget constructor
                widget = widgets_map[widget_name]
                children.append(widget())

        return cls(
            children=children,
            spacing=config.get("spacing", 4),
            style_classes=config.get("style_classes", []),
        )
