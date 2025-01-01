import time
from typing import ClassVar, Literal

from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GObject

import utils.functions as helpers
import utils.icons as icons
from services import audio_service, brightness_service
from utils.monitors import HyprlandWithMonitors
from utils.widget_config import BarConfig


class BrightnessOSDContainer(Box):
    """A widget to display the OSD for brightness."""

    def __init__(self, **kwargs):
        super().__init__(orientation="h", spacing=12, name="osd-container", **kwargs)
        self.brightness_service = brightness_service
        self.level = Label(name="osd-level")
        self.icon = Image(icon_name=icons.icons["brightness"]["screen"], icon_size=28)
        self.scale = helpers.create_scale()

        self.children = (self.icon, self.scale, self.level)
        self.update_brightness()

        self.scale.connect("value-changed", lambda *_: self.update_brightness())
        self.brightness_service.connect("screen", self.on_brightness_changed)

    def update_brightness(self):
        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )
        self.scale.animate_value(normalized_brightness)
        self.update_icon(int(normalized_brightness))

    def update_icon(self, current_brightness):
        icon_name = helpers.get_brightness_icon_name(current_brightness)["icon"]
        self.level.set_label(f"{current_brightness}%")
        self.icon.set_from_icon_name(icon_name)

    def on_brightness_changed(self, sender, value, *args):
        normalized_brightness = (value / self.brightness_service.max_screen) * 101
        self.scale.animate_value(normalized_brightness)


class AudioOSDContainer(Box):
    """A widget to display the OSD for audio."""

    __gsignals__: ClassVar[dict] = {
        "volume-changed": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, **kwargs):
        super().__init__(
            orientation="h",
            spacing=13,
            name="osd-container",
            **kwargs,
        )
        self.audio = audio_service
        self.icon = Image(
            icon_name=icons.icons["audio"]["volume"]["medium"], icon_size=28
        )
        self.level = Label(name="osd-level", h_align="center", h_expand=True)
        self.scale = helpers.create_scale()

        self.hyprland_monitor = HyprlandWithMonitors()

        self.children = (self.icon, self.scale, self.level)
        self.sync_with_audio()

        self.scale.connect("value-changed", self.on_volume_changed)
        self.audio.connect("notify::speaker", self.on_audio_speaker_changed)

    def sync_with_audio(self):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)
            self.scale.set_value(volume)
            self.update_icon(volume)

    def on_volume_changed(self, *_):
        if self.audio.speaker:
            volume = self.scale.value
            if 0 <= volume <= 100:
                self.audio.speaker.set_volume(volume)
                self.update_icon(volume)
                self.emit("volume-changed")

    def on_audio_speaker_changed(self, *_):
        if self.audio.speaker:
            self.audio.speaker.connect("notify::volume", self.update_volume)
            self.update_volume()

    def update_volume(self, *_):
        if self.audio.speaker and not self.is_hovered():
            volume = round(self.audio.speaker.volume)
            self.scale.set_value(volume)
            self.update_icon(volume)

    def update_icon(self, volume):
        icon_name = helpers.get_audio_icon_name(volume, self.audio.speaker.muted)[
            "icon"
        ]
        self.level.set_label(f"{volume}%")
        self.icon.set_from_icon_name(icon_name)


class OSDContainer(Window):
    """A widget to display the OSD for audio and brightness."""

    def __init__(
        self,
        widget_config: BarConfig,
        transition_duration=100,
        keyboard_mode: Literal["none", "exclusive", "on-demand"] = "on-demand",
        **kwargs,
    ):
        self.audio_container = AudioOSDContainer()
        self.brightness_container = BrightnessOSDContainer()

        self.hyprland_monitor = HyprlandWithMonitors()

        self.config = widget_config["osd"]

        self.timeout = self.config["timeout"]

        self.revealer = Revealer(
            name="osd-revealer",
            transition_type="slide-right",
            transition_duration=transition_duration,
            child_revealed=False,
        )

        self.main_box = Box(
            orientation="v",
            spacing=13,
            children=[self.revealer],
        )

        super().__init__(
            layer="overlay",
            anchor=self.config["anchor"],
            child=self.main_box,
            visible=False,
            pass_through=True,
            keyboard_mode=keyboard_mode,
            **kwargs,
        )

        self.monitor = self.hyprland_monitor.get_current_gdk_monitor_id()

        self.last_activity_time = time.time()

        self.audio_container.audio.connect("notify::speaker", self.show_audio)
        self.brightness_container.brightness_service.connect(
            "screen",
            self.show_brightness,
        )
        self.audio_container.connect("volume-changed", self.show_audio)

        invoke_repeater(100, self.check_inactivity, initial_call=True)

    def show_audio(self, *_):
        self.show_box(box_to_show="audio")
        self.reset_inactivity_timer()

    def show_brightness(self, *_):
        self.show_box(box_to_show="brightness")
        self.reset_inactivity_timer()

    def show_box(self, box_to_show: Literal["audio", "brightness"]):
        self.set_visible(True)
        if box_to_show == "audio":
            self.revealer.children = self.audio_container
        elif box_to_show == "brightness":
            self.revealer.children = self.brightness_container
        self.revealer.set_reveal_child(True)
        self.reset_inactivity_timer()

    def start_hide_timer(self):
        self.set_visible(False)

    def reset_inactivity_timer(self):
        self.last_activity_time = time.time()

    def check_inactivity(self):
        if time.time() - self.last_activity_time >= (self.timeout / 1000):
            self.start_hide_timer()
        return True
