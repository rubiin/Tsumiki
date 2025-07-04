from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.label import Label
from gi.repository import Gdk

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class HyprPickerWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, **kwargs):
        super().__init__(name="hyprpicker", **kwargs)

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.box.add(
                nerd_font_icon(
                    icon=self.config["icon"],
                    props={"style_classes": "panel-font-icon"},
                )
            )

        if self.config.get("label", True):
            self.box.add(Label(label="picker", style_classes="panel-text"))

        self.connect("button-press-event", self.on_button_press)

        self.initialized = False

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Pick a color")

    def lazy_init(self):
        if not self.initialized:
            self.script_file = get_relative_path("../assets/scripts/hyprpicker.sh")
            self.initialized = True

    def on_button_press(self, button, event):
        self.lazy_init()

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
