from typing import ClassVar, Literal

import gi
from fabric.utils import bulk_connect, cooldown, remove_handler
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
from utils.widget_settings import BarConfig
from utils.widget_utils import (
    create_scale,
    get_audio_icon_name,
    get_brightness_icon_name,
)

gi.require_versions({"GObject": "2.0"})


class GenericOSDContainer(Box, BaseWidget):
    """A generic OSD container to display the OSD for brightness and audio."""

    def __init__(self, config: dict, **kwargs):
        is_vertical = config.get("orientation", "horizontal") == "vertical"

        super().__init__(
            orientation=config.get("orientation", "horizontal"),
            spacing=10,
            name="osd-container",
            style_classes=["vertical"] if is_vertical else [],
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
            orientation=config.get("orientation", "horizontal"),
            h_expand=is_vertical,
            v_expand=is_vertical,
            duration=0.8,
            curve=(0.34, 1.56, 0.64, 1.0),
            inverted=is_vertical,
            style=scale_style,
        )

        self.children = (self.icon, self.scale)

        self.show_level = config.get("percentage", True)

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

    def __init__(self, config: dict, **kwargs):
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

    def __init__(self, config: dict, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service

        self.previous_volume = None
        self.previous_muted = None

        self.config = config

        bulk_connect(
            self.audio_service,
            {
                "notify::speaker": self.on_speaker_changed,
                "changed": self.check_mute,
            },
        )

    @cooldown(0.1)
    def check_mute(self, *_):
        if not self.audio_service.speaker:
            return

        current_muted = self.audio_service.speaker.muted
        if self.previous_muted is None or current_muted != self.previous_muted:
            self.previous_muted = current_muted
            self.update_icon()
            self.scale.add_style_class("muted")
            self.emit("volume-changed")

    def on_speaker_changed(self, *_):
        if speaker := self.audio_service.speaker:
            speaker.connect("notify::volume", self.update_volume)

    @cooldown(0.1)
    def update_volume(self, speaker, *_):
        if not self.audio_service.speaker:
            return

        speaker.handler_block_by_func(self.update_volume)
        volume = round(self.audio_service.speaker.volume)

        if self.previous_volume is None or volume != self.previous_volume:
            is_over_amplified = volume > 100
            self.previous_volume = volume

            self.scale.toggle_css_class("overamplified", is_over_amplified)

            if self.audio_service.speaker.muted or volume == 0:
                self.update_icon()
            else:
                self.scale.remove_style_class("muted")
                self.update_icon(volume)
            self.update_values(volume)
            self.emit("volume-changed")

        speaker.handler_unblock_by_func(self.update_volume)

    def update_icon(self, volume=0):
        icon_name = get_audio_icon_name(volume, self.audio_service.speaker.muted)[
            "icon"
        ]
        self.icon.set_from_icon_name(icon_name, self.icon_size)


class MicrophoneOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for microphone."""

    __gsignals__: ClassVar = {"mic-changed": (GObject.SignalFlags.RUN_FIRST, None, ())}

    def __init__(self, config: dict, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service

        self.previous_volume = None
        self.previous_muted = None

        self.config = config

        bulk_connect(
            self.audio_service,
            {
                "notify::microphone": self.on_microphone_changed,
                "changed": self.check_mute,
            },
        )

    @cooldown(0.1)
    def check_mute(self, *_):
        if not self.audio_service.microphone:
            return

        current_muted = self.audio_service.microphone.muted
        if self.previous_muted is None or current_muted != self.previous_muted:
            self.previous_muted = current_muted
            self.update_icon()
            self.scale.add_style_class("muted")
            self.emit("mic-changed")

    def on_microphone_changed(self, *_):
        if microphone := self.audio_service.microphone:
            microphone.connect("notify::volume", self.update_volume)

    @cooldown(0.1)
    def update_volume(self, *_):
        if not self.audio_service.microphone:
            return

        volume = round(self.audio_service.microphone.volume)

        if self.previous_volume is None or volume != self.previous_volume:
            is_over_amplified = volume > 100
            self.previous_volume = volume

            self.scale.toggle_css_class("overamplified", is_over_amplified)

            if self.audio_service.microphone.muted or volume == 0:
                self.update_icon()
            else:
                self.scale.remove_style_class("muted")
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


class OSDContainer(Window):
    """A widget to display the OSD for audio and brightness."""

    def __init__(
        self,
        config: BarConfig,
        keyboard_mode: Keyboard_Mode = "none",
        **kwargs,
    ):
        self.hide_timer_id = None
        self.config = config.get("modules", {}).get("osd", {})

        osds = self.config.get("osds", ["brightness", "volume"])

        if "volume" in osds:
            self.audio_container = AudioOSDContainer(config=self.config)
            self.audio_container.connect("volume-changed", self.show_audio)
        if "brightness" in osds:
            self.brightness_container = BrightnessOSDContainer(config=self.config)
            self.brightness_container.connect(
                "brightness-changed", self.show_brightness
            )
        if "microphone" in osds:
            self.microphone_container = MicrophoneOSDContainer(config=self.config)
            self.microphone_container.connect("mic-changed", self.show_microphone)

        self.timeout = self.config.get("timeout", 3000)

        self.revealer = Revealer(
            name="osd-revealer",
            transition_type=self.config.get("transition_type", "slide-up"),
            transition_duration=self.config.get("transition_duration", 500),
            child_revealed=False,
        )

        super().__init__(
            layer="overlay",
            anchor=self.config.get("anchor", "center"),
            child=self.revealer,
            visible=False,
            pass_through=True,
            keyboard_mode=keyboard_mode,
            name="osd",
            title="tsumiki",
            **kwargs,
        )

    def show_audio(self, *_):
        self.show_box(box_to_show="audio")

    def show_brightness(self, *_):
        self.show_box(box_to_show="brightness")

    def show_microphone(self, *_):
        self.show_box(box_to_show="microphone")

    def show_box(
        self, box_to_show: Literal["audio", "brightness", "microphone"]
    ):
        if box_to_show == "audio":
            child_to_show = self.audio_container
        elif box_to_show == "brightness":
            child_to_show = self.brightness_container
        else:
            child_to_show = self.microphone_container

        if self.revealer.get_child() != child_to_show:
            if self.revealer.get_child():
                self.revealer.remove(self.revealer.get_child())
            self.revealer.add(child_to_show)

        # First make the window visible
        self.set_visible(True)

        # Reset hide timer
        if self.hide_timer_id is not None:
            remove_handler(self.hide_timer_id)
            self.hide_timer_id = None

        # Delay reveal to ensure animation plays
        GLib.idle_add(lambda: self.revealer.set_reveal_child(True))

        self.hide_timer_id = GLib.timeout_add(self.timeout, self._hide)

    def _hide(self):
        self.revealer.set_reveal_child(False)  # Trigger hide animation

        # Wait for the animation to finish before hiding the window completely
        GLib.timeout_add(self.revealer.get_transition_duration(), self._finalize_hide)
        return False

    def _finalize_hide(self):
        self.set_visible(False)
        self.hide_timer_id = None
        return False
