import contextlib
import json
from typing import ClassVar

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import GObject, logger

from utils.icons import symbolic_icons

from ..osd import GenericOSDContainer


class LockkeysOSDContainer(GenericOSDContainer):
    """OSD for capslock and numlock state.

    Driven by Hyprland ``event::activelayout`` — queries lock state
    asynchronously via ``j/devices`` when the event fires, instead of
    polling every 200ms.
    """

    __gsignals__: ClassVar = {
        "locks-changed": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config: dict, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.config = config
        self.previous_capslock = None
        self.previous_numlock = None

        # Create text display for locks
        from fabric.widgets.label import Label

        self.lock_label = Label(
            label="",
            style_classes=["osd-lock-label"],
            name="lock-label",
        )

        # Replace scale with lock display
        self.children = (self.icon, self.lock_label)

        # Subscribe to Hyprland event — fires on keyboard layout changes
        self._hyprland_connection = get_hyprland_connection()
        self._event_handler_id = self._hyprland_connection.connect(
            "event::activelayout", self._on_activelayout
        )

        # Initial query
        self._query_lock_state()

    def _on_activelayout(self, *_):
        """Hyprland layout-change event — query lock state."""
        self._query_lock_state()

    def _query_lock_state(self) -> bool:
        """Query current lock state via Hyprland socket (async)."""
        self._hyprland_connection.send_command_async(
            "j/devices",
            self._on_devices_reply,
        )
        return True

    def _on_devices_reply(self, reply, *_):
        """Parse j/devices reply for capslock/numlock."""
        try:
            data = json.loads(reply.reply.decode().strip("\n"))
            keyboards = data.get("keyboards", [])
            main_kb = next((kb for kb in keyboards if kb.get("main")), None)
            if main_kb is None:
                return

            caps = main_kb.get("capsLock", False)
            num = main_kb.get("numLock", False)

            if self.previous_capslock != caps or self.previous_numlock != num:
                self.previous_capslock = caps
                self.previous_numlock = num

                self._update_display(caps, num)
                self.emit("locks-changed")

        except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
            logger.warning(f"[LockkeysOSD] Parse error: {e}")

    def _update_display(self, caps: bool, num: bool):
        """Update icon and label based on lock state."""
        # Update icon
        if caps or num:
            icon_name = symbolic_icons.get("keyboard", {}).get(
                "locks", "input-keyboard-symbolic"
            )
        else:
            icon_name = "input-keyboard-symbolic"

        self.icon.set_from_icon_name(icon_name, self.icon_size)

        # Update label
        status_parts = []
        if caps:
            status_parts.append("⇪ CAPS")
        if num:
            status_parts.append("🔢 NUM")

        label_text = " | ".join(status_parts) if status_parts else "No locks"
        self.lock_label.set_label(label_text)

    def cleanup(self):
        """Clean up signal handlers on destroy."""
        if self._event_handler_id is not None:
            with contextlib.suppress(Exception):
                self._hyprland_connection.disconnect(self._event_handler_id)
            self._event_handler_id = None

    def do_destroy(self):
        """Called when widget destroyed."""
        self.cleanup()
        super().do_destroy()
