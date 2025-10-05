import os

from fabric import Application
from fabric.utils import exec_shell_command, get_relative_path, logger

import utils.functions as helpers
from modules.bar import StatusBar
from utils.colors import Colors
from utils.config import theme_config, widget_config
from utils.constants import APP_DATA_DIRECTORY, APPLICATION_NAME


@helpers.run_in_thread
def process_and_apply_css(app: Application):
    logger.info(f"{Colors.INFO}[Main] Compiling CSS")
    output = exec_shell_command("sass styles/main.scss dist/main.css --no-source-map")

    if output == "":
        logger.info(f"{Colors.INFO}[Main] CSS applied")
        app.set_stylesheet_from_file(get_relative_path("dist/main.css"))
    else:
        logger.exception(f"{Colors.ERROR}[Main]Failed to compile sass!")
        logger.exception(f"{Colors.ERROR}[Main] {output}")
        app.set_stylesheet_from_string("")


general_options = widget_config.get("general", {})
module_options = widget_config.get("modules", {})


def main():
    """Main function to run the application."""

    helpers.ensure_directory(APP_DATA_DIRECTORY)
    helpers.copy_theme(theme_config.get("name", "catppuccin-mocha"))
    helpers.check_executable_exists("sass")

    helpers.set_process_name(APPLICATION_NAME)

    # Initialize the application
    app = Application(APPLICATION_NAME)

    # Create status bars
    StatusBar.create_bars(app, widget_config)

    if module_options.get("notification", {}).get("enabled", False):
        from modules.notification import NotificationPopup

        app.add_window(NotificationPopup(widget_config))

    if module_options.get("overview", {}).get("enabled", False):
        from modules.overview import OverViewOverlay

        app.add_window(OverViewOverlay(widget_config))

    if module_options.get("screen_corners", {}).get("enabled", False):
        from modules.corners import ScreenCorners

        app.add_window(ScreenCorners(widget_config))

    if module_options.get("desktop_quotes", {}).get("enabled", False):
        from modules.desktop_quotes import DesktopQuote

        app.add_window(DesktopQuote(widget_config))

    if module_options.get("activate_linux", {}).get("enabled", False):
        from modules.activate_linux import ActivateLinux

        app.add_window(ActivateLinux(widget_config))

    if module_options.get("app_launcher", {}).get("enabled", False):
        from modules.app_launcher import AppLauncher

        app.add_window(AppLauncher(widget_config))

    if module_options.get("dock", {}).get("enabled", False):
        from modules.dock import Dock

        app.add_window(Dock(widget_config))

    if module_options.get("desktop_clock", {}).get("enabled", False):
        from modules.desktop_clock import DesktopClock

        app.add_window(DesktopClock(widget_config))

    if module_options.get("osd", {}).get("enabled", False):
        from modules.osd import OSDContainer

        app.add_window(OSDContainer(widget_config))

    # Disable verbose logging for non-debug mode

    if not general_options.get("debug", False):
        for log in [
            "fabric",
            "widgets",
            "utils",
            "utils.config",
            "modules",
            "services",
            "config",
        ]:
            logger.disable(log)

    # Start config file watching if enabled
    if general_options.get("auto_reload", True):
        from utils.config_watcher import start_config_watching

        start_config_watching()
        logger.info(f"{Colors.INFO}[Main] Config auto-reload enabled")

    # if general_options.get("monitor_styles", False):
    #     main_css_file = monitor_file(get_relative_path("styles"))
    #     common_css_file = monitor_file(get_relative_path("styles/common"))
    #     main_css_file.connect("changed", lambda *_: process_and_apply_css(app))
    #     common_css_file.connect("changed", lambda *_: process_and_apply_css(app))
    # else:
    process_and_apply_css(app)

    logger.info(f"{Colors.INFO}[Main] Starting {APPLICATION_NAME}...")
    logger.info(f"Starting shell... pid:{os.getpid()}")

    @Application.action()
    def toggle_window(name: str):
        logger.info("[Main] Toggling window", name)
        available_windows = [window.get_name() for window in app.get_windows()]

        if name not in available_windows:
            logger.warning(
                f"{Colors.WARNING}[Main] No window named '{name}' found!",
                f"Available windows: {available_windows}",
            )
            return False

        window = filter(lambda w: w.get_name() == name, app.get_windows())
        if window:
            window = next(window)
            window.toggle()

        return False

    # Run the application
    app.run()


if __name__ == "__main__":
    main()
