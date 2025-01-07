import json

from fabric.utils import exec_shell_command_async
from fabric.widgets.label import Label

from shared.widget_container import BoxWidget
from utils.config import KBLAYOUT_MAP
from utils.functions import text_icon
from utils.widget_config import BarConfig


class KeyboardLayoutWidget(BoxWidget):
    """A widget to display the current keyboard layout."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="keyboard", **kwargs)

        self.config = widget_config["keyboard"]

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.kb_label = Label(label="0", style_classes="panel-text", visible=False)

        self.children = (self.icon, self.kb_label)

        exec_shell_command_async(
            "hyprctl devices -j", lambda output: self.get_keyboard(output)
        )

    def get_keyboard(self, value: str):
        data = json.loads(value)
        keyboards = data["keyboards"]
        if len(keyboards) == 0:
            return "Unknown"

        main_kb = next((kb for kb in keyboards if kb["main"]), None)

        if not main_kb:
            main_kb = keyboards[len(keyboards) - 1]

        layout = main_kb["active_keymap"]

        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"Caps Lock 󰪛: {main_kb['capsLock']} | Num Lock : {main_kb['numLock']}"
            )

        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.kb_label.set_label(f"󰌌 {KBLAYOUT_MAP[layout]}")
            self.kb_label.show()
