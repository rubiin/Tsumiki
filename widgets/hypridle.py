from shared.button_toggle import CommandSwitcher


class HyprIdleWidget(CommandSwitcher):
    """A widget to control the hypridle command."""

    def __init__(self, **kwargs):
        # Set the command to hypridle
        self.command = "hypridle"

        super().__init__(
            command=self.command,
            enabled_icon=self.config.get("enabled_icon", "󰕸"),
            disabled_icon=self.config.get("disabled_icon", "󰕸"),
            label=self.config.get("label", "HyprIdle"),
            tooltip=self.config.get("tooltip", "Control the hypridle command"),
            name="hypridle",
            **kwargs,
        )
