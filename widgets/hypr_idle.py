from shared import CommandSwitcher
from utils import BarConfig


class HyprIdleWidget(CommandSwitcher):
    """A widget to control the hypridle command."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        # Store the configuration for hypridle
        self.config = widget_config["hypr_idle"]

        # Set the command to hypridle
        self.command = "hypridle"

        super().__init__(
            config=widget_config,
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            label=self.config["label"],
            tooltip=self.config["tooltip"],
            name="hypridle",
            **kwargs,
        )
