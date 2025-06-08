from fabric.utils import cooldown
from fabric.widgets.box import Box

from services import audio_service
from shared.setting_scale import SettingSlider
from shared.widget_container import HoverButton
from utils.functions import set_scale_adjustment
from utils.icons import symbolic_icons
from utils.widget_utils import text_icon


class MicrophoneSlider(SettingSlider):
    """A widget to display a scale for audio settings."""

    def __init__(self, audio_stream=None, show_chevron=True):
        self.client = audio_service
        self.audio_stream = audio_stream

        self.pixel_size = 16

        super().__init__(
            icon_name=symbolic_icons["audio"]["mic"]["medium"],
            start_value=0,
            pixel_size=self.pixel_size,
        )

        if show_chevron:
            self.chevron_icon = text_icon(icon="", props={"style": "font-size:12px;"})
            self.chevron_btn = HoverButton(
                child=Box(
                    children=(self.chevron_icon,),
                )
            )
            self.chevron_btn.connect("clicked", self.on_button_click)
            self.children = (*self.children, self.chevron_btn)

        if not audio_stream:

            def init_device_audio(*args):
                if not self.client.microphone:
                    return
                self.audio_stream = self.client.speaker
                self.update_state()
                self.client.disconnect_by_func(init_device_audio)
                self.client.connect("microphone-changed", self.update_state)

            self.client.connect("changed", init_device_audio)
            if self.client.speaker:
                init_device_audio()
        else:
            self.update_state()
            self.audio_stream.connect("changed", self.update_state)

        self.scale.connect("change-value", self.on_scale_move)
        self.icon_button.connect("clicked", self.on_mute_click)

    @cooldown(0.1)
    def on_scale_move(self, _, __, moved_pos):
        self.client.microphone.volume = moved_pos

    def update_state(self, *args):
        """Update the slider state from the audio stream."""
        if not self.audio_stream:
            return

        self.scale.set_sensitive(not self.audio_stream.muted)
        set_scale_adjustment(self.scale, 0, 100, 1)
        self.scale.set_value(self.audio_stream.volume)
        self.scale.set_tooltip_text(f"{round(self.audio_stream.volume)}%")
        self.icon.set_from_icon_name(self._get_icon_name(), self.pixel_size)

    def _get_icon_name(self):
        """Get the appropriate icon name based on mute state."""
        if not self.audio_stream:
            return symbolic_icons["audio"]["mic"]["high"]
        return symbolic_icons["audio"]["mic"][
            "muted" if self.audio_stream.muted else "high"
        ]

    def on_button_click(self, *_):
        parent = self.get_parent()
        while parent and not hasattr(parent, "mic_submenu"):
            parent = parent.get_parent()

        if parent and hasattr(parent, "mic_submenu"):
            is_visible = parent.mic_submenu.toggle_reveal()

            self.chevron_icon.set_label("" if is_visible else "")

    def on_mute_click(self, *_):
        if self.audio_stream:
            self.client.microphone.muted = not self.client.microphone.muted
