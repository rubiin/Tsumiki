from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.svg import Svg
from fabric.widgets.widget import Widget

from shared.buttons import HoverButton
from shared.dialog import Dialog
from shared.popup import PopupWindow
from shared.widget_container import ButtonWidget
from utils.constants import ASSETS_DIR
from utils.widget_utils import nerd_font_icon


class PowerMenuPopup(PopupWindow):
    """A popup window to show power options."""

    def __init__(
        self,
        config,
        **kwargs,
    ):
        self.icon_size = config.get("icon_size", 16)

        self.icon_dir = f"{ASSETS_DIR}/icons/svg/"
        power_buttons_list = config.get("buttons", [])

        self.grid = Grid(
            name="power-button-menu",
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
                    parent=self,
                    icon_path=self.icon_dir,
                )
                for key, value in power_buttons_list.items()
            ],
            columns=config.get("items_per_row", 3),
        )

        super().__init__(
            child=self.grid,
            transition_duration=400,
            transition_type="slide-down",
            anchor="center",
            enable_inhibitor=True,
            keyboard_mode="exclusive",
            name="power-menu-overlay",
            **kwargs,
        )

    def set_action_buttons_focus(self, can_focus: bool):
        for child in self.grid.get_children():
            child: Widget = child
            child.set_can_focus(can_focus)

    def toggle(self):
        self.set_action_buttons_focus(True)
        return super().toggle_popup()


class PowerControlButtons(HoverButton):
    """A widget to show power options."""

    def __init__(
        self,
        config,
        parent: PopupWindow,
        name: str,
        command: str,
        icon_path: str,
        size: int,
        show_label=True,
        **kwargs,
    ):
        self.config = config
        self.name = name
        self.command = command
        self.size = size
        self.parent = parent

        self.container_box = Box(
            style_classes="power-button-container",
            orientation="v",
            children=[
                Svg(
                    svg_file=f"{icon_path}/{name}.svg",
                    size=size,
                    name="svg-icon",
                ),
            ],
        )

        super().__init__(
            config=config,
            orientation="v",
            name="power-control-button",
            on_clicked=self.on_button_press,
            child=self.container_box,
            **kwargs,
        )

        if show_label:
            self.container_box.add(
                Label(
                    label=name.capitalize(),
                    style_classes="panel-text",
                )
            )

    def on_button_press(self, *_):
        self.parent.toggle_popup()
        if self.config.get("confirm", True):
            Dialog().add_content(
                title=f"{self.name.capitalize()} Confirmation",
                body=f"Are you sure you want to {self.name}?",
                command=self.command,
            ).toggle_popup()
        else:
            exec_shell_command_async(self.command, lambda *_: None)

        return True


class PowerWidget(ButtonWidget):
    """A widget to power off the system."""

    def show_popover(self, *_):
        """Show the popover."""
        if self.popup is None:
            self.popup = PowerMenuPopup(self.config)
        self.popup.toggle()

    def __init__(self, **kwargs):
        super().__init__(name="power", **kwargs)

        self.popup = None

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": "panel-font-icon"},
            )
            self.container_box.add(self.icon)

        if self.config.get("label", True):
            self.container_box.add(Label(label="power", style_classes="panel-text"))

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Power")

        self.connect(
            "clicked",
            self.show_popover,
        )
