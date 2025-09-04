from fabric.widgets.image import Image

from modules.app_launcher import AppLauncher
from shared.widget_container import ButtonWidget
from utils.config import widget_config


class AppLauncherButton(ButtonWidget):
    """Button widget to launch the application launcher."""

    def __init__(self, **kwargs):
        super().__init__(name="app_launcher_button", **kwargs)

        self.app_launcher = None

        # Get icon from config or use default
        icon = self.config.get("icon", "view-app-grid-symbolic")
        icon_size = self.config.get("icon_size", 16)

        # Set tooltip
        if self.config.get("tooltip", True):
            self.set_tooltip_text("Open Application Launcher")

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
        if self.app_launcher is None:
            self.app_launcher = AppLauncher(widget_config)

        return self.app_launcher

    def on_click(self, *_):
        """Toggle the app launcher visibility."""
        launcher = self._get_or_create_launcher()
        if launcher:
            launcher.toggle()
