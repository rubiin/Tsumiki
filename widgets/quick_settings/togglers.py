from fabric.widgets.box import Box
from fabric.widgets.label import Label

from services import notification_service
from shared.button_toggle import CommandSwitcher
from shared.buttons import HoverButton
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


class QuickSettingToggler(CommandSwitcher):
    """A button widget to toggle a command."""

    def __init__(
        self,
        command: str,
        name: str,
        enabled_icon: str,
        disabled_icon: str,
        args="",
        **kwargs,
    ):
        super().__init__(
            command,
            enabled_icon,
            disabled_icon,
            name,
            args=args,
            label=True,
            tooltip=False,
            interval=1000,
            style_classes=["quicksettings-toggler"],
            **kwargs,
        )


class HyprIdleQuickSetting(QuickSettingToggler):
    """A button to toggle the hyper idle mode."""

    def __init__(self, popup, **kwargs):
        super().__init__(
            command="hypridle",
            enabled_icon="",
            disabled_icon="",
            name="quicksettings-togglebutton",
        )
        self.connect("clicked", lambda *_: popup.hide_popover())


class NotificationQuickSetting(HoverButton):
    """A button to toggle the notification."""

    def __init__(self, popup, **kwargs):
        super().__init__(
            name="quicksettings-togglebutton",
            style_classes=["quicksettings-toggler"],
        )

        self.popup = popup

        self.notification_label = Label(
            label="Noisy",
        )
        self.notification_icon = nerd_font_icon(
            icon=text_icons["notifications"]["noisy"],
            props={"style_classes": ["panel-font-icon"]},
        )

        self.children = Box(
            orientation="h",
            spacing=10,
            style="padding: 5px;",
            children=(
                self.notification_icon,
                self.notification_label,
            ),
        )

        notification_service.connect("dnd", self.toggle_notification)

        self.connect("clicked", self.on_click)

        self.toggle_notification(None, notification_service.dont_disturb)

    def on_click(self, *_):
        """Toggle the notification."""
        notification_service.dont_disturb = not notification_service.dont_disturb
        self.popup.hide_popover()

    def toggle_notification(self, _, value: bool, *args):
        """Toggle the notification."""

        self.toggle_css_class(
            "active",
            not value,
        )

        if value:
            self.notification_label.set_label("Quiet")
            self.notification_icon.set_label(text_icons["notifications"]["silent"])

        else:
            self.notification_label.set_label("Noisy")
            self.notification_icon.set_label(text_icons["notifications"]["noisy"])
