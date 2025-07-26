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

        self.group_config = self.config.get("group", {})
        self.widgets_config = self.config.get("widgets", [])
        self.icon_name = self.config.get("icon", "󰍽")
        self.show_icon = self.config.get("show_icon", True)
        self.show_label = self.config.get("show_label", False)
        self.label_text = self.config.get("label", "Tools")
        self.tooltip_text = self.config.get("tooltip", "Toggle tool menu")

        self.is_expanded = False
        self.popup = None
        self.widgets_list = None

        self._setup_button_content()
        self.connect("clicked", self._on_toggle_clicked)

        if self.tooltip_text:
            self.set_tooltip_text(self.tooltip_text)

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
        self.widgets_box = Box(
            orientation="h",
            spacing=self.group_config.get("spacing", 4),
            style_classes=[
                "panel-collapsible-group",
                *self.group_config.get("style_classes", [])
            ]
        )

        self._populate_widgets()

        self.popup = Popover(
            content=self.widgets_box,
            point_to=self
        )

    def _on_toggle_clicked(self, button):
        """Handle the toggle button click."""
        if self.popup is None:
            self._setup_popup()

        if self.is_expanded:
            self.popup.hide_popover()
            self.is_expanded = False
            self.set_has_class("active", False)
        else:
            self.popup.open()
            self.is_expanded = True
            self.set_has_class("active", True)

    def _populate_widgets(self):
        """Populate the widgets box with configured widgets."""
        if not self.widgets_list or not hasattr(self, 'widgets_box'):
            return

        for child in self.widgets_box.get_children():
            self.widgets_box.remove(child)

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
        if self.popup and self.is_expanded:
            self.popup.hide_popover()
            self.is_expanded = False
            self.set_has_class("active", False)

    def expand(self):
        """Expand the group programmatically."""
        if not self.is_expanded:
            if self.popup is None:
                self._setup_popup()
            self.popup.open()
            self.is_expanded = True
            self.set_has_class("active", True)
