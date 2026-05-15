"""
Simple configuration file watcher for auto-reloading Tsumiki when config files change.
"""

import hashlib
import subprocess

from fabric.utils import GLib, get_relative_path, logger, os
from gi.repository import Gio

from utils.colors import Colors
from utils.config import widget_config
from utils.constants import APPLICATION_NAME

# Constants
# Debounce first, then enforce a minimum gap between restart attempts.
_DEFAULT_restart_delay = 1500
_RESTART_COOLDOWN_MS = 3000
_CONFIG_FILES = frozenset(("config.toml", "theme.toml"))


class ConfigWatcher:
    """Simple file watcher that monitors config files and restarts Tsumiki."""

    __slots__ = (
        "_file_hashes",
        "_initialized",
        "_last_restart_at_us",
        "_restart_delay",
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
        self._file_hashes: dict[str, str | None] = {}
        self._restart_pending = False
        self._last_restart_at_us = 0
        self._restart_delay = self._get_restart_delay()
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
            self._file_hashes[file_path] = self._read_file_hash(file_path)
            logger.info(
                f"{Colors.INFO}[ConfigWatcher] Monitoring {os.path.basename(file_path)}"
            )
        except Exception as e:
            logger.exception(
                f"{Colors.ERROR}[ConfigWatcher] Failed to monitor {file_path}: {e}"
            )

    def _get_restart_delay(self) -> int:
        """Read restart debounce delay from config with a safe fallback."""
        delay_ms = (
            widget_config.get("general", {}).get(
                "restart_delay", _DEFAULT_restart_delay
            )
            or _DEFAULT_restart_delay
        )

        try:
            return max(1, int(delay_ms))
        except (TypeError, ValueError):
            logger.warning(
                f"{Colors.WARNING}[ConfigWatcher] Invalid restart_delay "
                f"({delay_ms}), using {_DEFAULT_restart_delay}"
            )
            return _DEFAULT_restart_delay

    def _read_file_hash(self, file_path: str) -> str | None:
        """Return a stable hash for file content, or None when unreadable."""
        try:
            with open(file_path, "rb") as config_file:
                return hashlib.sha256(config_file.read()).hexdigest()
        except OSError:
            return None

    def _on_file_changed(self, monitor, file, other_file, event_type):
        """Handle file change events."""
        if event_type != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            return

        file_path = file.get_path()
        if not file_path:
            return

        current_hash = self._read_file_hash(file_path)
        previous_hash = self._file_hashes.get(file_path)
        if current_hash is None or current_hash == previous_hash:
            return

        self._file_hashes[file_path] = current_hash
        if self._restart_pending:
            return

        self._restart_pending = True
        logger.info(
            f"{Colors.INFO}[ConfigWatcher] Config changed: {file.get_basename()}"
        )
        # Delay restart slightly to batch rapid config writes.
        GLib.timeout_add(self._restart_delay, self._restart_if_allowed)

    def _restart_if_allowed(self) -> bool:
        """Restart after debounce while respecting cooldown between restarts."""

        now_us = GLib.get_monotonic_time()
        if self._last_restart_at_us:
            elapsed_ms = (now_us - self._last_restart_at_us) // 1000
            if elapsed_ms < _RESTART_COOLDOWN_MS:
                wait_ms = max(1, _RESTART_COOLDOWN_MS - elapsed_ms)
                GLib.timeout_add(wait_ms, self._restart_if_allowed)
                return False

        self._restart_pending = False
        self._last_restart_at_us = now_us

        logger.info(f"{Colors.INFO}[ConfigWatcher] Restarting after config changes")
        return self._restart_tsumiki()

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
        self._file_hashes.clear()


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
