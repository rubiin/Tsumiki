import json
from typing import ClassVar

from fabric.utils import GLib, GObject, exec_shell_command_async, logger

from utils.icons import symbolic_icons

from ..osd import GenericOSDContainer


class LockkeysOSDContainer(GenericOSDContainer):
    """OSD for capslock and numlock state."""

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
        self.poll_interval = config.get("poll_interval", 200)

        # Create text display for locks
        from fabric.widgets.label import Label

        self.lock_label = Label(
            label="",
            style_classes=["osd-lock-label"],
            name="lock-label",
        )

        # Replace scale with lock display
        self.children = (self.icon, self.lock_label)

        # Start polling
        self._poll_timer = None
        self._start_polling()

    def _start_polling(self):
        """Start polling hyprctl devices state."""

        def poll():
            exec_shell_command_async(
                "hyprctl devices -j",
                self._on_devices_output,
            )
            return True

        self._poll_timer = GLib.timeout_add(self.poll_interval, poll)
        # Initial poll
        poll()

    def _on_devices_output(self, output: str):
        """Parse hyprctl devices output."""
        try:
            data = json.loads(output)
            keyboards = data.get("keyboards", [])

            # Find main keyboard
            main_kb = None
            for kb in keyboards:
                if kb.get("main"):
                    main_kb = kb
                    break

            if not main_kb:
                return

            caps = main_kb.get("capsLock", False)
            num = main_kb.get("numLock", False)

            # Only emit if state changed
            if self.previous_capslock != caps or self.previous_numlock != num:
                self.previous_capslock = caps
                self.previous_numlock = num

                self._update_display(caps, num)
                self.emit("locks-changed")

        except (json.JSONDecodeError, KeyError, TypeError) as e:
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
        """Clean up timer on destroy."""
        if self._poll_timer:
            GLib.source_remove(self._poll_timer)
            self._poll_timer = None

    def do_destroy(self):
        """Called when widget destroyed."""
        self.cleanup()
        super().do_destroy()
