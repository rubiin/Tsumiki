from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from services import power_pfl_service
from shared.buttons import HoverButton, QSChevronButton
from shared.submenu import QuickSubMenu
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


def icon_name_to_icon(icon_name: str) -> str:
    """Convert icon name to actual icon."""
    icon_map = {"power-saver": "󰌪", "performance": "󰓅", "balanced": "󰒂"}
    return icon_map.get(icon_name, "󰌪")


class PowerProfileItem(Button):
    """A button to display the power profile."""

    def __init__(
        self,
        key,
        profile,
        active,
        **kwargs,
    ):
        super().__init__(
            style_classes="submenu-button power-profile",
            **kwargs,
        )
        self.profile = profile
        self.key = key
        self.box = Box(
            orientation="h",
            spacing=10,
            children=(
                nerd_font_icon(
                    icon=icon_name_to_icon(profile),
                    props={
                        "style_classes": [
                            "panel-font-icon",
                        ],
                    },
                ),
                Label(
                    label=profile,
                    style_classes="submenu-item-label",
                ),
            ),
        )

        self.add(self.box)

        self.connect(
            "button-press-event",
            self._handle_click,
        )
        self.set_active(active)

    def _handle_click(self, *_):
        print(f"Setting power profile to {self.profile}")
        power_pfl_service.active_profile = self.profile
        return True

    def set_active(self, active: str):
        style_context = self.box.get_style_context()
        if self.key == active:
            style_context.add_class("active")
        else:
            style_context.remove_class("active")


class PowerProfileSubMenu(QuickSubMenu):
    """A submenu to display power profile options."""

    def __init__(self, **kwargs):
        self.profiles = [profile["Profile"] for profile in power_pfl_service.profiles]

        self.profile_items = None
        self.scan_button = HoverButton()

        self.profile_box = Box(
            orientation="v",
            name="power-profile-container",
            spacing=8,
            style="margin: 5px 0;",
        )

        super().__init__(
            title="Power profiles",
            title_icon=text_icons["powerprofiles"]["power-saver"],
            scan_button=self.scan_button,
            child=self.profile_box,
            **kwargs,
        )

        self.revealer.connect(
            "notify::child-revealed",
            self.on_child_revealed,
        )

    def on_child_revealed(self, *_):
        """Callback when the submenu is revealed."""

        if self.profile_items is None:
            self.profile_items = [
                PowerProfileItem(
                    key=key, profile=profile, active=power_pfl_service.active_profile
                )
                for key, profile in enumerate(self.profiles)
            ]

            self.profile_box.children = self.profile_items

        # Update items when profile changes
        power_pfl_service.connect("changed", self.on_profile_changed)

    def on_profile_changed(self, *_):
        for item in self.profile_items:
            item.set_active(power_pfl_service.active_profile)


class PowerProfileToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=text_icons["powerprofiles"]["power-saver"],
            action_label="Power Saver",
            submenu=submenu,
            **kwargs,
        )

        self.update_action_button()
        self.set_active_style(True)
        self.action_button.set_sensitive(False)

        power_pfl_service.connect(
            "changed",
            self.update_action_button,
        )

    def unslug(self, text: str) -> str:
        return " ".join(word.capitalize() for word in text.split("-"))

    def update_action_button(self, *_):
        self.action_icon.set_label(icon_name_to_icon(power_pfl_service.active_profile))
        self.set_action_label(self.unslug(power_pfl_service.active_profile))
