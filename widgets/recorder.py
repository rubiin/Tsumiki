from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.image import Image

from services import ScreenRecorder
from shared import ButtonWidget, LottieAnimation, LottieAnimationWidget
from utils import BarConfig, ExecutableNotFoundError, icons
from utils.functions import executable_exists


class RecorderWidget(ButtonWidget):
    """A widget to record the system"""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="recorder", **kwargs)

        self.is_recording = False
        self.config = widget_config["recorder"]

        if not executable_exists("wf-recorder"):
            raise ExecutableNotFoundError("wf-recorder")

        self.weather_lottie_dir = get_relative_path("../assets/icons/lottie")

        self.recording_ongoing_lottie = LottieAnimationWidget(
            LottieAnimation.from_file(
                f"{self.weather_lottie_dir}/recording.json",
            ),
            scale=0.40,
            h_align=True,
        )

        self.recording_idle_image = Image(
            icon_name=icons.icons["recorder"]["stopped"],
            icon_size=self.config["icon_size"],
            h_align=True,
        )

        self.box = Box(children=(self.recording_idle_image,))

        self.add(self.box)

        if self.config["tooltip"]:
            self.set_tooltip_text("Recording stopped")

        recorder_service = ScreenRecorder(widget_config)

        recorder_service.connect("recording", self.update_ui)

        self.connect(
            "clicked",
            lambda _: recorder_service.screencast_stop()
            if self.is_recording
            else recorder_service.screencast_start(),
        )

    def update_ui(self, _, is_recording: bool):
        if is_recording:
            self.is_recording = True
            self.box.children = (self.recording_ongoing_lottie,)
            self.recording_ongoing_lottie.play_loop()
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording started")
        else:
            self.box.children = self.recording_idle_image
            self.recording_ongoing_lottie.stop_play()
            self.is_recording = False
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording stopped")
