from fabric.hyprland.widgets import get_hyprland_connection
from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class SubMapWidget(ButtonWidget):
    """A widget to display the current submap."""

    def __init__(self, **kwargs):
        super().__init__(name="submap", **kwargs)

        self.submap_label = Label(label="submap", style_classes="panel-text")

        self.box.add(self.submap_label)

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        self._hyprland_connection = get_hyprland_connection()

        self._hyprland_connection.connect("event::submap", self.get_submap)

        # all aboard...
        if self._hyprland_connection.ready:
            self.on_ready(None)
        else:
            self._hyprland_connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.get_submap(), logger.info(
            "[Submap] Connected to the hyprland socket"
        )

    def get_submap(self, *_):
        try:
            submap = str(
                self._hyprland_connection.send_command("submap").reply.decode()
            ).strip("\n")

            if submap == "unknown request":
                submap = "default"

            self.submap_label.set_label(submap)

            if self.config.get("tooltip", False):
                self.set_tooltip_text(
                    f"Current submap: {submap}",
                )
        except Exception as e:
            logger.error(f"[Submap] Error getting submap: {e}")
