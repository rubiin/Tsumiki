from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from services.power_profile import PowerProfilesService
from shared.buttons import HoverButton, QSChevronButton
from shared.submenu import QuickSubMenu
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


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
                    icon=profile["icon"],
                    props={
                        "style_classes": [
                            "panel-font-icon",
                        ],
                    },
                ),
                Label(
                    label=profile["name"],
                    style_classes="submenu-item-label",
                ),
            ),
        )

        self.power_profile_service = PowerProfilesService()
        self.add(self.box)

        self.connect(
            "button-press-event",
            lambda *_: self.power_profile_service.set_power_profile(key),
        )
        self.set_active(active)

    def set_active(self, active: str):
        style_context = self.box.get_style_context()
        if self.key == active:
            style_context.add_class("active")
        else:
            style_context.remove_class("active")

class PowerProfileSubMenu(QuickSubMenu):
    """A submenu to display power profile options."""

    def __init__(self, **kwargs):
        self.client = PowerProfilesService()
        self.profiles = self.client.power_profiles

        self.profile_items = None
        self.scan_button = HoverButton()

        self.profile_box = Box(
            orientation="v",
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
                    key=key, profile=profile, active=self.client.get_current_profile()
                )
                for key, profile in self.profiles.items()
            ]

            self.profile_box.children = self.profile_items

        # Update items when profile changes
        self.client.connect("changed", self.on_profile_changed)

    def on_profile_changed(self, *_):
        for item in self.profile_items:
            item.set_active(self.client.get_current_profile())


class PowerProfileToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=text_icons["powerprofiles"]["power-saver"],
            action_label="Power Saver",
            submenu=submenu,
            **kwargs,
        )
        self.client = PowerProfilesService()
        self.update_action_button()
        self.set_active_style(True)
        self.action_button.set_sensitive(False)

        self.client.connect(
            "changed",
            self.update_action_button,
        )

    def unslug(self, text: str) -> str:
        return " ".join(word.capitalize() for word in text.split("-"))

    def update_action_button(self, *_):
        self.active_pfl = self.client.get_current_profile()

        icon = self.client.get_profile_icon(self.active_pfl)

        self.action_icon.set_label(icon)
        self.set_action_label(self.unslug(self.active_pfl))
