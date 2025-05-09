from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.label import Label
from gi.repository import Gdk

from shared import ButtonWidget
from utils import BarConfig, ExecutableNotFoundError
from utils.functions import executable_exists
from utils.widget_utils import text_icon


class HyprPickerWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config["hypr_picker"], name="hypr_picker", **kwargs)

        if not executable_exists("hyprpicker"):
            raise ExecutableNotFoundError("hyprpicker")

        self.picker_label = Label(label="picker", style_classes="panel-text")

        if self.config["show_icon"]:
            # Create a TextIcon with the specified icon and size
            self.icon = text_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-icon"},
            )
            self.box.add(self.icon)

        if self.config["label"]:
            self.box.add(self.picker_label)

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
