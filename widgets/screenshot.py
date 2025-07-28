from fabric.widgets.label import Label

from services.screen_record import ScreenRecorderService
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class ScreenShotWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, **kwargs):
        super().__init__(name="screenshot", **kwargs)

        self.initialized = False

        self.recorder_service = None

        self.box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰕸"),
            props={"style_classes": "panel-font-icon"},
        )

        if self.config.get("label", True):
            self.box.add(Label(label="screenshot", style_classes="panel-text"))

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Screen Shot")

        self.connect("clicked", self.handle_click)

    def lazy_init(self, *_):
        if not self.initialized:
            self.recorder_service = ScreenRecorderService()
            self.initialized = True

    def handle_click(self, *_):
        """Start recording the screen."""
        self.lazy_init()

        if not self.initialized:
            return  # Early exit if script not available

        self.recorder_service.screenshot(
            path=self.config.get("path", ""),
            config=self.config,
        )
