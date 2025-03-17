from services import audio_service
from shared import SettingSlider
from utils.icons import icons


class MicrophoneSlider(SettingSlider):
    """A widget to display a scale for audio settings."""

    def __init__(self):
        self.client = audio_service

        super().__init__(icon_name=icons["audio"]["mic"]["medium"])

        self.scale.connect("change-value", self.on_scale_move)
        self.client.connect("microphone-changed", self.on_microphone_change)
        self.icon_button.connect("clicked", self.on_button_click)

    def on_scale_move(self, _, __, moved_pos):
        self.client.microphone.volume = moved_pos

    def on_microphone_change(self, *args):
        self.scale.set_sensitive(not audio_service.microphone.muted)
        self.scale.set_value(audio_service.microphone.volume)
        self.scale.set_tooltip_text(f"{round(audio_service.microphone.volume)}%")

    def on_button_click(self, *_):
        self.client.microphone.muted = not self.client.microphone.muted
        self.icon.set_from_icon_name(
            icons["audio"]["mic"]["muted"], 20
        ) if self.client.microphone.muted else self.icon.set_from_icon_name(
            icons["audio"]["mic"]["medium"], 20
        )
