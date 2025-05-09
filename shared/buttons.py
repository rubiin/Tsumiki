from fabric.core.service import Signal
from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from utils.icons import icons
from utils.widget_utils import setup_cursor_hover

from .animator import Animator
from .circle_image import CircleImage
from .separator import Separator
from .submenu import QuickSubMenu
from .widget_container import HoverButton


class ScanButton(HoverButton):
    """A button to start a scan action."""

    def __init__(self, **kwargs):
        super().__init__(name="scan-button", style_classes="submenu-button", **kwargs)

        self.scan_image = CircleImage(
            image_file=get_relative_path("../assets/icons/png/refresh.png"),
            size=20,
        )

        self.scan_animator = Animator(
            bezier_curve=(0, 0, 1, 1),
            duration=4,
            min_value=0,
            max_value=360,
            tick_widget=self,
            repeat=False,
            notify_value=lambda p, *_: self.scan_image.set_angle(p.value),
        )

        self.set_image(self.scan_image)

    def play_animation(self):
        self.scan_animator.play()

    def stop_animation(self):
        self.scan_animator.stop()


class QSToggleButton(Box):
    """A widget to display a toggle button for quick settings."""

    @Signal
    def action_clicked(self) -> None: ...

    def __init__(
        self,
        action_label: str = "My Label",
        action_icon: str = icons["fallback"]["package"],
        pixel_size: int = 20,
        **kwargs,
    ):
        self.pixel_size = pixel_size

        self.box = Box()

        # Action button can hold an icon and a label NOTHING MORE
        self.action_icon = Image(
            style_classes="panel-icon",
            icon_name=action_icon,
            icon_size=pixel_size,
        )
        self.action_label = Label(
            style_classes="panel-text",
            label=action_label,
            ellipsization="end",
            h_align="start",
            h_expand=True,
        )

        self.action_button = HoverButton(style_classes="quicksettings-toggle-action")

        self.action_button.set_size_request(170, 20)

        self.action_button.add(
            Box(
                h_align="start",
                v_align="center",
                style_classes="quicksettings-toggle-action-box",
                children=[self.action_icon, self.action_label],
            )
        )

        self.box.add(self.action_button)

        super().__init__(
            name="quicksettings-togglebutton",
            h_align="start",
            v_align="start",
            children=[self.box],
            **kwargs,
        )

        setup_cursor_hover(self)

        self.action_button.connect("clicked", self.do_action)

    def do_action(self, _):
        self.emit("action-clicked")

    def set_active_style(self, action: bool) -> None:
        self.set_style_classes("") if not action else self.set_style_classes("active")

    def set_action_label(self, label: str):
        self.action_label.set_label(label.strip())

    def set_action_icon(self, icon_name: str):
        self.action_icon.set_from_icon_name(icon_name, self.pixel_size)


class QSChevronButton(QSToggleButton):
    """A widget to display a toggle button for quick settings."""

    @Signal
    def reveal_clicked(self) -> None: ...

    def __init__(
        self,
        action_label: str = "My Label",
        action_icon: str = icons["fallback"]["package"],
        pixel_size: int = 20,
        submenu: QuickSubMenu | None = None,
        **kwargs,
    ):
        self.submenu = submenu

        self.button_image = Image(icon_name=icons["ui"]["arrow"]["right"], icon_size=20)

        self.reveal_button = HoverButton(
            style_classes="toggle-revealer", image=self.button_image, h_expand=True
        )

        super().__init__(
            action_label,
            action_icon,
            pixel_size,
            **kwargs,
        )

        self.box.add(Separator())
        self.box.add(self.reveal_button)

        self.reveal_button.connect("clicked", self.do_reveal_toggle)

    def do_reveal_toggle(self, _):
        self.emit("reveal-clicked")
