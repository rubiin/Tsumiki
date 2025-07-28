import json
from datetime import datetime

from fabric.utils import (
    bulk_connect,
    cooldown,
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
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

        self.base_command = self._build_base_command()

        if self.config.get("show_icon", True):
            self.icon = nerd_font_icon(
                icon=self.config["no_updates_icon"],
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        if self.config.get("label", True):
            self.update_label = Label(label="0", style_classes="panel-text")

            if self.config.get("hover_reveal", True):
                self.revealer = Revealer(
                    child=self.update_label,
                    transition_duration=500,
                    transition_type="slide_right",
                )
                self.box.add(self.revealer)
            else:
                self.box.add(self.update_label)

        self.connect("button-press-event", self.on_button_press)

        # Set up a repeater to call the update method at specified intervals
        self.check_update()

        # reusing the fabricator to call specified intervals
        reusable_fabricator.connect("changed", self.should_update)

        if self.config.get("hover_reveal", True):
            # Connect to enter and leave events to toggle the revealer
            bulk_connect(
                self,
                {
                    "enter-notify-event": self._toggle_revealer,
                    "leave-notify-event": self._toggle_revealer,
                },
            )

    def _toggle_revealer(self, *_):
        if hasattr(self, "revealer"):
            self.revealer.set_reveal_child(not self.revealer.get_reveal_child())

    def _build_base_command(self) -> str:
        script = get_relative_path("../assets/scripts/systemupdates.sh")
        command = [f"{script} os={self.config['os']}"]

        # Add terminal option
        terminal = self.config.get("terminal", "kitty")
        command.append(f"--terminal={terminal}")

        if self.config.get("flatpak", False):
            command.append("--flatpak")
        if self.config.get("snap", False):
            command.append("--snap")
        if self.config.get("brew", False):
            command.append("--brew")

        return " ".join(command)

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
        """Update the UI based on the returned update data."""
        try:
            data = json.loads(value)
            total = int(data.get("total", "0"))

            # Update label
            if self.config.get("label", True):
                label_text = (
                    str(total).rjust(2, "0")
                    if self.config.get("pad_zero", True)
                    else str(total)
                )

                # dont show '0' if total is 0 and pad_zero is True
                if total == 0:
                    label_text = str(total)

                self.update_label.set_label(label_text)

            # Update icon
            if self.config.get("show_icon", True):
                icon = (
                    self.config["available_icon"]
                    if total > 0
                    else self.config["no_updates_icon"]
                )
                self.icon.set_label(icon)

            # Tooltip
            self.set_tooltip_text(data.get("tooltip", ""))

            # Auto-hide logic
            if self.config.get("auto_hide", False):
                self.set_visible(total > 0)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(
                f"{Colors.ERROR}[UpdatesWidget] Failed to parse update data: {e}"
            )

    def on_button_press(self, _, event):
        """Trigger a manual update check on click."""
        self.check_update(update=(event.button == 1))
        return True

    @cooldown(1)
    def check_update(self, update=False):
        """Run the update check asynchronously."""
        suffix = " up" if update else ""
        log_msg = (
            "Updating available updates..." if update else "Checking for updates..."
        )
        logger.info(f"{Colors.INFO}[Updates] {log_msg}")

        exec_shell_command_async(
            f"{self.base_command}{suffix}",
            self.update_values,
        )

        return True
