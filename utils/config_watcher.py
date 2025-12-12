"""
Simple configuration file watcher for auto-reloading Tsumiki when config files change.
"""

import os
import subprocess

from fabric.utils import get_relative_path, logger
from gi.repository import Gio, GLib

from utils.colors import Colors
from utils.constants import APPLICATION_NAME

# Constants
_RESTART_DELAY_MS = 1500
_CONFIG_FILES = frozenset(("config.toml", "theme.toml"))


class ConfigWatcher:
    """Simple file watcher that monitors config files and restarts Tsumiki."""

    __slots__ = (
        "_initialized",
        "_restart_pending",
        "init_script",
        "monitors",
        "root_dir",
    )

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.monitors: list[Gio.FileMonitor] = []
        self._restart_pending = False
        self.root_dir = get_relative_path("..")
        self.init_script = f"{self.root_dir}/init.sh"

        # Set up monitors for existing config files
        for filename in _CONFIG_FILES:
            config_path = f"{self.root_dir}/{filename}"
            if os.path.exists(config_path):
                self._monitor_file(config_path)

        self._initialized = True

    def _monitor_file(self, file_path: str):
        """Monitor a single file for changes."""
        try:
            file_obj = Gio.File.new_for_path(file_path)
            monitor = file_obj.monitor_file(Gio.FileMonitorFlags.NONE, None)
            monitor.connect("changed", self._on_file_changed)
            self.monitors.append(monitor)
            logger.info(
                f"{Colors.INFO}[ConfigWatcher] Monitoring {os.path.basename(file_path)}"
            )
        except Exception as e:
            logger.exception(
                f"{Colors.ERROR}[ConfigWatcher] Failed to monitor {file_path}: {e}"
            )

    def _on_file_changed(self, monitor, file, other_file, event_type):
        """Handle file change events."""
        if (
            event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT
            and not self._restart_pending
        ):
            self._restart_pending = True
            logger.info(
                f"{Colors.INFO}[ConfigWatcher] Config changed: {file.get_basename()}"
            )
            # Delay restart slightly to handle multiple rapid changes
            GLib.timeout_add(_RESTART_DELAY_MS, self._restart_tsumiki)

    def _restart_tsumiki(self) -> bool:
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
_watcher: ConfigWatcher | None = None


def start_config_watching():
    """Start watching config files for changes."""
    global _watcher
    if _watcher is None:
        _watcher = ConfigWatcher()


def stop_config_watching():
    """Stop watching config files."""
    global _watcher
    if _watcher is not None:
        _watcher.stop()
        _watcher = None
