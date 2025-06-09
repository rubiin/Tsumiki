from fabric.utils import cooldown, exec_shell_command_async

from shared.buttons import QSChevronButton, ScanButton
from shared.submenu import QuickSubMenu
from utils.functions import is_app_running, toggle_command
from utils.icons import text_icons
from utils.widget_utils import (
    create_scale,
    util_fabricator,
)


class HyprSunsetSubMenu(QuickSubMenu):
    """A submenu to display application-specific audio controls."""

    def __init__(self, **kwargs):
        # Create refresh button first since parent needs it
        self.scan_button = ScanButton(visible=False)

        self.scale = create_scale(
            name="hyprsunset-scale",
            increments=(100, 100),
            max_value=10000,
            min_value=1000,
            value=2600,
        )

        super().__init__(
            title="HyprSunset",
            title_icon=text_icons["nightlight"]["enabled"],
            name="hyprsunset-sub-menu",
            scan_button=self.scan_button,
            child=self.scale,
            **kwargs,
        )

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            # reusing the fabricator to call specified intervals
            util_fabricator.connect("changed", self.update_scale)

    @cooldown(0.1)
    def on_scale_move(self, _, __, moved_pos):
        exec_shell_command_async(
            f"hyprctl hyprsunset temperature {int(moved_pos)}",
            lambda *_: self.update_ui(int(moved_pos)),
        )
        return True

    def update_scale(self, *_):
        if is_app_running("hyprsunset"):
            self.scale.set_sensitive(True)
            exec_shell_command_async(
                "hyprctl hyprsunset temperature",
                self.update_ui,
            )
        else:
            self.scale.set_sensitive(False)

    def update_ui(self, moved_pos):
        # Update the scale value based on the current temperature
        sanitized_value = (
            float(moved_pos.strip("\n").strip(""))
            if isinstance(moved_pos, str)
            else moved_pos
        )
        # adj = self.scale.get_adjustment()
        # print("HyprSunsetSubMenu: Current temperature", sanitized_value)
        # print(f"HyprSunset scale: {self.scale.get_name()}")
        # print("HyprSunsetSubMenu: lower temperature", adj.get_lower())
        # print("HyprSunsetSubMenu: upper temperature", adj.get_upper())
        self.scale.set_value(float(sanitized_value))
        self.scale.set_tooltip_text(f"{sanitized_value}K")


class HyprSunsetToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon="redshift-status-off",
            pixel_size=20,
            action_label="Enabled",
            submenu=submenu,
            **kwargs,
        )
        self.action_button.set_sensitive(True)

        self.connect("action-clicked", self.on_action)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", self.update_action_button)

    def on_action(self, *_):
        """Handle the action button click event."""
        toggle_command(
            "hyprsunset",
            full_command="hyprsunset -t 2600",
        )
        return True

    def update_action_button(self, *_):
        self.is_running = is_app_running("hyprsunset")

        if self.is_running:
            self.action_icon.set_from_icon_name(
                "redshift-status-on-symbolic", self.pixel_size
            )
            self.action_label.set_label("Enabled")
            self.set_active_style(True)
        else:
            self.action_icon.set_from_icon_name(
                "redshift-status-off-symbolic", self.pixel_size
            )
            self.action_label.set_label("Disabled")
            self.set_active_style(False)
