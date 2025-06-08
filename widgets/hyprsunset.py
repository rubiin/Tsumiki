from shared.button_toggle import CommandSwitcher


class HyprSunsetWidget(CommandSwitcher):
    """A widget to control the hyprsunset command."""

    def __init__(self, **kwargs):
        # Set the command to adjust the screen temperature
        self.command = "hyprsunset"
        self.args = f"-t {self.config['temperature']}"

        super().__init__(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            label=self.config["label"],
            tooltip=self.config["tooltip"],
            name="hyprsunset",
            **kwargs,
        )
