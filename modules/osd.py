from typing import ClassVar, Literal

from fabric.utils import bulk_connect, cooldown
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GLib, GObject

from services import audio_service
from services.brightness import BrightnessService
from shared.widget_container import BaseWidget
from utils.icons import symbolic_icons
from utils.types import Keyboard_Mode
from utils.widget_utils import (
    create_scale,
    get_audio_icon_name,
    get_brightness_icon_name,
)


class GenericOSDContainer(Box, BaseWidget):
    """A generic OSD container to display the OSD for brightness and audio."""

    def __init__(self, config, **kwargs):
        is_vertical = config["orientation"] == "vertical"

        super().__init__(
            orientation=config["orientation"],
            spacing=10,
            name="osd-container",
            style_classes="vertical" if is_vertical else "",
            **kwargs,
        )

        self.icon_size = config.get("icon_size", 28)

        self.icon = Image(
            icon_name=symbolic_icons["brightness"]["screen"],
            icon_size=self.icon_size,
        )

        scale_style = (
            "scale {min-height: 150px; min-width: 11px;}" if is_vertical else ""
        )

        self.scale = create_scale(
            name="osd-scale",
            orientation=config["orientation"],
            h_expand=is_vertical,
            v_expand=is_vertical,
            duration=0.8,
            curve=(0.25, 0.1, 0.25, 1.0),
            inverted=is_vertical,
            style=scale_style,
        )

        self.children = (self.icon, self.scale)

        self.show_level = config["percentage"]

        if self.show_level:
            self.level = Label(name="osd-level", h_align="center", h_expand=True)
            self.add(self.level)

    def update_values(self, value):
        """Update the value."""
        round_value = round(value)
        self.scale.set_value(round_value)

        if self.show_level:
            self.level.set_label(f"{round_value}%")


class BrightnessOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for brightness."""

    __gsignals__: ClassVar = {
        "brightness-changed": (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.brightness_service = BrightnessService()
        self.config = config

        self.update_brightness()
        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

    @cooldown(0.1)
    def update_brightness(self):
        brightness_percent = self.brightness_service.screen_brightness_percentage
        self.update_values(brightness_percent)
        self.update_icon(int(brightness_percent))

    def update_icon(self, current_brightness: int):
        icon_name = get_brightness_icon_name(current_brightness)["icon"]
        self.icon.set_from_icon_name(icon_name, self.icon_size)

    def on_brightness_changed(self, *_):
        self.update_brightness()
        self.emit("brightness-changed", 0)


class AudioOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for audio."""

    __gsignals__: ClassVar = {
        "volume-changed": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service

        self.config = config

        bulk_connect(
            self.audio_service,
            {
                "notify::speaker": self.on_speaker_changed,
                "changed": self.check_mute,
            },
        )

    @cooldown(0.1)
    def check_mute(self, audio):
        if not audio.speaker:
            return
        if audio.speaker.muted:
            self.update_icon()
            self.emit("volume-changed")
        else:
            self.update_icon(round(self.audio_service.speaker.volume))

    def on_speaker_changed(self, *_):
        if speaker := self.audio_service.speaker:
            speaker.connect("notify::volume", self.update_volume)

    @cooldown(0.1)
    def update_volume(self, speaker, *_):
        self.emit("volume-changed")
        volume = round(self.audio_service.speaker.volume)

        is_over_amplified = volume > 100

        self.scale.set_has_class("overamplified", is_over_amplified)

        if not self.audio_service.speaker:
            return
        if self.audio_service.speaker.muted:
            self.update_icon()
        else:
            self.update_icon(volume)
        self.update_values(volume)

    def update_icon(self, volume=0):
        icon_name = get_audio_icon_name(volume, self.audio_service.speaker.muted)[
            "icon"
        ]
        self.icon.set_from_icon_name(icon_name, self.icon_size)


class OSDContainer(Window):
    """A widget to display the OSD for audio and brightness."""

    def __init__(
        self,
        config,
        transition_duration=200,
        keyboard_mode: Keyboard_Mode = "none",
        **kwargs,
    ):
        self.config = config["modules"]["osd"]

        self.audio_container = AudioOSDContainer(config=self.config)
        self.brightness_container = BrightnessOSDContainer(config=self.config)

        self.timeout = self.config["timeout"]

        self.revealer = Revealer(
            name="osd-revealer",
            transition_type="slide-up",
            transition_duration=transition_duration,
        )

        super().__init__(
            layer="overlay",
            anchor=self.config["anchor"],
            child=self.revealer,
            visible=False,
            pass_through=True,
            keyboard_mode=keyboard_mode,
            **kwargs,
        )

        self.hide_timer_id = None
        self.suppressed: bool = False

        self.audio_container.connect("volume-changed", self.show_audio)

        self.brightness_container.connect("brightness-changed", self.show_brightness)

    def show_audio(self, *_):
        self.show_box(box_to_show="audio")

    def show_brightness(self, *_):
        self.show_box(box_to_show="brightness")

    def show_box(self, box_to_show: Literal["audio", "brightness"]):
        if self.suppressed:
            return

        child_to_show = (
            self.audio_container
            if box_to_show == "audio"
            else self.brightness_container
        )

        if self.revealer.get_child() != child_to_show:
            if self.revealer.get_child():
                self.revealer.remove(self.revealer.get_child())
            self.revealer.add(child_to_show)

        self.revealer.set_reveal_child(True)

        self.set_visible(True)

        if self.hide_timer_id is not None:
            GLib.source_remove(self.hide_timer_id)
            self.hide_timer_id = None

        self.hide_timer_id = GLib.timeout_add(self.timeout, self._hide)

    def _hide(self):
        self.set_visible(False)
        self.hide_timer_id = None
        return False
