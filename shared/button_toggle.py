from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.label import Label

import utils.functions as helpers
from utils import ExecutableNotFoundError
from utils.widget_utils import (
    text_icon,
    util_fabricator,
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
        icon_size: str = "16px",
        label=True,
        tooltip=True,
        config=None,
        style_classes: str = "",
        **kwargs,
    ):
        self.command = command
        self.command_without_args = self.command.split(" ")[0]  # command without args

        super().__init__(
            config,
            name=name,
            **kwargs,
        )

        if not helpers.executable_exists(self.command_without_args):
            raise ExecutableNotFoundError(self.command_without_args)

        self.add_style_class(style_classes)

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.label = label
        self.tooltip = tooltip

        self.icon = text_icon(
            icon=enabled_icon,
            size=icon_size,
            props={"style_classes": "panel-icon"},
        )

        self.label_text = Label(
            visible=False,
            label="Enabled",
            style_classes="panel-text",
        )

        self.box = Box(
            children=[self.icon, self.label_text],
        )

        self.add(self.box)

        self.connect("clicked", self.toggle)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", lambda *_: self.update_ui())

    def toggle(self, *_):
        is_app_running = helpers.is_app_running(self.command_without_args)
        if is_app_running:
            exec_shell_command_async(
                f"pkill {self.command_without_args}", lambda *_: None
            )
        else:
            exec_shell_command_async(f"bash -c '{self.command}&'", lambda *_: None)
        self.update_ui(is_app_running)
        return True

    def update_ui(self, is_app_running: bool | None = None):
        if is_app_running is None:
            is_app_running = helpers.is_app_running(self.command_without_args)

        if is_app_running:
            self.add_style_class("active")
        else:
            self.remove_style_class("active")

        if self.label:
            self.label_text.set_visible(True)
            self.label_text.set_label("Enabled" if is_app_running else "Disabled")

        self.icon.set_label(self.enabled_icon if is_app_running else self.disabled_icon)

        if self.tooltip:
            self.set_tooltip_text(
                f"{self.command_without_args} enabled"
                if is_app_running
                else f"{self.command_without_args} disabled",
            )
        return True
