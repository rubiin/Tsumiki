from fabric.widgets.label import Label

import utils.functions as helpers
from utils.widget_utils import (
    nerd_font_icon,
    reusable_fabricator,
)

from .widget_container import ButtonWidget


class CommandSwitcher(ButtonWidget):
    """A button widget to toggle a command.
    Useful for making services with two states."""

    def __init__(
        self,
        command: str,
        enabled_icon: str,
        disabled_icon: str,
        name: str,
        label=True,
        args="",
        tooltip=True,
        style_classes="",
        **kwargs,
    ):
        self.command = command
        self.full_command = f"{command} {args}"

        super().__init__(
            name=name,
            **kwargs,
        )

        helpers.check_executable_exists(self.command)

        self.add_style_class(style_classes)

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.label = label
        self.tooltip = tooltip

        self.icon = nerd_font_icon(
            icon=enabled_icon,
            props={"style_classes": "panel-font-icon"},
        )

        self.box.add(
            self.icon,
        )

        if self.label:
            self.label_text = Label(
                label="Enabled",
                style_classes="panel-text",
            )
            self.box.add(self.label_text)

        self.connect("clicked", self.handle_click)

        # reusing the fabricator to call specified intervals
        reusable_fabricator.connect("changed", self.update_ui)
        self.update_ui()  # Initial update

    # toggle the command on click
    def handle_click(self, *_):
        helpers.toggle_command(
            self.command,
            full_command=self.full_command,
        )
        self.update_ui()
        return True

    def update_ui(self, *_):
        is_running = helpers.is_app_running(self.command)

        self.set_has_class("active", is_running)

        label = "Enabled" if is_running else "Disabled"

        if self.label:
            self.label_text.set_label(label)

        self.icon.set_label(self.enabled_icon if is_running else self.disabled_icon)

        if self.tooltip:
            self.set_tooltip_text(f"{self.command} {label.lower()}")

        return True
