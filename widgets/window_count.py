from fabric.hyprland import HyprlandReply
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import bulk_connect, logger
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.functions import parse_hyprland_reply


class WindowCountWidget(ButtonWidget):
    """A widget to display windows in active workspace."""

    def __init__(self, **kwargs):
        super().__init__(name="window_count", **kwargs)

        self._hyprland_connection = get_hyprland_connection()

        self.count_label = Label(label="0", style_classes=["panel-text"])
        self.container_box.add(self.count_label)

        for hid in bulk_connect(
            self._hyprland_connection,
            {
                "event::workspace": self._get_window_count,
                "event::focusedmon": self._get_window_count,
                "event::openwindow": self._get_window_count,
                "event::closewindow": self._get_window_count,
                "event::movewindow": self._get_window_count,
            },
        ):
            self._register_handler(self._hyprland_connection, hid)

        # all aboard...
        if self._hyprland_connection.ready:
            self.on_ready(None)
        else:
            self._register_handler(
                self._hyprland_connection,
                self._hyprland_connection.connect("event::ready", self.on_ready),
            )

    def on_ready(self, _):
        return self._get_window_count(None, None), logger.info(
            "[WindowCount] Connected to the hyprland socket"
        )

    def _handle_workspace_response(self, res: HyprlandReply, *_):
        try:
            data = parse_hyprland_reply(res)
            count = data.get("windows", 0)
            label_format = self.config.get("label_format", "[{count}]")
            self.count_label.set_label(label_format.format(count=count))

            if self.config.get("tooltip", False) and self.tooltips_enabled:
                self.set_tooltip_text(f"Workspace: {data.get('id')}, Windows: {count}")

            if self.config.get("hide_when_zero", False):
                self.set_visible(count != 0)

            logger.info(f"[WindowCount] Workspace: {data.get('id')} | Windows: {count}")
        except Exception as e:
            logger.exception(f"[WindowCount] Failed to parse workspace data: {e}")

    def _get_window_count(self, *_):
        """Get the number of windows in the active workspace."""
        try:
            self._hyprland_connection.send_command_async(
                "j/activeworkspace", self._handle_workspace_response
            )
        except Exception as e:
            logger.exception(f"[WindowCount] Failed to get active workspace: {e}")
