from fabric import Application
from fabric.utils import (
    GLib,
    exec_shell_command,
    get_relative_path,
    idle_add,
    logger,
    monitor_file,
    os,
)

import utils.functions as helpers
from modules.bar import Bar
from utils.colors import Colors
from utils.config import tsumiki_config
from utils.constants import APP_DATA_DIRECTORY, APPLICATION_NAME, CSS_PATH


def process_and_apply_css(app: Application):
    """Compile and apply CSS in background thread."""

    @helpers.run_in_thread
    def _compile():
        logger.info(f"{Colors.INFO}[Main] Compiling CSS")
        output = exec_shell_command(f"sass styles/main.scss {CSS_PATH} --no-source-map")

        if output == "":
            logger.info(f"{Colors.INFO}[Main] CSS applied")
            idle_add(lambda: app.set_stylesheet_from_file(get_relative_path(CSS_PATH)))
        else:
            logger.exception(f"{Colors.ERROR}[Main]Failed to compile sass!")
            logger.exception(f"{Colors.ERROR}[Main] {output}")

            idle_add(lambda: app.set_stylesheet_from_string(""))

    _compile()


def main():
    """Main function to run the application."""
    # Defer config loading until main() is called

    general_options = tsumiki_config.get("general", {})
    module_options = tsumiki_config.get("modules", {})

    helpers.check_executable_exists("sass")
    helpers.ensure_directory(APP_DATA_DIRECTORY)

    # Check if matugen is enabled and generate palette
    style_config = tsumiki_config.get("styling", {})
    matugen_config = style_config.get("matugen", {})
    if matugen_config.get("enabled", False):
        from services import matugen_service

        matugen_service.generate_sync()
    else:
        helpers.copy_themev2(
            style_config.get("theme_name", "catppuccin-mocha"),
            style_config.get("mode", "dark"),
        )

    helpers.set_process_name(APPLICATION_NAME)

    # Initialize the application
    app = Application(APPLICATION_NAME)

    # Create status bars
    Bar.create_bars(app, tsumiki_config)

    if module_options.get("notification", {}).get("enabled", False):
        from modules.notification import NotificationPopup

        app.add_window(NotificationPopup(tsumiki_config))

    if module_options.get("overview", {}).get("enabled", False):
        from modules.overview import OverViewOverlay

        logger.info("[Main] Adding overview module")

        app.add_window(OverViewOverlay(tsumiki_config))

    if module_options.get("screen_corners", {}).get("enabled", False):
        from modules.corners import ScreenCorners

        app.add_window(ScreenCorners(tsumiki_config))

    if module_options.get("desktop_quotes", {}).get("enabled", False):
        from modules.desktop_quotes import DesktopQuote

        app.add_window(DesktopQuote(tsumiki_config))

    if module_options.get("activate_linux", {}).get("enabled", False):
        from modules.activate_linux import ActivateLinux

        app.add_window(ActivateLinux(tsumiki_config))

    if module_options.get("app_launcher", {}).get("enabled", False):
        from modules.app_launcher import AppLauncher

        app.add_window(AppLauncher(tsumiki_config))

    if module_options.get("dock", {}).get("enabled", False):
        from modules.dock import Dock

        app.add_window(Dock(tsumiki_config))

    if module_options.get("desktop_clock", {}).get("enabled", False):
        from modules.desktop_clock import DesktopClock

        app.add_window(DesktopClock(tsumiki_config))

    if module_options.get("osd", {}).get("enabled", False):
        from modules.osd import OSDContainer

        app.add_window(OSDContainer(tsumiki_config))

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
    if general_options.get("auto_restart", True):
        from utils.config_watcher import start_config_watching

        start_config_watching()

    if general_options.get("monitor_styles", False):
        main_css_file = monitor_file(get_relative_path("styles"))
        common_css_file = monitor_file(get_relative_path("styles/common"))
        css_reload_timeout_id = 0
        css_reload_debounce_ms = 200

        def schedule_css_reload(*_):
            nonlocal css_reload_timeout_id
            if css_reload_timeout_id:
                GLib.source_remove(css_reload_timeout_id)

            css_reload_timeout_id = GLib.timeout_add(
                css_reload_debounce_ms,
                lambda: (process_and_apply_css(app), False),
            )

        main_css_file.connect("changed", schedule_css_reload)
        common_css_file.connect("changed", schedule_css_reload)

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

        window = next((w for w in app.get_windows() if w.get_name() == name), None)
        if window:
            window.toggle()

        return False

    @Application.action()
    def open_inspector():
        app.open_inspector()

        return False

    # Run the application
    app.run()


if __name__ == "__main__":
    main()
