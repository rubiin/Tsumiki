from typing import ClassVar

from fabric.utils import GObject, bulk_connect, cooldown

from services import audio_service
from utils.icons import symbolic_icons

from ..osd import GenericOSDContainer


class MicrophoneOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for microphone."""

    __gsignals__: ClassVar = {"mic-changed": (GObject.SignalFlags.RUN_FIRST, None, ())}

    def __init__(self, config: dict, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service
        self._microphone = None
        self._microphone_handler_id: int | None = None

        self.previous_volume = None
        self.previous_muted = None
        self._effective_muted = None

        self.config = config

        bulk_connect(
            self.audio_service,
            {
                "notify::microphone": self.on_microphone_changed,
                "changed": self.check_mute,
            },
        )
        self.on_microphone_changed()

    @cooldown(0.1)
    def check_mute(self, *_):
        microphone = self.audio_service.microphone
        if not microphone:
            return

        current_muted = microphone.muted
        if self.previous_muted is None or current_muted != self.previous_muted:
            self.previous_muted = current_muted
            self.update_icon()
            self.scale.toggle_css_class("muted", current_muted)
            self.emit("mic-changed")

    def on_microphone_changed(self, *_):
        if self._microphone and self._microphone_handler_id is not None:
            self._microphone.disconnect(self._microphone_handler_id)

        self._microphone_handler_id = None
        self.previous_volume = None
        self.previous_muted = None
        self._effective_muted = None
        self._microphone = self.audio_service.microphone

        if self._microphone:
            self._microphone_handler_id = self._microphone.connect(
                "notify::volume", self.update_volume
            )
            self.update_volume()

    @cooldown(0.1)
    def update_volume(self, *_):
        microphone = self.audio_service.microphone
        if not microphone:
            return

        volume = round(microphone.volume)
        current_muted = microphone.muted
        volume_changed = self.previous_volume is None or volume != self.previous_volume
        muted_changed = (
            self.previous_muted is None or current_muted != self.previous_muted
        )

        if volume_changed or muted_changed:
            self.previous_volume = volume
            self.previous_muted = current_muted

            is_muted = microphone.muted or volume == 0

            self.scale.toggle_css_class("overamplified", volume > 100)

            if self._effective_muted is None or is_muted != self._effective_muted:
                self._effective_muted = is_muted
                self.scale.toggle_css_class("muted", is_muted)

            if is_muted:
                self.update_icon()
            else:
                self.update_icon(volume)

            self.update_values(volume)
            self.emit("mic-changed")

    def update_icon(self, volume=0):
        icon_name = (
            symbolic_icons["audio"]["mic"]["muted"]
            if volume == 0 or self.audio_service.microphone.muted
            else symbolic_icons["audio"]["mic"]["high"]
        )
        self.icon.set_from_icon_name(icon_name, self.icon_size)
