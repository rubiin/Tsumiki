from fabric.widgets.box import Box
from fabric.widgets.label import Label

from utils.widget_utils import nerd_font_icon

from .widget_container import ButtonWidget


class CollapsibleGroupWidget(ButtonWidget):
    """A collapsible button group that shows a main toggle button in the bar.

    When clicked, reveals a popup menu with grouped widgets underneath.
    Uses lazy initialization for performance.
    """

    def __init__(self, **kwargs):
        super().__init__(name="collapsible_group", **kwargs)

        # Initialize defaults - will be overridden when config is updated
        self.widgets_config = []
        self.icon_name = "󰍽"  # default icon
        self.show_icon = True
        self.show_label = False
        self.label_text = "Tools"
        self.tooltip_text = "Toggle tool menu"

        self.is_expanded = False
        self.popup = None
        self.widgets_list = None

        # Read configuration and setup the widget
        self._read_config()
        self._setup_button_content()
        self.connect("clicked", self.on_toggle_clicked)

        if self.tooltip_text:
            self.set_tooltip_text(self.tooltip_text)

    def _read_config(self):
        """Read configuration values from the config."""
        # Fix: Read config directly instead of from non-existent "group" key
        self.widgets_config = self.config.get("widgets", [])
        self.icon_name = self.config.get("icon", "󰍽")
        self.show_icon = self.config.get("show_icon", True)
        self.show_label = self.config.get("show_label", False)
        self.label_text = self.config.get("label", "Tools")
        self.tooltip_text = self.config.get("tooltip", "Toggle tool menu")

    def _setup_button_content(self):
        """Set up the content of the main toggle button."""
        if self.show_icon:
            icon = nerd_font_icon(
                icon=self.icon_name,
                props={"style_classes": ["panel-font-icon"]},
            )
            self.container_box.add(icon)

        if self.show_label:
            label = Label(label=self.label_text, style_classes=["panel-text"])
            self.container_box.add(label)

    def _setup_popup(self):
        """Set up the popup that contains the grouped widgets."""

        from .popover import Popover

        # Fix: Read spacing and style_classes directly from config
        self.widgets_box = Box(
            orientation="h",
            spacing=self.config.get("spacing", 4),
            style_classes=[
                "panel-collapsible-group",
                *self.config.get("style_classes", []),
            ],
        )

        self._populate_widgets()

        self.popup = Popover(content=self.widgets_box, point_to=self)
        self.popup.connect(
                "popover-closed", lambda *_: self.remove_style_class("active")
            )

    def _set_expanded(self, expanded: bool):
        """Sets the expanded state of the widget."""
        if self.is_expanded == expanded:
            return  # No change

        if expanded:
            if self.popup is None:
                self._setup_popup()
            self.popup.open()
        elif self.popup:
            self.popup.hide_popover()

        self.is_expanded = expanded
        self.toggle_css_class("active", self.is_expanded)

    def on_toggle_clicked(self, button):
        """Handle the toggle button click."""
        self._set_expanded(not self.is_expanded)

    def _populate_widgets(self):
        """Populate the widgets box with configured widgets."""
        if not hasattr(self, "widgets_box") or not hasattr(self, "_resolver_context"):
            return

        # Clear existing widgets
        for child in self.widgets_box.get_children():
            child.destroy()

        # Use the widget factory system
        from utils.widget_factory import WidgetResolver

        resolver = WidgetResolver(self.widgets_list or {})
        widgets = resolver.batch_resolve(self.widgets_config, self._resolver_context)

        for widget in widgets:
            self.widgets_box.add(widget)

    def set_context(self, config: dict, widgets_list: dict):
        """Set resolution context for widget creation.

        Args:
            config: Main configuration dictionary
            widgets_list: Dictionary mapping widget names to widget classes
        """
        self._resolver_context = {"config": config}
        self.widgets_list = widgets_list

    def collapse(self):
        """Collapse the group programmatically."""
        self._set_expanded(False)

    def expand(self):
        """Expand the group programmatically."""
        self._set_expanded(True)

    def update_config(self, config_dict):
        """Update the widget configuration and refresh the display."""
        self.config.update(config_dict)
        self._read_config()

        # Clear and rebuild button content with new config
        for child in self.container_box.get_children():
            child.destroy()

        self._setup_button_content()

        if self.tooltip_text:
            self.set_tooltip_text(self.tooltip_text)
