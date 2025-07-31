from fabric.widgets.label import Label

from modules.wallpaper import WallPaperPickerOverlay
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class OverviewWidget(ButtonWidget):
    """A widget to show the overview of all workspaces and windows."""

    def __init__(self, **kwargs):
        # Initialize as a Box instead of a PopupWindow.
        super().__init__(name="overview", **kwargs)

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Overview")

        self.box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰕸"),
            props={"style_classes": "panel-font-icon"},
        )

        if self.config.get("label", True):
            self.box.add(Label(label="overview", style_classes="panel-text"))

        # Create the overview widget
        overview_popup = WallPaperPickerOverlay()
        self.connect("clicked", lambda *_: overview_popup.toggle_popup())
