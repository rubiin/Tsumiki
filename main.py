from typing import Literal

import setproctitle
from fabric import Application
from fabric.utils import cooldown, exec_shell_command, get_relative_path
from loguru import logger

import utils.functions as helpers
from modules.bar import StatusBar
from utils.colors import Colors
from utils.config import theme_config, widget_config
from utils.constants import APP_CACHE_DIRECTORY, APPLICATION_NAME


@cooldown(2)
@helpers.run_in_thread
def process_and_apply_css(app: Application):
    helpers.check_executable_exists("sass")
    logger.info(f"{Colors.INFO}[Main] Compiling CSS")
    output = exec_shell_command("sass styles/main.scss dist/main.css --no-source-map")

    if output == "":
        logger.info(f"{Colors.INFO}[Main] CSS applied")
        app.set_stylesheet_from_file(get_relative_path("dist/main.css"))
    else:
        logger.exception(f"{Colors.ERROR}[Main]Failed to compile sass!")
        logger.exception(f"{Colors.ERROR}[Main] {output}")
        app.set_stylesheet_from_string("")


general_options = widget_config["general"]
module_options = widget_config["modules"]


if not general_options["debug"]:
    for log in [
        "fabric",
        "widgets",
        "utils",
        "utils.config",
        "modules",
        "services",
    ]:
        logger.disable(log)


if __name__ == "__main__":
    helpers.ensure_directory(APP_CACHE_DIRECTORY)

    # Create the status bar
    bar = StatusBar(widget_config)

    windows = [bar]

    if module_options["app_launcher"]["enabled"]:
        from modules.app_launcher import AppLauncher

        app_launcher = AppLauncher(widget_config)
        windows.append(app_launcher)

    if module_options["notification"]["enabled"]:
        from modules.notification import NotificationPopup

        windows.append(NotificationPopup(widget_config))

    if module_options["screen_corners"]["enabled"]:
        from modules.corners import ScreenCorners

        screen_corners = ScreenCorners(widget_config)

        windows.append(screen_corners)

    if module_options["dock"]["enabled"]:
        from modules.dock import Dock

        dock = Dock(widget_config)

        windows.append(dock)

    if module_options["desktop_clock"]["enabled"]:
        from modules.desktop_clock import DesktopClock

        desktop_clock = DesktopClock(widget_config)

        windows.append(desktop_clock)

    if module_options["osd"]["enabled"]:
        from modules.osd import OSDContainer

        windows.append(OSDContainer(widget_config))

    @Application.action("toggle")
    def toggle(
        item: Literal["bar", "desktop_clock", "dock", "screen_corners", "app_launcher"],
    ):
        """Toggle the visibility of the specified item."""
        match item:
            case "bar":
                bar.toggle()
            case "desktop_clock":
                desktop_clock.toggle()
            case "dock":
                dock.toggle()
            case "screen_corners":
                screen_corners.toggle()
            case "app_launcher":
                app_launcher.toggle()
            case _:
                logger.exception(
                    f"{Colors.ERROR}[Main] Invalid item '{item}' specified for toggle."
                    "Valid options are: bar, desktop_clock, dock, screen_corners, app_launcher."  # noqa: E501
                )

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, windows=windows)

    helpers.copy_theme(theme_config["name"])

    # TODO: add scss monitoring

    process_and_apply_css(app)

    setproctitle.setproctitle(APPLICATION_NAME)

    # Run the application
    app.run()
