from shared.button_toggle import CommandSwitcher


class HyprSunsetWidget(CommandSwitcher):
    """A widget to control the hyprsunset command."""

    def __init__(self, **kwargs):
        # Set the command to adjust the screen temperature
        self.command = "hyprsunset"
        self.args = f"-t {self.config.get('temperature', 6500)}"

        super().__init__(
            command=self.command,
            enabled_icon=self.config.get("enabled_icon", "󰕸"),
            disabled_icon=self.config.get("disabled_icon", "󰕸"),
            label=self.config.get("label", "HyprSunset"),
            tooltip=self.config.get("tooltip", "Adjust screen temperature"),
            name="hyprsunset",
            **kwargs,
        )
