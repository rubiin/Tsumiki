"""
Simple configuration file watcher for auto-reloading Tsumiki when config files change.
"""

import os
import subprocess

from fabric.utils import get_relative_path
from gi.repository import Gio, GLib
from loguru import logger

from utils.colors import Colors
from utils.constants import APPLICATION_NAME


class ConfigWatcher:
    """Simple file watcher that monitors config files and restarts Tsumiki."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.monitors: list[Gio.FileMonitor] = []
        self.restart_pending = False

        self.root_dir = get_relative_path("..")

        self.init_script = f"{self.root_dir}/init.sh"

        # Files to monitor
        config_files = [
            f"{self.root_dir}/config.json",
            f"{self.root_dir}/config.toml",
            f"{self.root_dir}/theme.json",
        ]

        self.RESTART_DELAY_MS = 1500

        # Set up monitors for existing files
        for config_file in config_files:
            if os.path.exists(config_file):
                self._monitor_file(config_file)

    def _monitor_file(self, file_path: str):
        """Monitor a single file for changes."""
        try:
            file_obj = Gio.File.new_for_path(file_path)
            monitor = file_obj.monitor_file(Gio.FileMonitorFlags.NONE, None)
            monitor.connect("changed", self.on_file_changed, file_path)
            self.monitors.append(monitor)
            logger.info(
                f"{Colors.INFO}[ConfigWatcher] Monitoring {os.path.basename(file_path)}"
            )
        except Exception as e:
            logger.exception(
                f"{Colors.ERROR}[ConfigWatcher] Failed to monitor {file_path}: {e}"
            )

    def on_file_changed(self, monitor, file, other_file, event_type, file_path: str):
        """Handle file change events."""
        if (
            event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT
            and not self.restart_pending
        ):
            self.restart_pending = True
            logger.info(
                (
                    f"{Colors.INFO}[ConfigWatcher] Config changed: "
                    f"{os.path.basename(file_path)}"
                )
            )

            # Delay restart slightly to handle multiple rapid changes
            GLib.timeout_add(self.RESTART_DELAY_MS, self._restart_tsumiki)

    def _restart_tsumiki(self):
        """Restart Tsumiki using the init script."""
        try:
            logger.info(
                f"{Colors.INFO}[ConfigWatcher] Restarting {APPLICATION_NAME.title()}..."
            )

            # Run restart in background to avoid blocking
            subprocess.Popen(
                [self.init_script, "-restart"],
                cwd=os.path.dirname(self.init_script),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception as e:
            logger.exception(f"{Colors.ERROR}[ConfigWatcher] Failed to restart: {e}")

        return False  # Don't repeat

    def stop(self):
        """Stop monitoring files."""
        for monitor in self.monitors:
            monitor.cancel()
        self.monitors.clear()


# Global watcher instance
_watcher = None


def start_config_watching():
    """Start watching config files for changes."""
    global _watcher
    if _watcher is None:
        _watcher = ConfigWatcher()


def stop_config_watching():
    """Stop watching config files."""
    global _watcher
    if _watcher:
        _watcher.stop()
        _watcher = None
