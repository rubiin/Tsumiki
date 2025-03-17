import json

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from loguru import logger

from shared import ButtonWidget
from utils import KBLAYOUT_MAP, BarConfig
from utils.widget_utils import text_icon


class KeyboardLayoutWidget(ButtonWidget):
    """A widget to display the current keyboard layout."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="keyboard", **kwargs)

        self.box = Box()
        self.children = (self.box,)

        self.config = widget_config["keyboard"]

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.kb_label = Label(label="0", style_classes="panel-text", visible=False)

        self.box.children = (self.icon, self.kb_label)

        self.connection = get_hyprland_connection()

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.get_keyboard(), logger.info(
            "[Keyboard] Connected to the hyprland socket"
        )

    def get_keyboard(self):
        data = json.loads(str(self.connection.send_command("j/devices").reply.decode()))
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
            self.kb_label.set_label(KBLAYOUT_MAP[layout])
            self.kb_label.show()
