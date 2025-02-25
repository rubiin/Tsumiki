from fabric.widgets.box import Box
from .widget_container import BoxWidget

class ModuleGroup(BoxWidget):
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
    def from_config(cls, config, widgets_map, bar=None, widget_config=None):
        children = []
        for widget_name in config.get("widgets", []):
            if widget_name in widgets_map:
                # Create widget instance using the constructor from widgets_map
                # Pass both widget_config and bar to the widget constructor
                widget = widgets_map[widget_name](widget_config, bar=bar)
                children.append(widget)

        return cls(
            children=children,
            spacing=config.get("spacing", 4),
            style_classes=config.get("style_classes", [])
        )
