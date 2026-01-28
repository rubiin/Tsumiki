import math
import subprocess
from pathlib import Path

from shared.animator import Animator
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.revealer import Revealer
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.wayland import WaylandWindow
from PIL import Image as PILImage
from PIL import ImageFilter, ImageOps

from utils.constants import WALLPAPER_BLURRED_DIR, WALLPAPER_DIR, WALLPAPER_THUMBS_DIR

SCREEN_SIZE = (1920, 1080)
SPACING = 20
WALLPAPERS_PER_PAGE = 5
THUMBNAIL_SIZE = (
    (SCREEN_SIZE[0] / WALLPAPERS_PER_PAGE)
    - (SPACING * (WALLPAPERS_PER_PAGE - 1)) / WALLPAPERS_PER_PAGE,
    math.ceil(SCREEN_SIZE[1] / 2),
)
SLOWNESS_FACTOR = 5.5


class Bgselector(WaylandWindow):
    """A wallpaper selector widget."""

    def __init__(self, **kwargs):
        super().__init__(
            anchor="bottom",
            keyboard_mode="none",
        )
        self.connect("key-press-event", self.on_key_press)

        for path in Path(WALLPAPER_DIR).iterdir():
            if path.is_file():
                img = PILImage.open(str(path))
                blurred_img = img.filter(ImageFilter.GaussianBlur(5))
                blurred_img.save(WALLPAPER_BLURRED_DIR + path.name)
                resized_img = ImageOps.cover(img, THUMBNAIL_SIZE, 1)
                resized_img.save(WALLPAPER_THUMBS_DIR + path.name)

        self.wallpapers_container = Box(
            size=(SCREEN_SIZE[0], THUMBNAIL_SIZE[1]),
            v_align="center",
            h_align="center",
            orientation="h",
            spacing=SPACING,
        )

        for file in sorted(Path(WALLPAPER_THUMBS_DIR).iterdir()):
            if file.is_file():
                new_wallpaper = ScrolledWindow(
                    child=Image(image_file=str(file), h_align="fill", name=file.name),
                    min_content_size=THUMBNAIL_SIZE,
                    max_content_size=THUMBNAIL_SIZE,
                    name="wallpaper",
                    h_align="center",
                    v_align="center",
                    v_scrollbar_policy="never",
                    h_scrollbar_policy="always",
                    overlay_scroll=True,
                )
                self.wallpapers_container.add(new_wallpaper)

        self.carousel = ScrolledWindow(
            min_content_size=(SCREEN_SIZE[0], THUMBNAIL_SIZE[1]),
            max_content_size=(SCREEN_SIZE[0], THUMBNAIL_SIZE[1]),
            name="carousel",
            child=self.wallpapers_container,
            h_align="center",
            v_align="center",
            v_scrollbar_policy="never",
            h_scrollbar_policy="always",
            overlay_scroll=False,
        )
        self.carousel_adjustment = self.carousel.get_hadjustment()
        self.carousel_adjustment.connect("value-changed", self.on_navigate)
        self.animator = Animator(
            bezier_curve=(0.34, 1.56, 0.64, 1.0),
            duration=0.8,
            tick_widget=self,
            notify_value=lambda animator, *_: self.carousel_adjustment.set_value(
                animator.value
            ),
        )

        self.do_parallax = True
        self.centered_index = math.ceil(len(self.wallpapers_container) / 2) - 1
        self.scroll_to_next_wallpaper()
        self.old_carousel_value = self.carousel_adjustment.get_value()

        self.main_container = Box(
            size=SCREEN_SIZE,
            name="maincontainer",
            spacing=SPACING,
            children=[self.carousel],
            h_align="center",
            v_align="center",
        )

        self.revealer = Revealer(
            transition_type="slide-up",
            transition_duration=200,
            child=self.main_container,
            h_align="center",
            v_align="center",
        )

        self.revealer_container = Box(
            size=1, children=[self.revealer], h_align="center", v_align="center"
        )

        self.add(self.revealer_container)

    def scroll_to_next_wallpaper(self):
        self.animator.pause()
        y_position = (
            (self.centered_index * THUMBNAIL_SIZE[0])
            + (self.centered_index * SPACING)
            + (THUMBNAIL_SIZE[0] / 2)
            - (SCREEN_SIZE[0] / 2)
        )
        current_value = self.carousel_adjustment.get_value()
        self.animator.min_value = current_value
        self.animator.max_value = y_position
        self.animator.play()

    def cycle_carousel(self, direction):
        self.do_parallax = False
        current_value = self.carousel_adjustment.get_value()
        match direction:
            case "right":
                tail = self.wallpapers_container.get_children()[0]
                self.wallpapers_container.reorder_child(tail, -1)
                self.carousel_adjustment.set_value(
                    current_value - THUMBNAIL_SIZE[0] - SPACING
                )
            case "left":
                tail = self.wallpapers_container.get_children()[-1]
                self.wallpapers_container.reorder_child(tail, 0)
                self.carousel_adjustment.set_value(
                    current_value + THUMBNAIL_SIZE[0] + SPACING
                )
        self.do_parallax = True

    def on_navigate(self, carousel_adjusment):
        new_carousel_value = carousel_adjusment.get_value()
        if self.do_parallax:
            for i, adj in enumerate(
                [
                    wallpaper.get_hadjustment()
                    for wallpaper in self.wallpapers_container.get_children()
                ]
            ):
                if i in range(
                    self.centered_index - math.ceil(WALLPAPERS_PER_PAGE / 2),
                    self.centered_index + math.ceil(WALLPAPERS_PER_PAGE / 2) + 1,
                ):
                    carousel_change = new_carousel_value - self.old_carousel_value
                    current_wallpaper_value = adj.get_value()
                    adj.set_value(
                        current_wallpaper_value + carousel_change / SLOWNESS_FACTOR
                    )
                elif i < self.centered_index:
                    adj.set_value(adj.get_upper() - adj.get_page_size())
                else:
                    adj.set_value(0)
        self.old_carousel_value = new_carousel_value

    def on_key_press(self, _, event):
        key = event.keyval
        if key == 65307:
            self.toggle()
        elif key == 65293:
            self.handle_enter()
        elif key in range(65361, 65365):
            self.handle_arrow(key)
        return True

    def handle_enter(self):
        file_name = (
            self.wallpapers_container.get_children()[self.centered_index]
            .get_child()
            .get_child()
            .get_name()
        )
        subprocess.run(
            [
                "swww",
                "img",
                WALLPAPER_DIR + file_name,
                "-t",
                "grow",
                "--transition-duration",
                "1",
                "--transition-fps",
                "75",
                "-n",
                "workspaces",
            ]
        )
        subprocess.run(
            [
                "swww",
                "img",
                WALLPAPER_BLURRED_DIR + file_name,
                "-t",
                "grow",
                "--transition-duration",
                "1",
                "--transition-fps",
                "75",
                "-n",
                "overview",
            ]
        )
        self.toggle()

    def handle_arrow(self, arrow_key):
        match arrow_key:
            case 65363:
                self.cycle_carousel("right")
                self.scroll_to_next_wallpaper()
            case 65361:
                self.cycle_carousel("left")
                self.scroll_to_next_wallpaper()

    def toggle(self):
        if self.revealer.fully_revealed:
            self.revealer.unreveal()
            self.set_keyboard_mode("none")
        else:
            self.revealer.reveal()
            self.set_keyboard_mode("exclusive")

