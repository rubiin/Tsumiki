import json
import re

from fabric.hyprland.widgets import HyprlandEvent, get_hyprland_connection
from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.constants import KBLAYOUT_MAP
from utils.widget_utils import nerd_font_icon


class KeyboardLayoutWidget(ButtonWidget):
    """A widget to display the current keyboard layout."""

    def __init__(self, **kwargs):
        super().__init__(name="keyboard", **kwargs)

        self.kb_label = Label(label="keyboard", style_classes="panel-text")

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        self.box.add(self.kb_label)

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

    def on_activelayout(self, _, event: HyprlandEvent):
        if len(event.data) < 2:
            return logger.warning("[Keyboard] got invalid event data from hyprland")
        keyboard, language = event.data
        matched: bool = False

        if re.match(self.keyboard, keyboard) and (matched := True):
            self.kb_label.set_label(self.formatter.format(language=language))

        return logger.debug(
            f"[Keyboard] Keyboard: {keyboard}, Language: {language}, Match: {matched}"
        )

    def get_keyboard(self):
        data = json.loads(str(self.connection.send_command("j/devices").reply.decode()))

        keyboards = data.get("keyboards", [])
        if not keyboards:
            return "Unknown"

        main_kb = next((kb for kb in keyboards if kb.get("main")), keyboards[-1])

        layout = main_kb["active_keymap"]

        label = KBLAYOUT_MAP.get(layout, layout)

        if self.config.get("tooltip", False):
            caps = "On" if main_kb["capsLock"] else "Off"
            num = "On" if main_kb["numLock"] else "Off"
            self.set_tooltip_text(
                f"Layout: {layout} | Caps Lock 󰪛: {caps} | Num Lock : {num}"
            )

        self.kb_label.set_label(label)
