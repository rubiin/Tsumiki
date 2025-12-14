import json
import subprocess
import threading

from fabric.core.service import Property, Signal
from gi.repository import GLib
from fabric.utils import logger

from .base import SingletonService


class LockStateService(SingletonService):
    """Service to monitor CapsLock and NumLock states."""

    @Signal
    def caps_changed(self, is_on: bool) -> None:
        """Signal emitted when CapsLock state changes."""

    @Signal
    def num_changed(self, is_on: bool) -> None:
        """Signal emitted when NumLock state changes."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._caps = None
        self._num = None
        self._stop_monitoring = threading.Event()
        self._thread = None

    def start_monitoring(self):
        """Start monitoring lock states."""
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop_monitoring(self):
        """Stop monitoring lock states."""
        self._stop_monitoring.set()
        if self._thread:
            self._thread.join()

    def _monitor_loop(self):
        """Monitor loop that checks lock states periodically."""
        while not self._stop_monitoring.is_set():
            self._check_lock_states()
            self._stop_monitoring.wait(0.1)  # Wait 100ms or until stopped

    def _check_lock_states(self):
        """Check current lock states using hyprctl."""
        try:
            result = subprocess.run(
                ["hyprctl", "devices", "-j"], capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                devices = json.loads(result.stdout)
                # Find main keyboard
                for keyboard in devices.get("keyboards", []):
                    if keyboard.get("main", False):
                        caps = keyboard.get("capsLock", False)
                        num = keyboard.get("numLock", False)
                        self._update_caps(caps)
                        self._update_num(num)
                        break
        except Exception as e:
            logger.error(f"CapsLock polling error: {e}")

    def _update_caps(self, state: bool):
        """Update caps lock state and emit signal if changed."""
        if self._caps != state:
            self._caps = state
            GLib.idle_add(lambda: self.emit("caps_changed", state))

    def _update_num(self, state: bool):
        """Update num lock state and emit signal if changed."""
        print("Num lock state checked:", state)
        if self._num != state:
            self._num = state
            GLib.idle_add(lambda: self.emit("num_changed", state))

    @Property(bool, "read-write", default_value=False)
    def caps_on(self) -> bool:
        return self._caps if self._caps is not None else False

    @Property(bool, "read-write", default_value=False)
    def num_on(self) -> bool:
        return self._num if self._num is not None else False
