from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.label import Label
from gi.repository import Gdk

from shared.widget_container import ButtonWidget
from utils.functions import check_executable_exists
from utils.widget_utils import text_icon


class HyprPickerWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, **kwargs):
        super().__init__(name="hyprpicker", **kwargs)

        check_executable_exists("hyprpicker")

        if self.config["show_icon"]:
            # Create a TextIcon with the specified icon and size
            self.box.add(
                text_icon(
                    icon=self.config["icon"],
                    props={"style_classes": "panel-font-icon"},
                )
            )

        if self.config["label"]:
            self.box.add(Label(label="picker", style_classes="panel-text"))

        self.connect("button-press-event", self.on_button_press)

        self.script_file = get_relative_path("../assets/scripts/hyprpicker.sh")

        if self.config["tooltip"]:
            self.set_tooltip_text("Pick a color")

    def on_button_press(self, button, event):
        # Mouse event handler
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                # Left click: HEX
                exec_shell_command_async(f"{self.script_file} -hex", lambda *_: None)
            elif event.button == 2:
                # Middle click: HSV
                exec_shell_command_async(f"{self.script_file} -hsv", lambda *_: None)
            elif event.button == 3:
                # Right click: RGB
                exec_shell_command_async(f"{self.script_file} -rgb", lambda *_: None)
