import gc
import sys
import tracemalloc

import setproctitle
from fabric import Application
from fabric.utils import exec_shell_command, get_relative_path
from gi.repository import GLib, Gtk
from loguru import logger

import utils.functions as helpers
from modules.bar import StatusBar
from utils.colors import Colors
from utils.config import theme_config, widget_config
from utils.constants import APP_CACHE_DIRECTORY, APPLICATION_NAME

tracemalloc.start(10)  # Track 10 frames for better traces

baseline_snapshot = None


def is_relevant_frame(frame):
    # Only include frames from your project (not site-packages or standard lib)
    return "site-packages" not in frame.filename and "lib/python" not in frame.filename


baseline_snapshot = None


def print_gtk_object_growth():
    gc.collect()

    all_objects = gc.get_objects()
    gtk_widgets = [obj for obj in all_objects if isinstance(obj, Gtk.Widget)]

    total_size = 0
    for i, w in enumerate(gtk_widgets, 1):
        size = sys.getsizeof(w)
        total_size += size
        try:
            name = w.get_name() if hasattr(w, "get_name") else "N/A"
        except Exception:
            name = "N/A"
        print(f"{i}: Type={type(w).__name__}, Name={name}, Approx size={size} bytes")

    print(
        f"Found {len(gtk_widgets)} GTK widgets in memory. "
        f"Total approx size of GTK widgets: {total_size} bytes "
        f"({total_size / (1024 * 1024):.2f} MB)"
    )

    return True  # Schedule to repeat every 60s


def take_baseline_snapshot():
    global baseline_snapshot
    baseline_snapshot = tracemalloc.take_snapshot()
    logger.info("[Memory] Baseline snapshot taken")
    return False  # Only run once


def compare_to_baseline():
    if baseline_snapshot is None:
        logger.warning("[Memory] Baseline not yet available, skipping comparison")
        return True

    new_snapshot = tracemalloc.take_snapshot()

    top_stats = new_snapshot.compare_to(baseline_snapshot, "lineno")

    print("\n[Memory] Top 10 allocation differences (filtered):")
    for i, stat in enumerate(top_stats[:10], 1):
        print(f"{i}. {stat}")
    total = sum(stat.size for stat in top_stats[:10])
    print(f"\n[Memory] Total diff size (top 10): {total / 1024:.1f} KiB\n")

    return True  # Schedule to repeat every 60s


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

    # if module_options["app_launcher"]["enabled"]:
    #     from modules.app_launcher import AppLauncher

    #     app_launcher = AppLauncher(widget_config)
    #     windows.append(app_launcher)

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

    # # Take baseline snapshot shortly after startup
    # GLib.timeout_add_seconds(5, take_baseline_snapshot)
    # # Schedule filtered snapshot comparison every 5 seconds
    GLib.timeout_add_seconds(10, print_gtk_object_growth)
    # Run the application
    app.run()


if __name__ == "__main__":
    main()
