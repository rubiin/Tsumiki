from fabric.utils import cooldown

from services import BrightnessService
from shared.setting_scale import SettingSlider
from utils.functions import set_scale_adjustment
from utils.icons import symbolic_icons


class BrightnessSlider(SettingSlider):
    """A widget to display a scale for brightness settings."""

    def __init__(
        self,
    ):
        self.client = BrightnessService()
        super().__init__(
            pixel_size=20,
            icon_name=symbolic_icons["brightness"]["screen"],
            min=0,
            max=self.client.max_screen,  # Use actual max brightness
            start_value=self.client.screen_brightness,
        )

        if self.client.screen_brightness == -1:
            self.destroy()
            return

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            self.client.connect("brightness_changed", self.on_brightness_change)

        self.icon_button.connect("clicked", self.reset)

    def reset(self, *_):
        """Reset the brightness to the default value."""
        self.client.screen_brightness = 0

    @cooldown(0.1)
    def on_scale_move(self, _, __, moved_pos):
        self.client.screen_brightness = moved_pos

    def on_brightness_change(self, service: BrightnessService, _):
        set_scale_adjustment(self.scale, 0, 100, 1)
        self.scale.set_value(service.screen_brightness)
        percentage = int((service.screen_brightness / service.max_screen) * 100)
        self.scale.set_tooltip_text(f"{percentage}%")
