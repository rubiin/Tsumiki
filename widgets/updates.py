import json
from datetime import datetime

from fabric.utils import (
    cooldown,
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.widget_utils import (
    nerd_font_icon,
    reusable_fabricator,
)


class UpdatesWidget(ButtonWidget):
    """A widget to display the number of available updates."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(name="updates", **kwargs)

        self.update_time = datetime.now()

        script_file = get_relative_path("../assets/scripts/systemupdates.sh")

        self.base_command = f"{script_file} --{self.config['os']}"

        if self.config["flatpak"]:
            self.base_command += " --flatpak"

        if self.config["snap"]:
            self.base_command += " --snap"

        if self.config["brew"]:
            self.base_command += " --brew"

        if self.config["show_icon"]:
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        if self.config["label"]:
            self.update_label = Label(label="0", style_classes="panel-text")
            self.box.add(self.update_label)

        self.connect("button-press-event", self.on_button_press)

        # Set up a repeater to call the update method at specified intervals
        self.check_update()

        # reusing the fabricator to call specified intervals
        reusable_fabricator.connect("changed", self.should_update)

    def should_update(self, *_):
        """
        Handles the 'changed' signal from the fabricator.
        Checks if the update interval has elapsed and triggers an update if necessary.
        """
        if (datetime.now() - self.update_time).total_seconds() >= self.config[
            "interval"
        ]:
            self.check_update()
            self.update_time = datetime.now()
        return True

    def update_values(self, value: str):
        # Parse the JSON value

        value = json.loads(value)

        if value["total"] > "0":
            # Update the label if enabled
            if self.config["label"]:
                self.update_label.set_label(value["total"])
            if self.config["show_icon"]:
                self.icon.set_label("󱧘")

            self.set_tooltip_text(value["tooltip"])

    def on_button_press(self, _, event):
        if event.button == 1:
            self.check_update(update=True)
        else:
            self.check_update()
        return True

    @cooldown(1)
    def check_update(self, update=False):
        # Execute the update script asynchronously and update values

        if update:
            exec_shell_command_async(
                f"{self.base_command} up",
                self.update_values,
            )
        else:
            logger.info(f"{Colors.INFO}[Updates] Checking for updates...")
            exec_shell_command_async(
                self.base_command,
                self.update_values,
            )

        return True
