from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.scale import Scale

from utils.icons import icons

from .widget_container import HoverButton


class SettingSlider(Box):
    """A widget to display a scale for quick settings."""

    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        start_value: float = 50,
        icon_name: str = icons["fallback"]["package"],
        pixel_size: int = 18,
        **kwargs,
    ):
        super().__init__(
            name="setting-slider",
            **kwargs,
        )
        self.pixel_size = pixel_size
        self.icon = Image(
            icon_name=icon_name, icon_size=self.pixel_size, style_classes="panel-icon"
        )
        self.icon_button = HoverButton(image=self.icon, name="setting-slider-button")

        self.scale = Scale(
            marks=None,
            min_value=min,
            max_value=max,
            name="setting-slider-scale",
            value=start_value,
            increments=(1, 1),
            tooltip_text=str(start_value),
        )

        self.children = (self.icon_button, self.scale)
