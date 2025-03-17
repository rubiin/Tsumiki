import setproctitle
from fabric import Application
from fabric.utils import cooldown, exec_shell_command, get_relative_path, monitor_file
from loguru import logger

import utils.functions as helpers
from modules import NotificationPopup, OSDContainer, StatusBar
from utils import (
    APP_CACHE_DIRECTORY,
    APPLICATION_NAME,
    Colors,
    ExecutableNotFoundError,
    widget_config,
)


@cooldown(2)
@helpers.run_in_thread
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
        print(output)
        app.set_stylesheet_from_string("")
        logger.error(f"{Colors.ERROR}[Main]Failed to compile sass!")


general_options = widget_config["general"]

if not general_options["debug"]:
    for log in [
        "fabric",
        "widgets",
        "utils",
        "modules",
        "services",
    ]:
        logger.disable(log)


if __name__ == "__main__":
    # Create the status bar
    bar = StatusBar(widget_config)
    notifications = NotificationPopup(widget_config)

    windows = [notifications, bar]

    if (
        general_options["screen_corners"]
        and general_options["screen_corners"]["enabled"]
    ):
        from widgets.corners import ScreenCorners

        windows.append(ScreenCorners(general_options["screen_corners"]["size"]))

    if general_options["desktop_clock"] and general_options["desktop_clock"]["enabled"]:
        from widgets.desktop_clock import DesktopClock

        windows.append(
            DesktopClock(
                general_options["desktop_clock"]["date_format"],
                general_options["desktop_clock"]["anchor"],
            )
        )

    if widget_config["osd"]["enabled"]:
        windows.append(OSDContainer(widget_config))

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, windows=windows)

    # Monitor styles folder for changes
    if general_options["debug"]:
        main_css_file = monitor_file(get_relative_path("styles"))
        common_css_file = monitor_file(get_relative_path("styles/common"))
        main_css_file.connect("changed", lambda *_: process_and_apply_css(app))
        common_css_file.connect("changed", lambda *_: process_and_apply_css(app))
    else:
        process_and_apply_css(app)

    setproctitle.setproctitle(APPLICATION_NAME)

    helpers.ensure_dir_exists(APP_CACHE_DIRECTORY)

    helpers.copy_theme(widget_config["theme"]["name"])

    # Run the application
    app.run()
