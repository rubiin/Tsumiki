from fabric.utils import get_relative_path

from services import ScreenRecorderService
from shared.lottie import LottieAnimation, LottieAnimationWidget
from shared.widget_container import ButtonWidget
from utils.functions import check_executable_exists
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


class RecorderWidget(ButtonWidget):
    """A widget to record the system"""

    def __init__(self, **kwargs):
        super().__init__(name="recorder", **kwargs)

        check_executable_exists("wf-recorder")

        # Initial UI setup
        self.recording_idle_image = nerd_font_icon(
            icon=text_icons["recorder"],
            props={"style_classes": "panel-font-icon"},
        )
        self.box.add(self.recording_idle_image)

        if self.config.get("tooltip"):
            self.set_tooltip_text("Recording stopped")

        self.recorder_service = ScreenRecorderService()
        self.recorder_service.connect("recording", self.update_ui)

        self.connect("clicked", self.handle_click)

        # Internal state
        self._recording_lottie = None

    @property
    def recording_ongoing_lottie(self):
        if self._recording_lottie is None:
            self._recording_lottie = LottieAnimationWidget(
                LottieAnimation.from_file(
                    f"{get_relative_path('../assets/icons/')}/recording.json",
                ),
                scale=0.30,
                h_align="center",
                v_align="center",
            )
        return self._recording_lottie

    def handle_click(self, *_):
        """Start or stop recording the screen."""
        if self.recorder_service.is_recording:
            self.recorder_service.screenrecord_stop()
        else:
            self.recorder_service.screenrecord_start(
                path=self.config["path"], allow_audio=self.config["audio"]
            )

    def update_ui(self, _, is_recording: bool):
        current_children = self.box.get_children()

        if is_recording:
            if self.recording_idle_image in current_children:
                self.box.remove(self.recording_idle_image)
                self.box.add(self.recording_ongoing_lottie)

            self.recording_ongoing_lottie.play_loop()

            if self.config.get("tooltip"):
                self.set_tooltip_text("Recording started")
        else:
            if (
                self._recording_lottie
                and self.recording_ongoing_lottie in current_children
            ):
                self.box.remove(self.recording_ongoing_lottie)
                self.box.add(self.recording_idle_image)

                self.recording_ongoing_lottie.stop_play()

            if self.config.get("tooltip"):
                self.set_tooltip_text("Recording stopped")
