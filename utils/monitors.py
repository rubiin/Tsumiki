import json
import warnings

from fabric.hyprland import Hyprland
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import bulk_connect
from gi.repository import Gdk, GLib
from loguru import logger

from .constants import MONITOR_HOTPLUG_DELAY_MS
from .functions import ttl_lru_cache

warnings.filterwarnings("ignore", category=DeprecationWarning)


class HyprlandWithMonitors(Hyprland):
    """A Hyprland class with additional monitor common."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, commands_only: bool = False, **kwargs):
        super().__init__(commands_only, **kwargs)
        self.display: Gdk.Display = Gdk.Display.get_default()

    @ttl_lru_cache(100, 5)
    def get_all_monitors(self) -> dict | None:
        try:
            monitors = self.send_command("j/monitors").reply.decode().strip("\n")
            return {monitor["id"]: monitor["name"] for monitor in monitors}
        except Exception as e:
            logger.exception(f"[Monitors] Error getting all monitors: {e}")
            return None

    def get_gdk_monitor_id_from_name(self, plug_name: str) -> int | None:
        for i in range(self.display.get_n_monitors()):
            if self.display.get_default_screen().get_monitor_plug_name(i) == plug_name:
                return i
        return None

    def get_gdk_monitor_id(self, hyprland_id: int) -> int | None:
        monitors = self.get_all_monitors()
        if not monitors:
            return None
        if hyprland_id in monitors:
            return self.get_gdk_monitor_id_from_name(monitors[hyprland_id])
        return None

    def get_current_gdk_monitor_id(self) -> int | None:
        try:
            active_workspace = (
                self.send_command("j/activeworkspace").reply.decode().strip("\n")
            )
            return self.get_gdk_monitor_id_from_name(active_workspace["monitor"])
        except Exception as e:
            logger.exception(f"[Monitors] Error getting current GDK monitor ID: {e}")
            return None

    def get_monitor_names(self) -> list[str]:
        """Get list of all connected monitor names."""
        try:
            monitors = self.send_command("j/monitors").reply.decode().strip("\n")
            return [monitor["name"] for monitor in monitors]
        except json.JSONDecodeError as e:
            logger.exception(f"[Monitors] Error parsing monitor data: {e}")
            return []
        except Exception as e:
            logger.exception(f"[Monitors] Error getting monitor names: {e}")
            return []


class MonitorWatcher:
    """Watches for monitor add/remove events and notifies registered callbacks."""

    def __init__(self):
        self.callbacks = []
        self._hyprland_connection = None

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def start_watching(self):
        if self._hyprland_connection:
            return

        self._hyprland_connection = get_hyprland_connection()

        bulk_connect(
            self._hyprland_connection,
            {
                "event::monitoradded": self.on_monitor_changed,
                "event::monitorremoved": self.on_monitor_changed,
            },
        )

    def on_monitor_changed(self, *_):
        GLib.timeout_add(MONITOR_HOTPLUG_DELAY_MS, self._notify_callbacks)

    def _notify_callbacks(self):
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                logger.exception(f"Monitor callback error: {e}")
        return False
