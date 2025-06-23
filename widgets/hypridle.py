from shared.button_toggle import CommandSwitcher


class HyprIdleWidget(CommandSwitcher):
    """A widget to control the hypridle command."""

    def __init__(self, **kwargs):
        # Set the command to hypridle
        self.command = "hypridle"

        super().__init__(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            label=self.config["label"],
            tooltip=self.config["tooltip"],
            name="hypridle",
            **kwargs,
        )
