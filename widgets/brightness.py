from fabric.utils import cooldown

import utils.functions as helpers
from services.brightness import BrightnessService
from shared.widget_container import EventBoxWidget
from utils.icons import get_text_icon
from utils.widget_utils import create_progress, get_brightness_icon_name, nerd_font_icon


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

        self.icon = nerd_font_icon(
            icon=get_text_icon("brightness.medium"),
            props={
                "style_classes": ["panel-font-icon", "progress-bar-icon"],
            },
        )

        # Create a circular progress bar to display the brightness level
        self.progress_bar = create_progress(
            child=self.icon,
            value=normalized_brightness / 100,
        )

        # Create an event box to handle scroll events for brightness control
        self.container_box.add(self.progress_bar)

        # Connect the audio service to update the progress bar on brightness change
        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

    @cooldown(1)
    def on_scroll(self, _, event):
        # Adjust the brightness based on the scroll direction
        val_y = event.delta_y
        step_size = self.config.get("step_size", 5)

        if val_y > 0:
            self.brightness_service.screen_brightness += step_size
        else:
            self.brightness_service.screen_brightness -= step_size

    def on_brightness_changed(self, *_):
        brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )

        normalized_volume = brightness / 100
        self.progress_bar.set_value(normalized_volume)
        self.progress_bar.animate_value(normalized_volume)

        self.icon.set_text(get_brightness_icon_name(brightness)["icon_text"])

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(f"{brightness}%")
