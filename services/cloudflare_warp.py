import subprocess

from fabric.core.service import Signal
from fabric.utils import GLib, exec_shell_command_async, logger

from .base import SingletonService


class CloudflareWarpService(SingletonService):
    """Service to manage Cloudflare WARP connection status.

    Polls ``warp-cli status`` at a configurable interval and emits
    ``changed`` when state changes.
    """

    @Signal
    def changed(self) -> None:
        """Emitted when connection state changes."""

    def __init__(self, poll_interval_ms: int = 5000, **kwargs):
        super().__init__(**kwargs)

        self._poll_interval = poll_interval_ms
        self._connected = False

        self._poll_timer_id: int | None = None
        self._poller_running = False

        self._start_polling()

    # ── Properties ──────────────────────────────────────────────

    @property
    def connected(self) -> bool:
        return self._connected

    # ── Polling ─────────────────────────────────────────────────

    def _start_polling(self):
        if self._poller_running:
            return
        self._poller_running = True
        self._poll()

    def _stop_polling(self):
        self._poller_running = False
        if self._poll_timer_id is not None:
            GLib.source_remove(self._poll_timer_id)
            self._poll_timer_id = None

    def _poll(self):
        if not self._poller_running:
            return False

        exec_shell_command_async(
            "warp-cli status",
            self._on_status_line,
        )

        self._poll_timer_id = GLib.timeout_add(self._poll_interval, self._poll)
        return False

    def _on_status_line(self, line: str):
        raw = line.strip()
        if not raw:
            return

        was = self._connected

        if "Connected" in raw:
            self._connected = True
        elif "Disconnected" in raw:
            self._connected = False
        else:
            return  # Unknown line, keep current state

        if was != self._connected:
            logger.info(
                f"[CloudflareWARP] {'Connected' if self._connected else 'Disconnected'}"
            )
            self.emit("changed")

    # ── Actions (synchronous for user-initiated ops) ────────────

    def _run_warp_cli(self, action: str) -> bool:
        """Run a warp-cli command synchronously. Returns success."""
        try:
            result = subprocess.run(
                ["warp-cli", action],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.error(
                    f"[CloudflareWARP] 'warp-cli {action}' failed: "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )
                return False
            return True

        except FileNotFoundError:
            logger.error("[CloudflareWARP] warp-cli not found in PATH")
            return False
        except subprocess.TimeoutExpired:
            logger.error(f"[CloudflareWARP] 'warp-cli {action}' timed out")
            return False
        except Exception as e:
            logger.error(f"[CloudflareWARP] 'warp-cli {action}' error: {e}")
            return False

    def connect_warp(self) -> bool:
        ok = self._run_warp_cli("connect")
        if ok:
            self._connected = True
            self.emit("changed")
            # Confirm via immediate poll
            exec_shell_command_async("warp-cli status", self._on_status_line)
        return ok

    def disconnect_warp(self) -> bool:
        ok = self._run_warp_cli("disconnect")
        if ok:
            self._connected = False
            self.emit("changed")
            exec_shell_command_async("warp-cli status", self._on_status_line)
        return ok

    def toggle_warp(self) -> bool:
        return self.disconnect_warp() if self._connected else self.connect_warp()

    # ── Teardown ────────────────────────────────────────────────

    def destroy(self):
        self._stop_polling()
        return super().destroy()


# Singleton instance
cloudflare_warp_service = CloudflareWarpService()
