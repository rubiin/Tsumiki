from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.popover import Popover
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


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
        self.connect("clicked", self._on_toggle_clicked)

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
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(icon)

        if self.show_label:
            label = Label(
                label=self.label_text,
                style_classes="panel-text"
            )
            self.box.add(label)

    def _setup_popup(self):
        """Set up the popup that contains the grouped widgets."""
        # Fix: Read spacing and style_classes directly from config
        self.widgets_box = Box(
            orientation="h",
            spacing=self.config.get("spacing", 4),
            style_classes=[
                "panel-collapsible-group",
                *self.config.get("style_classes", [])
            ]
        )

        self._populate_widgets()

        self.popup = Popover(
            content=self.widgets_box,
            point_to=self
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
        self.set_has_class("active", self.is_expanded)

    def _on_toggle_clicked(self, button):
        """Handle the toggle button click."""
        self._set_expanded(not self.is_expanded)

    def _populate_widgets(self):
        """Populate the widgets box with configured widgets."""
        if not self.widgets_list or not hasattr(self, 'widgets_box'):
            return

        # Fix: Properly destroy child widgets to prevent memory leaks
        for child in self.widgets_box.get_children():
            child.destroy()

        for widget_name in self.widgets_config:
            if widget_name in self.widgets_list:
                widget_class = self.widgets_list[widget_name]
                try:
                    widget_instance = widget_class()
                    self.widgets_box.add(widget_instance)
                except Exception as e:
                    print(f"Failed to create widget {widget_name}: {e}")
                    continue

    def set_widgets(self, widgets_list):
        """Set the widgets to be displayed in the collapsible group.

        Args:
            widgets_list: Dictionary mapping widget names to widget classes
        """
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
        for child in self.box.get_children():
            child.destroy()

        self._setup_button_content()

        if self.tooltip_text:
            self.set_tooltip_text(self.tooltip_text)
