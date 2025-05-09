from fabric.widgets.label import Label

from services.screen_record import ScreenRecorder
from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


class ScreenShotWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config["screen_shot"], name="screen_shot", **kwargs)

        if self.config["tooltip"]:
            self.set_tooltip_text("Screen Shot")

        recorder_service = ScreenRecorder()

        self.submap_label = Label(label="0", style_classes="panel-text")

        self.children = text_icon(
            self.config["icon"],
            props={"style_classes": "panel-icon"},
        )

        self.connect(
            "clicked", lambda _: recorder_service.screenshot(path=self.config["path"])
        )
