import setproctitle
from fabric import Application
from fabric.utils import exec_shell_command, get_relative_path, monitor_file
from loguru import logger

import utils.functions as helpers
from modules.bar import StatusBar
from modules.notification_pop_up import NotificationPopup
from modules.osd import OSDContainer
from utils.colors import Colors
from utils.config import widget_config
from utils.constants import APP_CACHE_DIRECTORY, APPLICATION_NAME
from utils.exceptions import ExecutableNotFoundError
from widgets.corners import ScreenCorners


def process_and_apply_css(app: Application):
    if not helpers.executable_exists("sass"):
        raise ExecutableNotFoundError(
            "sass"
        )  # Raise an error if sass is not found and exit the application

    logger.info(f"{Colors.INFO}[Main] Compiling CSS")
    output = exec_shell_command("sass styles/main.scss dist/main.css --no-source-map")

    if output == "":
        logger.info(f"{Colors.INFO}[Main] CSS applied")
        app.set_stylesheet_from_file(get_relative_path("dist/main.css"))
    else:
        app.set_stylesheet_from_string("")
        logger.error(f"{Colors.ERROR}[Main]Failed to compile sass!")


for log in [
    "fabric.hyprland.widgets",
    "fabric.audio.service",
    "fabric.bluetooth.service",
    "fabric.audio",
    "fabric.widgets.wayland",
]:
    logger.disable(log)


if __name__ == "__main__":
    # Create the status bar
    bar = StatusBar()
    notifications = NotificationPopup(widget_config)

    windows = [notifications, bar]

    if widget_config["general"]["screen_corners"]:
        windows.append(ScreenCorners())

    if widget_config["osd"]["enabled"]:
        windows.append(OSDContainer(widget_config))

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, windows=windows)

    setproctitle.setproctitle(APPLICATION_NAME)

    helpers.ensure_dir_exists(APP_CACHE_DIRECTORY)

    helpers.copy_theme(widget_config["theme"]["name"])

    # Monitor styles folder for changes
    main_css_file = monitor_file(get_relative_path("styles"))
    common_css_file = monitor_file(get_relative_path("styles/common"))
    main_css_file.connect("changed", lambda *_: process_and_apply_css(app))
    common_css_file.connect("changed", lambda *_: process_and_apply_css(app))

    process_and_apply_css(app)

    # Run the application
    app.run()
