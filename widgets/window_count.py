import json

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

        self._hyprland_connection = get_hyprland_connection()

        self.count_label = Label(label="0", style_classes="panel-text")
        self.box.add(self.count_label)

        if self.config.get("show_icon", True):
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
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

    def get_window_count(self, *_):
        """Get the number of windows in the active workspace."""
        try:
            response = self.connection.send_command("j/activeworkspace").reply.decode()
            data = json.loads(response)
        except Exception as e:
            logger.error(f"[WindowCount] Failed to get active workspace: {e}")
            return

        count = data.get("windows", 0)
        label_format = self.config.get("label_format", "[{count}]")
        self.count_label.set_label(label_format.format(count=count))

        if self.config.get("tooltip", False):
            self.set_tooltip_text(f"Workspace: {data.get('id')}, Windows: {count}")

        if self.config.get("hide_when_zero", False):
            self.set_visible(count != 0)

        logger.info(f"[WindowCount] Workspace: {data.get('id')} | Windows: {count}")
