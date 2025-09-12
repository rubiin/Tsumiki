from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class OverviewButtonWidget(ButtonWidget):
    """A widget to show the overview of all workspaces and windows."""

    def __init__(self, **kwargs):
        super().__init__(name="overview_button", **kwargs)

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Overview")

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰕸"),
            props={"style_classes": "panel-font-icon"},
        )

        if self.config.get("label", True):
            self.container_box.add(Label(label="overview", style_classes="panel-text"))

        # Lazy-init overview popup
        self._overview_popup = None
        self.connect("clicked", self.on_click)

    def on_click(self, *_):
        from modules.overview import OverViewOverlay
        from utils.config import widget_config

        if self._overview_popup is None:
            self._overview_popup = OverViewOverlay(widget_config)
        self._overview_popup.toggle_popup()
