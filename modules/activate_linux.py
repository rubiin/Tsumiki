from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.widget_container import BaseWindow
from utils.i18n import _
from utils.widget_settings import BarConfig


class ActivateLinux(BaseWindow):
    """
    A simple activate linux widget.
    """

    def __init__(self, config: BarConfig, **kwargs):
        self.config = config.get("modules", {}).get("activate_linux", {})

        self.main_label = Label(
            name="activate_linux-main-label",
            label=_('module.activate_linux.title'),
            h_expand=True,
            justification="left",
            h_align="start",
        )

        self.sub_label = Label(
            name="activate_linux-sub-label",
            label=_('module.activate_linux.subtitle'),
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
