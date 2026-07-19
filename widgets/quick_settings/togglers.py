from services import notification_service
from shared.button_toggle import CommandSwitcher
from shared.buttons import HoverButton
from utils.icons import get_text_icon
from widgets.quick_settings.components import QuickSettingsIconLabelRow


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
            enabled_icon=get_text_icon("idle.enabled"),
            disabled_icon=get_text_icon("idle.disabled"),
            name="quicksettings-togglebutton",
            **kwargs,
        )
        self.connect("clicked", lambda *_: popup.hide_popover())


class NotificationQuickSetting(HoverButton):
    """A button to toggle the notification."""

    def __init__(self, popup, **kwargs):
        super().__init__(
            name="quicksettings-togglebutton",
            style_classes=["quicksettings-toggler"],
            **kwargs,
        )

        self.popup = popup

        self.row = QuickSettingsIconLabelRow(
            icon=get_text_icon("notifications.noisy"),
            label="Noisy",
            row_classes=["quicksettings-toggle-row"],
        )

        self.notification_icon = self.row.icon
        self.notification_label = self.row.label

        self.children = self.row

        self._register_handler(
            notification_service,
            notification_service.connect("dnd", self.toggle_notification),
        )

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
            self.notification_icon.set_label(get_text_icon("notifications.silent"))

        else:
            self.notification_label.set_label("Noisy")
            self.notification_icon.set_label(get_text_icon("notifications.noisy"))
