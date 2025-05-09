from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.widget import Widget
from gi.repository import Gtk

from shared import ButtonWidget, PopupWindow
from shared.dialog import Dialog
from shared.widget_container import HoverButton
from utils import BarConfig
from utils.widget_utils import text_icon


class PowerMenuPopup(PopupWindow):
    """A popup window to show power options."""

    instance = None

    @staticmethod
    def get_default(widget_config):
        if PowerMenuPopup.instance is None:
            PowerMenuPopup.instance = PowerMenuPopup(widget_config)

        return PowerMenuPopup.instance

    def __init__(
        self,
        config,
        **kwargs,
    ):
        self.icon_size = config["icon_size"]

        power_buttons_list = config["buttons"]

        self.grid = Gtk.Grid(
            visible=True,
            column_homogeneous=True,
            row_homogeneous=True,
        )

        self.row = 0
        self.column = 0
        self.max_columns = config["items_per_row"]

        for index, (key, value) in enumerate(power_buttons_list.items()):
            button = PowerControlButtons(
                config=config,
                name=key,
                command=value,
                size=self.icon_size,
            )
            self.grid.attach(button, self.column, self.row, 1, 1)
            self.column += 1
            if self.column >= self.max_columns:
                self.column = 0
                self.row += 1

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
        self.dialog = Dialog(
            title=name,
            body=f"Are you sure you want to {name}?",
            command=command,
            **kwargs,
        )

        super().__init__(
            config=config,
            orientation="v",
            name="power-control-button",
            on_clicked=lambda _: self.on_button_press(),
            child=Box(
                orientation="v",
                children=[
                    Image(
                        image_file=get_relative_path(f"../assets/icons/png/{name}.png"),
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

    def on_button_press(
        self,
    ):
        PowerMenuPopup.get_default(widget_config=self.config).toggle_popup()
        self.dialog.toggle_popup()
        return True


class PowerWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config["power"], name="power", **kwargs)

        self.power_label = Label(label="power", style_classes="panel-text")

        if self.config["show_icon"]:
            # Create a TextIcon with the specified icon and size
            self.icon = text_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-icon"},
            )
            self.box.add(self.icon)

        if self.config["label"]:
            self.box.add(self.power_label)

        if self.config["tooltip"]:
            self.set_tooltip_text("Power")

        self.connect(
            "clicked",
            lambda *_: PowerMenuPopup.get_default(
                widget_config=self.config
            ).toggle_popup(),
        )
