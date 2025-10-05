from fabric.utils import cooldown
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

from services import audio_service
from shared.widget_container import EventBoxWidget
from utils.icons import text_icons
from utils.widget_utils import get_audio_icon_name, nerd_font_icon


class VolumeWidget(EventBoxWidget):
    """a widget that displays and controls the volume."""

    def __init__(self, **kwargs):
        super().__init__(
            name="volume",
            events=["scroll", "smooth-scroll", "enter-notify-event"],
            **kwargs,
        )

        # Initialize the audio service
        self.audio = audio_service

        # Create a circular progress bar to display the volume level
        self.progress_bar = CircularProgressBar(
            style_classes="overlay-progress-bar",
            pie=True,
            size=24,
        )

        self.icon = nerd_font_icon(
            icon=text_icons["volume"]["medium"],
            props={
                "style_classes": ["panel-font-icon", "overlay-icon"],
            },
        )

        # Create an event box to handle scroll events for volume control
        self.box.add(
            Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
        )

        # Connect the audio service to update the progress bar on volume change
        self.audio.connect("notify::speaker", self.on_speaker_changed)

        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

        if self.config.get("label", True):
            self.volume_label = Label(style_classes=["panel-text"])
            self.box.add(self.volume_label)

    @cooldown(0.1)
    def on_scroll(self, _, event):
        # Adjust the volume based on the scroll direction
        val_y = event.delta_y

        if val_y > 0:
            self.audio.speaker.volume += self.config.get("step_size", 5)
        else:
            self.audio.speaker.volume -= self.config.get("step_size", 5)

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio.speaker:
            return

        if self.config.get("tooltip", False):
            self.set_tooltip_text(self.audio.speaker.description)

        self.audio.speaker.connect("notify::volume", self.update_volume)
        self.update_volume()

    # Mute and unmute the speaker
    def toggle_mute(self):
        current_stream = self.audio.speaker
        if current_stream:
            current_stream.muted = not current_stream.muted
            self.icon.set_text(
                text_icons["volume"]["muted"]
            ) if current_stream.muted else self.update_volume()

    def update_volume(self, *_):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)
            self.progress_bar.set_value(volume / 100)

            if self.config.get("label", True):
                self.volume_label.set_text(f"{volume}%")

        self.icon.set_text(
            get_audio_icon_name(volume, self.audio.speaker.muted)["icon_text"]
        )
