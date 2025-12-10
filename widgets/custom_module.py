import json
import os
import signal
import subprocess

from fabric.utils import bulk_connect, exec_shell_command_async, invoke_repeater, logger
from fabric.widgets.label import Label
from gi.repository import Gdk, GLib

from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.widget_utils import nerd_font_icon

# Module-level constants - evaluated once at import
_BUTTON_HANDLERS = {
    1: "on_click",
    2: "on_click_middle",
    3: "on_click_right",
}

_SCROLL_HANDLERS = {
    Gdk.ScrollDirection.UP: "on_scroll_up",
    Gdk.ScrollDirection.DOWN: "on_scroll_down",
}


class CustomModuleWidget(ButtonWidget):
    """A Waybar-compatible custom module widget."""

    __slots__ = (
        "_exec_cmd",
        "_exec_on_event",
        "_format_str",
        "_interval",
        "_last_class",
        "_max_len",
        "_process",
        "_signal_handler_id",
        "icon",
        "module_config",
        "text_label",
    )

    def __init__(
        self,
        widget_name: str = "custom_module",
        config: dict | None = None,
        **kwargs,
    ):
        super().__init__(name=widget_name, **kwargs)

        # Use passed config or get from widget_config
        self.module_config = config or self.config
        self._process: subprocess.Popen | None = None
        self._last_class: str | None = None
        self._signal_handler_id: int | None = None

        # Cache frequently accessed config values
        self._exec_cmd = self.module_config.get("exec")
        self._interval = self.module_config.get("interval", 0)
        self._format_str = self.module_config.get("format", "{}")
        self._max_len = self.module_config.get("max_length", 0)
        self._exec_on_event = self.module_config.get("exec_on_event", False)

        icon = self.module_config.get("format_icons", {}).get("default")
        if icon:
            self.icon = nerd_font_icon(
                icon=icon,
                props={"style_classes": ["panel-font-icon"]},
            )
            self.container_box.add(self.icon)
        else:
            self.icon = None

        self.text_label = Label(label="", style_classes=["panel-text"])
        self.container_box.add(self.text_label)

        rotation = self.module_config.get("rotate", 0)
        if rotation:
            self.text_label.set_angle(rotation)

        self.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.SMOOTH_SCROLL_MASK)

        bulk_connect(
            self,
            {
                "button-press-event": self._on_button_press,
                "scroll-event": self._on_scroll,
            },
        )

        # Register signal handler for external updates (like waybar's signal feature)
        sig = self.module_config.get("signal")
        if sig and isinstance(sig, int):
            try:
                self._register_signal(sig)
            except Exception as e:
                logger.exception(
                    f"{Colors.WARNING}[CustomModule] Failed to register signal: {e}"
                )

        self._start_execution()

    def _register_signal(self, sig_num: int):
        """Register a Unix signal handler to trigger updates."""
        # SIGRTMIN is typically 34, we add the user-specified offset
        actual_signal = signal.SIGRTMIN + sig_num
        signal.signal(actual_signal, lambda *_: self._execute_command())
        self._signal_handler_id = sig_num

    def _start_execution(self):
        """Start the command execution based on configuration."""
        if not self._exec_cmd:
            logger.warning(
                f"{Colors.WARNING}[CustomModule] No 'exec' command specified"
            )
            return

        if self._interval > 0:
            self._execute_command()
            invoke_repeater(self._interval * 1000, self._periodic_execute)
            return

        # One-shot or continuous execution
        restart_interval = self.module_config.get("restart_interval", 0)
        if restart_interval > 0:
            self._start_continuous()
        else:
            self._execute_command()

    def _periodic_execute(self, *_) -> bool:
        """Called periodically by invoke_repeater."""
        self._execute_command()
        return True

    def _execute_command(self):
        """Execute the configured command asynchronously."""
        if not self._exec_cmd:
            return

        exec_shell_command_async(
            os.path.expanduser(self._exec_cmd),
            self._handle_output,
        )

    def _start_continuous(self):
        """Start a continuous/streaming command."""
        if not self._exec_cmd:
            return

        exec_cmd = os.path.expanduser(self._exec_cmd)

        try:
            self._process = subprocess.Popen(
                exec_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            def read_output():
                if self._process and self._process.stdout:
                    line = self._process.stdout.readline()
                    if line:
                        GLib.idle_add(self._handle_output, line.strip())
                        return True
                    else:
                        # Process ended, restart if configured
                        restart = self.module_config.get("restart_interval", 0)
                        if restart > 0:
                            GLib.timeout_add(restart * 1000, self._start_continuous)
                return False

            invoke_repeater(100, read_output)

        except Exception as e:
            logger.exception(
                f"{Colors.ERROR}[CustomModule] Failed to start continuous command: {e}"
            )

    def _handle_output(self, output: str):
        """Handle command output (plain text or JSON)."""
        if not output:
            return

        output = output.strip()
        return_type = self.module_config.get("return_type", "plain")

        if return_type == "json" or output.startswith("{"):
            self._handle_json_output(output)
        else:
            self._handle_text_output(output)

    def _format_text(self, text: str) -> str:
        """Apply format string and max_length to text."""
        display_text = (
            self._format_str.replace("{}", str(text))
            if "{}" in self._format_str
            else text
        )
        if self._max_len > 0 and len(display_text) > self._max_len:
            display_text = display_text[: self._max_len] + "…"
        return display_text

    def _update_icon(self, alt: str | None, percentage: int | None):
        """Update icon based on alt or percentage."""
        if not self.icon:
            return

        format_icons = self.module_config.get("format_icons", {})
        if not format_icons:
            return

        icon = None
        if alt and alt in format_icons:
            icon = format_icons[alt]
        elif percentage is not None:
            # Find icon for percentage ranges
            for key, val in format_icons.items():
                if isinstance(key, str) and key.isdigit() and percentage >= int(key):
                    icon = val

        if icon:
            self.icon.set_label(icon)

    def _handle_json_output(self, output: str):
        """Parse Waybar-compatible JSON output."""
        try:
            data = json.loads(output)

            text = data.get("text", "")
            alt = data.get("alt", "")
            percentage = data.get("percentage")

            self.text_label.set_label(self._format_text(text))

            # Tooltip
            if self.module_config.get("tooltip", True):
                tooltip = data.get("tooltip", "")
                self.set_tooltip_markup(tooltip) if tooltip else self.set_tooltip_text(
                    ""
                )

            # CSS class
            new_class = data.get("class")
            if new_class != self._last_class:
                if self._last_class:
                    self.remove_style_class(self._last_class)
                if new_class:
                    self.add_style_class(new_class)
                self._last_class = new_class

            # Update icon based on alt or percentage
            self._update_icon(alt, percentage)

        except json.JSONDecodeError as e:
            logger.warning(f"{Colors.WARNING}[CustomModule] Invalid JSON output: {e}")
            self._handle_text_output(output)

    def _handle_text_output(self, output: str):
        """Handle plain text output."""
        self.text_label.set_label(self._format_text(output))

    def _on_button_press(self, widget, event) -> bool:
        """Handle button press events."""
        handler_key = _BUTTON_HANDLERS.get(event.button)
        if not handler_key:
            return False

        cmd = self.module_config.get(handler_key)
        if not cmd:
            return False

        exec_shell_command_async(os.path.expanduser(cmd), lambda _: None)

        # Re-execute main command if exec_on_event is true
        if self._exec_on_event:
            self._execute_command()

        return True

    def _on_scroll(self, widget, event) -> bool:
        """Handle scroll events (both discrete and smooth scrolling)."""
        direction = event.direction

        # Handle smooth scrolling (touchpads and modern mice)
        if direction == Gdk.ScrollDirection.SMOOTH:
            _, _, delta_y = event.get_scroll_deltas()
            if delta_y > 0:
                handler_key = "on_scroll_down"
            elif delta_y < 0:
                handler_key = "on_scroll_up"
            else:
                return False
        else:
            # Handle discrete scrolling (traditional scroll wheels)
            handler_key = _SCROLL_HANDLERS.get(direction)
            if not handler_key:
                return False

        cmd = self.module_config.get(handler_key)
        if not cmd:
            return False

        exec_shell_command_async(os.path.expanduser(cmd), lambda _: None)

        if self._exec_on_event:
            self._execute_command()

        return True

    def destroy(self):
        """Clean up resources."""
        if self._process:
            self._process.terminate()
            self._process = None
        super().destroy()
