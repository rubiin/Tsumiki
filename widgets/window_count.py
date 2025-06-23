import json

from fabric.hyprland.service import HyprlandEvent
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import bulk_connect
from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class WindowCountWidget(ButtonWidget):
    """A widget to display windows in active workspace."""

    def __init__(self, **kwargs):
        super().__init__(name="window_count", **kwargs)

        self.connection = get_hyprland_connection()

        self.count_label = Label(label="0", style_classes="panel-text")
        self.box.add(self.count_label)

        if self.config["show_icon"]:
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        bulk_connect(
            self.connection,
            {
                "event::workspace": self.get_window_count,
                "event::focusedmon": self.get_window_count,
                "event::openwindow": self.get_window_count,
                "event::closewindow": self.get_window_count,
                "event::movewindow": self.get_window_count,
            },
        )

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.get_window_count(None, None), logger.info(
            "[WindowCount] Connected to the hyprland socket"
        )

    def get_window_count(self, _, event: HyprlandEvent):
        """Get the number of windows in the active workspace."""
        data = json.loads(
            str(self.connection.send_command("j/activeworkspace").reply.decode())
        )

        self.count_label.set_label(
            self.config["label_format"].format(count=data["windows"])
        )

        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"Workspace: {data['id']}, Windows: {data['windows']}"
            )
        if self.config["hide_when_zero"]:
            self.hide() if data["windows"] == 0 else self.show()

        return (
            logger.info("[WindowCount] Could not find active windows for workspace")
            if not data
            else logger.info(
                f"[WindowCount] Set WindowCount for workspace: {data['id']}"
            )
        )
