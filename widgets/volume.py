from fabric.utils import cooldown

from services import audio_service
from shared.widget_container import EventBoxWidget
from utils.functions import safe_disconnect
from utils.icons import get_text_icon
from utils.widget_utils import create_progress, get_audio_icon_name, nerd_font_icon


class VolumeWidget(EventBoxWidget):
    """a widget that displays and controls the volume."""

    def __init__(self, **kwargs):
        super().__init__(
            name="volume",
            events=["scroll", "smooth-scroll", "enter-notify-event"],
            **kwargs,
        )
        self._speaker = None
        self._speaker_volume_handler_id = None

        # Initialize the audio service
        self.audio = audio_service

        self.icon = nerd_font_icon(
            icon=get_text_icon("volume.medium"),
            props={
                "style_classes": ["panel-font-icon", "overlay-icon"],
            },
        )

        # Create a circular progress bar to display the brightness level
        self.progress_bar = create_progress(
            child=self.icon,
            value=self.audio.speaker.volume / 100 if self.audio.speaker else 0,
        )

        # Create an event box to handle scroll events for volume control
        self.container_box.add(self.progress_bar)

        # Connect the audio service to update the progress bar on volume change
        self.audio.connect("notify::speaker", self.on_speaker_changed)

        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

    @cooldown(0.1)
    def on_scroll(self, _, event):
        # Adjust the volume based on the scroll direction
        val_y = event.delta_y
        step_size = self.config.get("step_size", 5)

        if val_y > 0:
            self.audio.speaker.volume += step_size
        else:
            self.audio.speaker.volume -= step_size

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        speaker = self.audio.speaker
        if not speaker:
            return

        if self._speaker and self._speaker_volume_handler_id is not None:
            safe_disconnect(self._speaker, self._speaker_volume_handler_id)
            self._speaker_volume_handler_id = None

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(speaker.description)

        self._speaker = speaker
        self._speaker_volume_handler_id = speaker.connect(
            "notify::volume", self.update_volume
        )
        self.update_volume()

    # Mute and unmute the speaker
    def toggle_mute(self):
        current_stream = self.audio.speaker
        if current_stream:
            current_stream.muted = not current_stream.muted
            self.icon.set_text(
                get_text_icon("volume.muted")
            ) if current_stream.muted else self.update_volume()

    def update_volume(self, *_):
        speaker = self.audio.speaker
        if not speaker:
            return

        volume = round(speaker.volume)
        nomalized_value = volume / 100
        self.progress_bar.set_value(nomalized_value)
        self.progress_bar.animate_value(nomalized_value)

        self.icon.set_text(get_audio_icon_name(volume, speaker.muted)["icon_text"])

    def destroy(self):
        if self._speaker and self._speaker_volume_handler_id is not None:
            safe_disconnect(self._speaker, self._speaker_volume_handler_id)
            self._speaker_volume_handler_id = None
        self._speaker = None
        return super().destroy()
