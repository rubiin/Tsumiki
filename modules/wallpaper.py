import mimetypes
import os

from fabric.core.service import Signal
from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GLib

from shared.popup import PopupWindow

WALLPAPER_DIR = f"/home/{GLib.get_user_name()}/Pictures/Wallpapers"
WALLPAPER_THUMBS_DIR = f"/home/{GLib.get_user_name()}/wallpapers/.thumbs"


print(WALLPAPER_DIR)

if not os.path.exists(WALLPAPER_DIR):
    os.makedirs(WALLPAPER_DIR)

if not os.path.exists(WALLPAPER_THUMBS_DIR):
    os.makedirs(WALLPAPER_THUMBS_DIR)


class ImageButton(Button):
    """A button that sets the wallpaper when clicked."""

    @Signal
    def wallpaper_change(self, wp_path: str) -> str: ...

    def __init__(self, wallpaper_name, thumb_size=300, **kwargs):
        self.wallpaper_name = wallpaper_name
        self.wp_path = os.path.join(WALLPAPER_DIR, self.wallpaper_name)
        self.thumb_size = thumb_size
        self.wp_thumb_path = os.path.join(
            WALLPAPER_THUMBS_DIR, f"{self.thumb_size}_{self.wallpaper_name}"
        )
        super().__init__(
            style_classes=[
                "button-basic",
                "button-basic-props",
                "cool-border",
            ],  # TODO: change these css
            on_clicked=lambda *_: self._set_wallpaper_from_image(),
            **kwargs,
        )
        self._generate_wp_thumbnail()

    def _set_wallpaper_from_image(self):
        def on_wallpaper_change(*_):
            self.wallpaper_change(self.wp_path)

        exec_shell_command_async(
            f"hyprctl hyprpaper reload ,'{self.wp_path}'", on_wallpaper_change
        )

    def _generate_wp_thumbnail(self):
        if os.path.exists(self.wp_thumb_path):
            self.set_image(
                Image(image_file=self.wp_thumb_path, style="border-radius: 20px")
            )
            return

        exec_shell_command_async(
            f"ffmpegthumbnailer -i {self.wp_path} -s {self.thumb_size} -o {self.wp_thumb_path}",  # noqa: E501
            lambda *_: self.set_image(
                Image(image_file=self.wp_thumb_path, style="border-radius: 20px")
            ),
        )


class WallpaperPickerBox(ScrolledWindow):
    """A box that contains wallpaper buttons."""

    @Signal
    def wallpaper_change(self, wp_path: str) -> str: ...

    def __init__(self):
        super().__init__(
            orientation="h",
            max_content_size=(-1, 800),
        )
        self._buttons = self._grab_wallpaper_images()
        row_size = 3
        rows = [
            self._buttons[i : i + row_size]
            for i in range(0, len(self._buttons), row_size)
        ]
        self._main_box = Box(
            orientation="v",
            children=[Box(children=row, orientation="h", spacing=10) for row in rows],
            spacing=10,
        )
        self.children = self._main_box

    def _grab_wallpaper_images(self) -> list[ImageButton]:
        images = []
        print(os.listdir(WALLPAPER_DIR))
        for wp in os.listdir(WALLPAPER_DIR):
            file_type = mimetypes.guess_type(wp)[0]

            if file_type and "image" in file_type:
                images.append(
                    ImageButton(
                        wp,
                        on_wallpaper_change=lambda _, wp_path: self.wallpaper_change(
                            wp_path
                        ),
                    )
                )
        return images


class WallPaperPickerOverlay(PopupWindow):
    """A popup window for selecting wallpapers."""

    def __init__(self):
        self.wallpaper_box = WallpaperPickerBox()
        super().__init__(
            layer="top",
            child=Box(
                orientation="v",
                spacing=10,
                children=[
                    Label("Wallpaper Picker", style_classes=["label-title"]),
                    self.wallpaper_box,
                ],
                style_classes=["cool-border", "window-basic"],
            ),
            transition_duration=300,
            transition_type="slide-down",
            anchor="center",
            enable_inhibitor=True,
        )
        self.wallpaper_box.connect("wallpaper-change", lambda *_: self.toggle_popup())

    def toggle_popup(self, monitor: bool = False):
        super().toggle_popup(monitor)


wallpaper_picker = WallPaperPickerOverlay()
