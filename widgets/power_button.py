from typing import Literal

from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.widget import Widget

from shared import PopupWindow
from shared.widget_container import ButtonWidget
from utils.config import widget_config
from utils.functions import handle_power_action
from utils.widget_settings import BarConfig
from utils.widget_utils import text_icon

POWER_BUTTONS = widget_config["power"]["buttons"]


class PowerMenuPopup(PopupWindow):
    """A popup window to show power options."""

    instance = None

    @staticmethod
    def get_default():
        if PowerMenuPopup.instance is None:
            PowerMenuPopup.instance = PowerMenuPopup()

        return PowerMenuPopup.instance

    def __init__(
        self,
        **kwargs,
    ):
        self.icon_size = 100

        self.menu = Box(
            name="power-button-menu",
            orientation="v",
            children=[
                Box(
                    orientation="h",
                    children=[
                        PowerControlButtons(
                            name=value,
                            size=self.icon_size,
                        )
                        for value in POWER_BUTTONS[0:3]
                    ],
                ),
                Box(
                    orientation="h",
                    children=[
                        PowerControlButtons(
                            name=value,
                            size=self.icon_size,
                        )
                        for value in POWER_BUTTONS[3:]
                    ],
                ),
            ],
        )

        super().__init__(
            transition_type="crossfade",
            child=self.menu,
            anchor="center",
            keyboard_mode="on-demand",
            **kwargs,
        )

    def set_action_buttons_focus(self, can_focus: bool):
        for child in self.menu.children[0]:
            child: Widget = child
            child.set_can_focus(can_focus)

    def toggle_popup(self):
        self.set_action_buttons_focus(True)
        return super().toggle_popup()


class PowerControlButtons(ButtonWidget):
    """A widget to show power options."""

    def __init__(self, name: str, size: int, show_label=True, **kwargs):
        (
            super().__init__(
                orientation="v",
                name="power-control-button",
                on_clicked=lambda button: self.on_button_press(pressed_button=name),
                child=Box(
                    orientation="v",
                    children=[
                        Image(
                            image_file=get_relative_path(f"../assets/icons/{name}.png"),
                            size=size,
                        ),
                        Label(
                            label=name.capitalize(),
                            style_classes="panel-text",
                            visible=show_label,
                        ),
                    ],
                ),
                **kwargs,
            ),
        )

    def on_button_press(
        self,
        pressed_button: Literal[
            "lock",
            "logout",
            "suspend",
            "hibernate",
            "shutdown",
            "reboot",
        ],
    ):
        PowerMenuPopup().get_default().toggle_popup()
        return handle_power_action(pressed_button)


class PowerWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="power", **kwargs)

        self.config = widget_config["power"]

        self.children = text_icon(
            self.config["icon"],
            self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        if self.config["tooltip"]:
            self.set_tooltip_text("Power")

        self.connect(
            "clicked",
            lambda *_: PowerMenuPopup().get_default().toggle_popup(),
        )
