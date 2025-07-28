from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.svg import Svg
from fabric.widgets.widget import Widget

from shared.buttons import HoverButton
from shared.dialog import Dialog
from shared.popup import PopupWindow
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class PowerMenuPopup(PopupWindow):
    """A popup window to show power options."""

    instance = None

    @staticmethod
    def get_default(config):
        if PowerMenuPopup.instance is None:
            PowerMenuPopup.instance = PowerMenuPopup(config)

        return PowerMenuPopup.instance

    def __init__(
        self,
        config,
        **kwargs,
    ):
        self.icon_size = config.get("icon_size", 16)

        power_buttons_list = config.get("buttons", [])
        self.grid = Grid(
            column_homogeneous=True,
            row_homogeneous=True,
        )

        self.grid.attach_flow(
            children=[
                PowerControlButtons(
                    config=config,
                    name=key,
                    command=value,
                    size=self.icon_size,
                )
                for key, value in power_buttons_list.items()
            ],
            columns=config.get("items_per_row", 3),
        )

        self.menu = Box(name="power-button-menu", orientation="v", children=self.grid)

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


class PowerControlButtons(HoverButton):
    """A widget to show power options."""

    def __init__(
        self, config, name: str, command: str, size: int, show_label=True, **kwargs
    ):
        self.config = config
        self.name = name
        self.command = command
        self.size = size

        super().__init__(
            config=config,
            orientation="v",
            name="power-control-button",
            on_clicked=self.on_button_press,
            child=Box(
                orientation="v",
                children=[
                    Svg(
                        svg_file=get_relative_path(f"../assets/icons/svg/{name}.svg"),
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
        )

    def on_button_press(self, *_):
        PowerMenuPopup.get_default(widget_config=self.config).toggle_popup()
        Dialog().add_content(
            title=f"{self.name.capitalize()} Confirmation",
            body=f"Are you sure you want to {self.name}?",
            command=self.command,
        ).toggle_popup()

        return True


class PowerWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, **kwargs):
        super().__init__(name="power", **kwargs)

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        if self.config.get("label", True):
            self.box.add(Label(label="power", style_classes="panel-text"))

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Power")

        self.connect(
            "clicked",
            lambda *_: PowerMenuPopup.get_default(self.config).toggle_popup(),
        )
