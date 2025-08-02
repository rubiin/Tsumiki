from fabric.widgets.label import Label

from modules.wallpaper import WallPaperPickerOverlay
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class WallpaperWidget(ButtonWidget):
    """A widget to show the wallpaper picker."""

    def __init__(self, **kwargs):
        super().__init__(name="wallpaper", **kwargs)

        cfg = self.config  # Local reference for cleaner code

        # Optional tooltip
        if cfg.get("tooltip"):
            self.set_tooltip_text("Wallpaper Picker")

        # Add icon
        self.box.children = nerd_font_icon(
            icon=cfg.get("icon", "󰕸"),
            props={"style_classes": "panel-font-icon"},
        )

        # Optional label
        if cfg.get("label", True):
            self.box.add(Label(label="wallpaper", style_classes="panel-text"))

        # Lazy-init wallpaper popup
        self._wallpaper_popup = None
        self.connect("clicked", self._on_click)

    def _on_click(self, *_):
        if self._wallpaper_popup is None:
            self._wallpaper_popup = WallPaperPickerOverlay()
        self._wallpaper_popup.toggle_popup()
