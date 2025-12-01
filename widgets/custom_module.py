"""
Waybar-compatible custom module widget.

Runs external commands/scripts and displays their output on the bar.
Supports both plain text and Waybar JSON protocol output.
"""

import json
import os
import signal
import subprocess

from fabric.utils import bulk_connect, exec_shell_command_async, invoke_repeater, logger
from fabric.widgets.label import Label
from gi.repository import GLib

from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.widget_utils import nerd_font_icon


class CustomModuleWidget(ButtonWidget):
    """A Waybar-compatible custom module widget."""

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

        # Create icon label (optional)
        icon = self.module_config.get("format_icons", {}).get("default")
        if icon:
            self.icon = nerd_font_icon(
                icon=icon,
                props={"style_classes": ["panel-font-icon"]},
            )
            self.container_box.add(self.icon)
        else:
            self.icon = None

        # Create text label
        self.text_label = Label(label="", style_classes=["panel-text"])
        self.container_box.add(self.text_label)

        # Apply rotation if specified
        rotation = self.module_config.get("rotate", 0)
        if rotation:
            self.text_label.set_angle(rotation)

        # Connect click and scroll events
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
                logger.warning(
                    f"{Colors.WARNING}[CustomModule] Failed to register signal: {e}"
                )

        # Start execution
        self._start_execution()

    def _register_signal(self, sig_num: int):
        """Register a Unix signal handler to trigger updates."""
        # SIGRTMIN is typically 34, we add the user-specified offset
        actual_signal = signal.SIGRTMIN + sig_num

        def handler(signum, frame):
            self._execute_command()

        signal.signal(actual_signal, handler)
        self._signal_handler_id = sig_num

    def _start_execution(self):
        """Start the command execution based on configuration."""
        exec_cmd = self.module_config.get("exec")
        if not exec_cmd:
            logger.warning(
                f"{Colors.WARNING}[CustomModule] No 'exec' command specified"
            )
            return

        interval = self.module_config.get("interval", 0)

        if interval and interval > 0:
            # Periodic execution
            self._execute_command()
            invoke_repeater(interval * 1000, self._periodic_execute)
        else:
            # One-shot or continuous execution
            restart_interval = self.module_config.get("restart_interval", 0)
            if restart_interval > 0:
                # Continuous with restart
                self._start_continuous()
            else:
                # Single execution
                self._execute_command()

    def _periodic_execute(self, *_) -> bool:
        """Called periodically by invoke_repeater."""
        self._execute_command()
        return True

    def _execute_command(self):
        """Execute the configured command asynchronously."""
        exec_cmd = self.module_config.get("exec")
        if not exec_cmd:
            return

        # Expand ~ to home directory
        exec_cmd = os.path.expanduser(exec_cmd)

        exec_shell_command_async(
            exec_cmd,
            self._handle_output,
        )

    def _start_continuous(self):
        """Start a continuous/streaming command."""
        exec_cmd = self.module_config.get("exec")
        if not exec_cmd:
            return

        exec_cmd = os.path.expanduser(exec_cmd)

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
            logger.error(
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

    def _handle_json_output(self, output: str):
        """Parse Waybar-compatible JSON output."""
        try:
            data = json.loads(output)

            # Get text
            text = data.get("text", "")
            alt = data.get("alt", "")
            percentage = data.get("percentage")

            # Apply format string
            format_str = self.module_config.get("format", "{}")
            if "{}" in format_str:
                display_text = format_str.replace("{}", str(text))
            else:
                display_text = text

            # Apply max_length
            max_len = self.module_config.get("max_length", 0)
            if max_len > 0 and len(display_text) > max_len:
                display_text = display_text[:max_len] + "…"

            self.text_label.set_label(display_text)

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
            format_icons = self.module_config.get("format_icons", {})
            if format_icons:
                icon = None
                if alt and alt in format_icons:
                    icon = format_icons[alt]
                elif percentage is not None:
                    # Find icon for percentage ranges
                    for key, val in format_icons.items():
                        if (
                            isinstance(key, str)
                            and key.isdigit()
                            and percentage >= int(key)
                        ):
                            icon = val
                if icon and self.icon:
                    self.icon.set_label(icon)

        except json.JSONDecodeError as e:
            logger.warning(f"{Colors.WARNING}[CustomModule] Invalid JSON output: {e}")
            self._handle_text_output(output)

    def _handle_text_output(self, output: str):
        """Handle plain text output."""
        format_str = self.module_config.get("format", "{}")
        if "{}" in format_str:
            display_text = format_str.replace("{}", output)
        else:
            display_text = output

        max_len = self.module_config.get("max_length", 0)
        if max_len > 0 and len(display_text) > max_len:
            display_text = display_text[:max_len] + "…"

        self.text_label.set_label(display_text)

    def _on_button_press(self, widget, event) -> bool:
        """Handle button press events."""
        handlers = {
            1: "on_click",
            2: "on_click_middle",
            3: "on_click_right",
        }

        handler_key = handlers.get(event.button)
        if handler_key:
            cmd = self.module_config.get(handler_key)
            if cmd:
                exec_shell_command_async(os.path.expanduser(cmd), lambda _: None)

                # Re-execute main command if exec_on_event is true
                if self.module_config.get("exec_on_event", False):
                    self._execute_command()

                return True

        return False

    def _on_scroll(self, widget, event) -> bool:
        """Handle scroll events."""
        from gi.repository import Gdk

        direction = event.direction

        if direction == Gdk.ScrollDirection.UP:
            cmd = self.module_config.get("on_scroll_up")
        elif direction == Gdk.ScrollDirection.DOWN:
            cmd = self.module_config.get("on_scroll_down")
        else:
            return False

        if cmd:
            exec_shell_command_async(os.path.expanduser(cmd), lambda _: None)

            if self.module_config.get("exec_on_event", False):
                self._execute_command()

            return True

        return False

    def destroy(self):
        """Clean up resources."""
        if self._process:
            self._process.terminate()
            self._process = None
        super().destroy()
