
from services import audio_service
from shared.setting_scale import SettingSlider
from utils.icons import icons


class AudioSlider(SettingSlider):
    """A widget to display a scale for audio settings.

    Can be used for both device audio and application audio control.
    """

    def __init__(self, audio_stream=None):
        """Initialize the audio slider.

        Args:
            audio_stream: Optional AudioStream object. If None, controls device audio.
                        If provided, controls application-specific audio.
        """
        self.client = audio_service
        self.audio_stream = audio_stream

        # Initialize with default values first
        super().__init__(
            icon_name=icons["audio"]["volume"]["high"],
            start_value=0
        )

        if not audio_stream:
            def init_device_audio(*args):
                if not self.client.speaker:
                    return
                self.audio_stream = self.client.speaker
                self.update_state()
                self.client.disconnect_by_func(init_device_audio)
                self.client.connect("speaker-changed", self.on_audio_change)

            self.client.connect("changed", init_device_audio)
            if self.client.speaker:
                init_device_audio()
        else:
            self.update_state()
            self.audio_stream.connect("changed", self.on_audio_change)

        # Connect signals
        self.scale.connect("change-value", self.on_scale_move)
        if not audio_stream:
            self.icon_button.connect("button-press-event", self.on_button_click)
        else:
            self.icon_button.connect("clicked", self.on_mute_click)

    def _get_icon_name(self):
        """Get the appropriate icon name based on mute state."""
        if not self.audio_stream:
            return icons["audio"]["volume"]["high"]
        return icons["audio"]["volume"]["muted" if self.audio_stream.muted else "high"]

    def update_state(self):
        """Update the slider state from the audio stream."""
        if not self.audio_stream:
            return

        self.scale.set_sensitive(not self.audio_stream.muted)
        self.scale.set_value(self.audio_stream.volume)
        self.scale.set_tooltip_text(f"{round(self.audio_stream.volume)}%")
        self.icon.set_from_icon_name(self._get_icon_name(), 20)

    def on_scale_move(self, _, __, moved_pos):
        """Handle volume slider changes."""
        if self.audio_stream:
            self.audio_stream.volume = moved_pos

    def on_audio_change(self, *args):
        """Update slider state when audio changes."""
        self.update_state()

    def on_button_click(self, button, event):
        """Handle button clicks on the icon button."""
        if event.button == 3:  # Right click
            # Find and toggle the AudioSubMenu
            parent = self.get_parent()
            while parent and not hasattr(parent, "audio_submenu"):
                parent = parent.get_parent()

            if parent and hasattr(parent, "audio_submenu"):
                parent.audio_submenu.toggle_reveal()
        else:  # Left click
            self.on_mute_click(button)

    def on_mute_click(self, button):
        """Toggle mute state."""
        if self.audio_stream:
            self.audio_stream.muted = not self.audio_stream.muted
