from fabric.utils import get_relative_path
from fabric.widgets.image import Image

from services import ScreenRecorderService
from shared.lottie import LottieAnimation, LottieAnimationWidget
from shared.widget_container import ButtonWidget
from utils.functions import check_executable_exists
from utils.icons import symbolic_icons


class RecorderWidget(ButtonWidget):
    """A widget to record the system"""

    def __init__(self, **kwargs):
        super().__init__(name="recorder", **kwargs)

        check_executable_exists("wf-recorder")

        self.recording_ongoing_lottie = LottieAnimationWidget(
            LottieAnimation.from_file(
                f"{get_relative_path('../assets/icons/')}/recording.json",
            ),
            scale=0.40,
            h_align=True,
        )

        self.recording_idle_image = Image(
            icon_name=symbolic_icons["recorder"]["stopped"],
            icon_size=self.config["icon_size"],
            h_align=True,
        )

        self.box.add(
            self.recording_idle_image,
        )

        if self.config["tooltip"]:
            self.set_tooltip_text("Recording stopped")

        self.recorder_service = ScreenRecorderService()

        self.recorder_service.connect("recording", self.update_ui)

        self.connect(
            "clicked",
            self.handle_click,
        )

    # record or stop on click
    def handle_click(self, *_):
        """Start or stop recording the screen."""
        if self.recorder_service.is_recording:
            self.recorder_service.screenrecord_stop()
        else:
            self.recorder_service.screenrecord_start(
                path=self.config["path"], allow_audio=self.config["audio"]
            )

    def update_ui(self, _, is_recording: bool):
        if is_recording:
            self.box.children = (self.recording_ongoing_lottie,)
            self.recording_ongoing_lottie.play_loop()
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording started")
        else:
            self.box.children = self.recording_idle_image
            self.recording_ongoing_lottie.stop_play()
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording stopped")
