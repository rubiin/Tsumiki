from shared import CommandSwitcher
from utils import BarConfig


class HyprSunsetWidget(CommandSwitcher):
    """A widget to control the hyprsunset command."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        # Store the configuration for hyprsunset
        self.config = widget_config["hypr_sunset"]

        # Set the command to adjust the screen temperature
        self.command = f"hyprsunset -t {self.config['temperature']}"

        super().__init__(
            config=widget_config,
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            label=self.config["label"],
            tooltip=self.config["tooltip"],
            name="hyprsunset",
            **kwargs,
        )
