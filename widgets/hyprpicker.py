import os

from fabric.utils import exec_shell_command_async
from fabric.widgets.label import Label
from gi.repository import Gdk

from shared.widget_container import ButtonWidget
from utils.constants import ASSETS_DIR
from utils.widget_utils import nerd_font_icon


class HyprPickerWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, **kwargs):
        super().__init__(name="hyprpicker", **kwargs)

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.container_box.add(
                nerd_font_icon(
                    icon=self.config.get("icon", "󰕸"),
                    props={"style_classes": "panel-font-icon"},
                )
            )

        if self.config.get("label", True):
            self.container_box.add(Label(label="picker", style_classes="panel-text"))

        self.connect("button-press-event", self.on_button_press)

        self.initialized = False

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Pick a color")

    def lazy_init(self):
        if not self.initialized:
            self.script_file = f"{ASSETS_DIR}/scripts/hyprpicker.sh"
            if not os.path.isfile(self.script_file):
                self.set_sensitive(False)
                self.set_tooltip_text("Script not found")
                return
            self.initialized = True

    def on_button_press(self, button, event):
        self.lazy_init()

        if not self.initialized:
            return  # Early exit if script not available

        base_command = f"{self.script_file}"
        if self.config.get("quiet", False):
            base_command += " --no-notify"

        # Mouse event handler
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                # Left click: HEX
                exec_shell_command_async(f"{base_command} -hex", lambda *_: None)
            elif event.button == 2:
                # Middle click: HSV
                exec_shell_command_async(f"{base_command} -hsv", lambda *_: None)
            elif event.button == 3:
                # Right click: RGB
                exec_shell_command_async(f"{base_command} -rgb", lambda *_: None)
