import re

from fabric.hyprland.widgets import HyprlandEvent, get_hyprland_connection
from fabric.utils import logger
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.constants import KBLAYOUT_MAP
from utils.widget_utils import nerd_font_icon


class KeyboardLayoutWidget(ButtonWidget):
    """A widget to display the current keyboard layout."""

    def __init__(self, **kwargs):
        super().__init__(name="keyboard", **kwargs)

        self.kb_label = Label(label="keyboard", style_classes=["panel-text"])

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": ["panel-font-icon"]},
            )
            self.container_box.add(self.icon)

        self.container_box.add(self.kb_label)

        self._hyprland_connection = get_hyprland_connection()

        # all aboard...
        if self._hyprland_connection.ready:
            self.on_ready(None)
        else:
            self._hyprland_connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self._get_keyboard(), logger.info(
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

    def _handle_reply(self, data: str):
        try:
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
        except Exception as e:
            logger.exception(f"[Keyboard] Failed to parse keyboard data: {e}")
            return

    def _get_keyboard(self):
        try:
            self._hyprland_connection.send_command_async(
                "j/devices", lambda res, *_: self._handle_reply(res.reply.decode())
            )

        except Exception as e:
            logger.exception(f"[Keyboard] Error getting keyboard layout: {e}")
