from fabric.widgets.box import Box
from fabric.widgets.label import Label

from utils.functions import get_display_server_window
from utils.widget_settings import BarConfig

Window = get_display_server_window()


class ActivateLinux(Window):
    """
    A simple activate linux widget.
    """

    def __init__(self, config: BarConfig, **kwargs):
        self.config = config.get("modules", {}).get("activate_linux", {})

        self.main_label = Label(
            name="activate_linux-main-label",
            label="Activate Linux",
            h_expand=True,
            justification="left",
            h_align="start",
        )

        self.sub_label = Label(
            name="activate_linux-sub-label",
            label="Go to Settings to activate Linux.",
            h_expand=True,
            justification="left",
        )

        super().__init__(
            name="activate_linux",
            layer=self.config.get("layer", "top"),
            anchor=self.config.get("anchor", "center"),
            child=Box(
                name="activate_linux-box",
                orientation="v",
                children=(self.main_label, self.sub_label),
            ),
            **kwargs,
        )
