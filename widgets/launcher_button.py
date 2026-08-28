from fabric.widgets.image import Image

from shared.widget_container import ButtonWidget
from utils.i18n import _


class LauncherButton(ButtonWidget):
    """Button widget to launch the application launcher."""

    def __init__(self, **kwargs):
        super().__init__(name="launcher_button", **kwargs)

        self.launcher = None

        # Get icon from config or use default
        icon = self.config.get("icon", "view-app-grid-symbolic")
        icon_size = self.config.get("icon_size", 16)

        # Set tooltip
        self.set_tooltip_if_enabled(_("widget.launcher_button.tooltip"), default=True)

        # Create the button content
        self.container_box.children = [
            Image(
                icon_name=icon,
                icon_size=icon_size,
            )
        ]

        # Connect click event
        self.connect("clicked", self.on_click)

    def _get_or_create_launcher(self):
        """Get or create the app launcher instance."""
        from modules.launcher import Launcher
        from utils.config import tsumiki_config

        if self.launcher is None:
            self.launcher = Launcher(tsumiki_config)

        return self.launcher

    def on_click(self, *_):
        """Toggle the app launcher visibility."""
        launcher = self._get_or_create_launcher()
        if launcher:
            launcher.toggle()
