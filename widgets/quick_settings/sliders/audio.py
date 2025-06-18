from fabric.utils import cooldown
from fabric.widgets.box import Box

from services import audio_service
from shared.buttons import HoverButton
from shared.setting_scale import SettingSlider
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


class AudioSlider(SettingSlider):
    """A widget to display a scale for audio settings.

    Can be used for both device audio and application audio control.
    """

    def __init__(self, audio_stream=None, show_chevron=True):
        """Initialize the audio slider.

        Args:
            audio_stream: Optional AudioStream object. If None, controls device audio.
                        If provided, controls application-specific audio.
        """
        self.client = audio_service
        self.audio_stream = audio_stream

        self.pixel_size = 20

        # Initialize with default values first
        super().__init__(
            icon_name=text_icons["volume"]["high"],
            start_value=0,
            pixel_size=self.pixel_size,
        )

        if show_chevron:
            self.chevron_icon = nerd_font_icon(
                icon="", props={"style": "font-size:12px;"}
            )

            self.chevron_btn = HoverButton(
                child=Box(
                    children=(self.chevron_icon,),
                )
            )
            self.chevron_btn.connect("clicked", self.on_button_click)
            self.children = (*self.children, self.chevron_btn)

        if not audio_stream:

            def init_device_audio(*args):
                if not self.client.speaker:
                    return
                self.audio_stream = self.client.speaker
                self.update_state()
                self.client.disconnect_by_func(init_device_audio)
                self.client.connect("speaker-changed", self.update_state)

            self.client.connect("changed", init_device_audio)
            if self.client.speaker:
                init_device_audio()
        else:
            self.update_state()
            self.audio_stream.connect("changed", self.update_state)

        # Connect signals
        self.scale.connect("change-value", self.on_scale_move)

        self.icon_button.connect("clicked", self.on_mute_click)

    def _get_icon_name(self):
        """Get the appropriate icon name based on mute state."""
        if not self.audio_stream:
            return text_icons["volume"]["high"]
        return text_icons["volume"]["muted" if self.audio_stream.muted else "high"]

    def update_state(self, *args):
        """Update the slider state from the audio stream."""
        if not self.audio_stream:
            return

        volume = int(self.audio_stream.volume)

        self.scale.set_sensitive(not self.audio_stream.muted)

        # Avoid unnecessary updates if the value hasn't changed
        if (volume) == round(self.scale.get_value()):
            return

        self.scale.set_value(volume)
        self.scale.set_tooltip_text(f"{volume}%")
        self.icon.set_label(self._get_icon_name())

    @cooldown(0.1)
    def on_scale_move(self, _, __, moved_pos):
        """Handle volume slider changes."""
        if self.audio_stream:
            self.audio_stream.volume = moved_pos

    def on_button_click(self, *_):
        parent = self.get_parent()
        while parent and not hasattr(parent, "audio_submenu"):
            parent = parent.get_parent()

        if parent and hasattr(parent, "audio_submenu"):
            is_visible = parent.audio_submenu.toggle_reveal()

            self.chevron_icon.set_label("" if is_visible else "")

    def on_mute_click(self, *_):
        """Toggle mute state."""
        if self.audio_stream:
            self.audio_stream.muted = not self.audio_stream.muted
