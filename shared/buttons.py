from functools import partial

from fabric.core.service import Signal
from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from utils.bezier import cubic_bezier
from utils.icons import symbolic_icons, text_icons
from utils.widget_utils import nerd_font_icon, setup_cursor_hover

from .circle_image import CircleImage
from .submenu import QuickSubMenu
from .widget_container import BaseWidget


class HoverButton(Button, BaseWidget):
    """A container for button with hover effects."""

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        setup_cursor_hover(self)


class ScanButton(HoverButton):
    """A button to start a scan action."""

    def __init__(self, **kwargs):
        super().__init__(name="scan-button", style_classes="submenu-button", **kwargs)

        self.scan_image = CircleImage(
            image_file=get_relative_path("../assets/icons/svg/refresh2.svg"),
            size=20,
        )
        self.scan_animator = None

        self.set_image(self.scan_image)

    def set_notify_value(self, p, *_):
        self.scan_image.set_angle(p.value)

    def play_animation(self):
        from .animator import Animator

        if self.scan_animator is None:
            self.scan_animator = Animator(
                timing_function=partial(cubic_bezier, 0, 0, 1, 1),
                duration=4,
                min_value=0,
                max_value=360,
                tick_widget=self,
                notify_value=self.set_notify_value,
            )
        self.scan_animator.play()

    def stop_animation(self):
        self.scan_animator.stop()


class QSToggleButton(Box, BaseWidget):
    """A widget to display a toggle button for quick settings."""

    @Signal
    def action_clicked(self) -> None: ...

    def __init__(
        self,
        action_label: str = "My Label",
        action_icon: str = text_icons["ui"]["package"],
        pixel_size: int = 18,
        **kwargs,
    ):
        self.pixel_size = pixel_size

        # required for chevron button
        self.box = Box()

        # Action button can hold an icon and a label NOTHING MORE
        self.action_icon = nerd_font_icon(
            icon=action_icon,
            props={
                "style_classes": ["panel-font-icon"],
                "style": f"font-size: {self.pixel_size}px;",
            },
        )

        self.action_label = Label(
            style_classes="panel-text",
            label=action_label,
            ellipsization="end",
            h_align="start",
            h_expand=True,
        )

        self.action_button = HoverButton(
            style_classes="quicksettings-toggle-action",
            on_clicked=self._action,
        )

        self.action_button.set_size_request(170, 20)

        self.action_button.add(
            Box(
                h_align="start",
                v_align="center",
                style_classes="quicksettings-toggle-action-box",
                children=[self.action_icon, self.action_label],
            ),
        )

        self.box.add(self.action_button)

        super().__init__(
            name="quicksettings-togglebutton",
            h_align="start",
            v_align="start",
            children=[self.box],
            **kwargs,
        )

    def _action(self, *_):
        self.emit("action-clicked")

    def set_active_style(self, action: bool, *_) -> None:
        self.set_style_classes("") if not action else self.set_style_classes("active")

    def set_action_label(self, label: str):
        self.action_label.set_label(label.strip())

    def set_action_icon(self, icon: str):
        self.action_icon.set_label(icon)


class QSChevronButton(QSToggleButton):
    """A widget to display a toggle button for quick settings."""

    @Signal
    def reveal_clicked(self) -> None: ...

    def __init__(
        self,
        action_label: str = "My Label",
        action_icon: str = symbolic_icons["fallback"]["package"],
        pixel_size: int = 18,
        submenu: QuickSubMenu | None = None,
        **kwargs,
    ):
        self.submenu = submenu

        self.button_image = Image(
            icon_name=symbolic_icons["ui"]["arrow"]["right"], icon_size=20
        )

        self.reveal_button = HoverButton(
            style_classes="toggle-revealer",
            image=self.button_image,
            h_expand=True,
            on_clicked=self._reveal_toggle,
        )

        super().__init__(
            action_label,
            action_icon,
            pixel_size,
            **kwargs,
        )
        self.box.add(self.reveal_button)

        self.submenu.revealer.connect(
            "notify::reveal-child",
            self.set_chevron_icon,
        )

    def set_chevron_icon(self, *_):
        icon_name = (
            symbolic_icons["ui"]["arrow"]["down"]
            if self.submenu.revealer.get_reveal_child()
            else symbolic_icons["ui"]["arrow"]["right"]
        )
        self.button_image.set_from_icon_name(icon_name, 20)

    def _reveal_toggle(self, *_):
        self.emit("reveal-clicked")
