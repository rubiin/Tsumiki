import traceback

import setproctitle
from fabric import Application
from fabric.utils import exec_shell_command, get_relative_path
from gi.repository import GLib
from loguru import logger

import utils.functions as helpers
from modules.bar import StatusBar
from utils.colors import Colors
from utils.config import theme_config, widget_config
from utils.constants import APP_CACHE_DIRECTORY, APPLICATION_NAME

# Manually map log levels to readable names
LOG_LEVEL_NAMES = {
    GLib.LogLevelFlags.LEVEL_ERROR: "ERROR",
    GLib.LogLevelFlags.LEVEL_CRITICAL: "CRITICAL",
    GLib.LogLevelFlags.LEVEL_WARNING: "WARNING",
    GLib.LogLevelFlags.LEVEL_MESSAGE: "MESSAGE",
    GLib.LogLevelFlags.LEVEL_INFO: "INFO",
    GLib.LogLevelFlags.LEVEL_DEBUG: "DEBUG",
}


def take_snapshot():
    import tracemalloc

    tracemalloc.start()
    # Later in code
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    print("[Top 10 Memory Lines]")
    for stat in top_stats[:10]:
        print(stat)


def log_handler(domain, level, message):
    level_name = LOG_LEVEL_NAMES.get(
        GLib.LogLevelFlags(
            level & ~GLib.LogLevelFlags.FLAG_FATAL & ~GLib.LogLevelFlags.FLAG_RECURSION
        ),
        f"UNKNOWN({level})",
    )
    print(f"\n[{domain or 'Default'}] {level_name}: {message}")
    traceback.print_stack()


# Set log levels
log_levels = (
    GLib.LogLevelFlags.LEVEL_ERROR
    | GLib.LogLevelFlags.LEVEL_CRITICAL
    | GLib.LogLevelFlags.LEVEL_WARNING
    | GLib.LogLevelFlags.LEVEL_MESSAGE
    | GLib.LogLevelFlags.LEVEL_INFO
    | GLib.LogLevelFlags.LEVEL_DEBUG
)

# Common GTK/GLib log domains
domains = [None, "Gtk", "GLib", "GLib-GObject", "Gdk", "Pango"]

for domain in domains:
    GLib.log_set_handler(domain, log_levels, log_handler)


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


def main():
    """Main function to run the application."""
    logger.info(f"{Colors.INFO}[Main] Starting {APPLICATION_NAME}...")

    helpers.ensure_directory(APP_CACHE_DIRECTORY)
    helpers.copy_theme(theme_config["name"])

    # Create the status bar
    bar = StatusBar(widget_config)

    windows = [bar]

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

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, windows=windows)

    setproctitle.setproctitle(APPLICATION_NAME)
    process_and_apply_css(app)

    GLib.timeout_add_seconds(120, take_snapshot)

    # Run the application
    app.run()


if __name__ == "__main__":
    main()
