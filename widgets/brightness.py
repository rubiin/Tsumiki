from fabric.utils import cooldown
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

import utils.functions as helpers
from services.brightness import BrightnessService
from shared.widget_container import EventBoxWidget
from utils.icons import text_icons
from utils.widget_utils import get_brightness_icon_name, nerd_font_icon


class BrightnessWidget(EventBoxWidget):
    """a widget that displays and controls the brightness."""

    def __init__(self, **kwargs):
        super().__init__(
            name="brightness",
            events=["scroll", "smooth-scroll"],
            **kwargs,
        )

        # Initialize the audio service
        self.brightness_service = BrightnessService()

        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )

        # Create a circular progress bar to display the brightness level
        self.progress_bar = CircularProgressBar(
            style_classes="overlay-progress-bar",
            pie=True,
            size=24,
            value=normalized_brightness / 100,
        )

        self.icon = nerd_font_icon(
            icon=text_icons["brightness"]["medium"],
            props={
                "style_classes": "panel-font-icon overlay-icon",
            },
        )

        # Create an event box to handle scroll events for brightness control
        self.box.add(
            Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
        )

        # Connect the audio service to update the progress bar on brightness change
        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

        if self.config["label"]:
            self.brightness_label = Label(
                label=f"{normalized_brightness}%",
                style_classes="panel-text",
            )
            self.box.add(self.brightness_label)

    @cooldown(1)
    def on_scroll(self, _, event):
        # Adjust the brightness based on the scroll direction
        val_y = event.delta_y

        if val_y > 0:
            self.brightness_service.screen_brightness += self.config["step_size"]
        else:
            self.brightness_service.screen_brightness -= self.config["step_size"]

    def on_brightness_changed(self, *_):
        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )
        self.progress_bar.set_value(normalized_brightness / 100)

        if self.config["label"]:
            self.brightness_label.set_text(f"{normalized_brightness}%")

        self.icon.set_text(get_brightness_icon_name(normalized_brightness)["icon_text"])

        if self.config["tooltip"]:
            self.set_tooltip_text(f"{normalized_brightness}%")
