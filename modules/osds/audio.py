from typing import ClassVar

from fabric.utils import GObject, bulk_connect, cooldown

from services import audio_service
from utils.widget_utils import (
    get_audio_icon_name,
)

from ..osd import GenericOSDContainer


class AudioOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for audio."""

    __gsignals__: ClassVar = {
        "volume-changed": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config: dict, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service
        self._speaker = None
        self._speaker_handler_id: int | None = None

        self.previous_volume = None
        self.previous_muted = None
        self._effective_muted = None

        self.config = config

        bulk_connect(
            self.audio_service,
            {
                "notify::speaker": self.on_speaker_changed,
                "changed": self.check_mute,
            },
        )
        self.on_speaker_changed()

    @cooldown(0.1)
    def check_mute(self, *_):
        speaker = self.audio_service.speaker
        if not speaker:
            return

        current_muted = speaker.muted
        if self.previous_muted is None or current_muted != self.previous_muted:
            self.previous_muted = current_muted
            self.update_icon()
            self.scale.toggle_css_class("muted", current_muted)
            self.emit("volume-changed")

    def on_speaker_changed(self, *_):
        if self._speaker and self._speaker_handler_id is not None:
            self._speaker.disconnect(self._speaker_handler_id)

        self._speaker_handler_id = None
        self.previous_volume = None
        self.previous_muted = None
        self._effective_muted = None
        self._speaker = self.audio_service.speaker

        if self._speaker:
            self._speaker_handler_id = self._speaker.connect(
                "notify::volume", self.update_volume
            )
            self.update_volume(self._speaker)

    @cooldown(0.1)
    def update_volume(self, *_):
        speaker = self.audio_service.speaker
        if not speaker:
            return

        volume = round(speaker.volume)
        current_muted = speaker.muted
        volume_changed = self.previous_volume is None or volume != self.previous_volume
        muted_changed = (
            self.previous_muted is None or current_muted != self.previous_muted
        )

        if volume_changed or muted_changed:
            self.previous_volume = volume
            self.previous_muted = current_muted

            is_muted = speaker.muted or volume == 0

            self.scale.toggle_css_class("overamplified", volume > 100)

            if self._effective_muted is None or is_muted != self._effective_muted:
                self._effective_muted = is_muted
                self.scale.toggle_css_class("muted", is_muted)

            if is_muted:
                self.update_icon()
            else:
                self.update_icon(volume)

            self.update_values(volume)
            self.emit("volume-changed")

    def update_icon(self, volume=0):
        icon_name = get_audio_icon_name(volume, self.audio_service.speaker.muted)[
            "icon"
        ]
        self.icon.set_from_icon_name(icon_name, self.icon_size)
