import json

from fabric.utils import exec_shell_command, exec_shell_command_async
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

import utils.functions as helpers
from services.networkspeed import NetworkSpeed
from shared.widget_container import ButtonWidget
from utils.icons import text_icons
from utils.widget_utils import (
    get_bar_graph,
    nerd_font_icon,
    util_fabricator,
)


class CpuWidget(ButtonWidget):
    """A widget to display the current CPU usage."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="cpu",
            **kwargs,
        )

        # Set the CPU name and mode
        self.current_mode = self.config.get("mode", "label")

        exec_shell_command_async(
            "bash -c \"lscpu | grep 'Model name' | awk -F: '{print $2}'\"",
            self.set_cpu_name,
        )

        if self.current_mode == "graph":
            self.graph_values = []
            self.cpu_level_label = Label(
                label="0%",
                style_classes=["panel-text"],
            )
            self.container_box.children = self.cpu_level_label

        elif self.current_mode == "progress":
            # Create a circular progress bar to display the volume level
            self.progress_bar = CircularProgressBar(
                name="stat-circle",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )

            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": ["panel-font-icon", "overlay-icon"],
                },
            )

            # Create an event box to handle scroll events for volume control
            self.container_box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": ["panel-font-icon"]},
            )

            self.cpu_level_label = Label(
                label="0%",
                style_classes=["panel-text"],
            )
            self.container_box.children = (self.icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self._update_ui)

    def set_cpu_name(self, cpu_name: str):
        self.cpu_name = cpu_name.strip()

    def _update_ui(self, _, value: dict):
        # Update the label with the current CPU usage if enabled
        frequency = value.get("cpu_freq")
        usage = value.get("cpu_usage")

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(usage))

            if len(self.graph_values) > self.config.get("graph_length", 4):
                self.graph_values.pop(0)

            self.cpu_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(usage / 100.0)

        else:
            self.cpu_level_label.set_label(f"{usage}%")

        # Update the tooltip with the memory usage details if enabled
        if self.config.get("tooltip", False):
            temp = value.get("temperature")

            temp = temp.get(self.config.get("sensor", ""))

            if temp is None:
                return "N/A"

            # current temperature
            temp = temp[-1][1] if temp else 0

            temp = round(temp) if self.config.get("round", True) else temp

            is_celsius = self.config.get("temperature_unit", "celsius") == "celsius"

            temp = (
                f"{temp} °C"
                if is_celsius
                else f"{helpers.celsius_to_fahrenheit(temp)} °F"
            )

            if isinstance(frequency, (list, tuple)) and frequency:
                freq_text = f"{round(frequency[0], 2)} MHz"
            else:
                freq_text = "Unknown"

            tooltip_text = (
                f"{self.cpu_name}\n"
                f" Temperature: {temp}\n"
                f"󰾆 Utilization: {usage}\n"
                f" Clock Speed: {freq_text}"
            )

            self.set_tooltip_text(tooltip_text)

        return True


class GpuWidget(ButtonWidget):
    """A widget to display the current GPU usage."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="gpu",
            **kwargs,
        )

        # Set the GPU name and mode
        self.current_mode = self.config.get("mode", "label")

        if self.current_mode == "graph":
            self.graph_values = []
            self.gpu_level_label = Label(
                label="0%",
                style_classes=["panel-text"],
            )
            self.container_box.children = self.gpu_level_label

        elif self.current_mode == "progress":
            # Create a circular progress bar to display the volume level
            self.progress_bar = CircularProgressBar(
                name="stat-circle",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )

            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": ["panel-font-icon", "overlay-icon"],
                },
            )

            # Create an event box to handle scroll events for volume control
            self.container_box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": ["panel-font-icon"]},
            )

            self.gpu_level_label = Label(
                label="0%",
                style_classes=["panel-text"],
            )
            self.container_box.children = (self.icon, self.gpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self._update_ui)

    def _update_ui(self, *_):
        # Update the label with the current GPU usage if enabled

        value = exec_shell_command("nvtop -s")

        stats = json.loads(value.strip("\n"))

        if type(stats) is list:
            stats = stats[0]

        frequency = stats.get("gpu_clock", "0 MHz")
        usage = stats.get("mem_util", "0").strip("%")
        gpu_name = stats.get("device_name", "N/A")

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(usage))

            if len(self.graph_values) > self.config.get("graph_length", 4):
                self.graph_values.pop(0)

            self.gpu_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(usage / 100.0)

        else:
            self.gpu_level_label.set_label(usage)

        # Update the tooltip with the memory usage details if enabled
        if self.config.get("tooltip", False):
            temp = stats.get("temp")

            if temp is None:
                return "N/A"

            tooltip_text = (
                f"{gpu_name}\n"
                f" Temperature: {temp}\n"
                f"󰾆 Utilization: {usage}\n"
                f" Clock Speed: {frequency}"
            )

            self.set_tooltip_text(tooltip_text)

        return True


class MemoryWidget(ButtonWidget):
    """A widget to display the current memory usage."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="memory",
            **kwargs,
        )

        # Set the memory name and mode
        self.current_mode = self.config.get("mode", "label")

        if self.current_mode == "graph":
            self.graph_values = []
            self.memory_level_label = Label(
                label="0%", style_classes=["panel-text"], visible=False
            )

            self.container_box.children = self.memory_level_label

        elif self.current_mode == "progress":
            # Create a circular progress bar to display the volume level
            self.progress_bar = CircularProgressBar(
                name="stat-circle",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )

            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": ["panel-font-icon", "overlay-icon"],
                },
            )

            # Create an event box to handle scroll events for volume control
            self.container_box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": ["panel-font-icon"]},
            )

            self.memory_level_label = Label(
                label="0%",
                style_classes=["panel-text"],
            )
            self.container_box.children = (self.icon, self.memory_level_label)

        # Set up a fabricator to call the update_label method  at specified intervals
        util_fabricator.connect("changed", self._update_ui)

    def _update_ui(self, _, value: dict):
        # Get the current memory usage
        memory = value.get("memory")
        self.used_memory = memory.used
        self.total_memory = memory.total
        self.percent_used = memory.percent

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(self.percent_used))

            if len(self.graph_values) > self.config.get("graph_length", 4):
                self.graph_values.pop(0)

            self.memory_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(self.percent_used / 100.0)

        else:
            self.memory_level_label.set_label(f"{self.get_used()}")

        # Update the tooltip with the memory usage details if enabled
        if self.config.get("tooltip", False):
            self.set_tooltip_text(
                f"󰾆 {self.percent_used}%\n{text_icons['memory']} {self.ratio()}",
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.used_memory, self.config.get("unit", "MB"))

    def get_total(self):
        return helpers.convert_bytes(self.total_memory, self.config.get("unit", "MB"))

    def ratio(self):
        return f"{self.get_used()}/{self.get_total()}"


class StorageWidget(ButtonWidget):
    """A widget to display the current storage usage."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="storage",
            **kwargs,
        )

        # Set the memory name and mode
        self.current_mode = self.config.get("mode", "label")

        if self.current_mode == "graph":
            self.graph_values = []

            self.storage_level_label = Label(
                label="0",
                style_classes=["panel-text"],
            )

            self.container_box.children = self.storage_level_label

        elif self.current_mode == "progress":
            # Create a circular progress bar to display the volume level
            self.progress_bar = CircularProgressBar(
                name="stat-circle",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )

            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={
                    "style_classes": ["panel-font-icon", "overlay-icon"],
                },
            )

            # Create an event box to handle scroll events for volume control
            self.container_box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰕸"),
                props={"style_classes": ["panel-font-icon"]},
            )

            self.storage_level_label = Label(
                label="0",
                style_classes=["panel-text"],
            )

            self.container_box.children = (self.icon, self.storage_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self._update_ui)

    def _update_ui(self, _, value: dict):
        # Get the current disk usage
        self.disk = value.get("disk")
        percent = self.disk.percent

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(percent))

            if len(self.graph_values) > self.config.get("graph_length", 4):
                self.graph_values.pop(0)

            self.storage_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(percent / 100.0)

        else:
            self.storage_level_label.set_label(f"{self.get_used()}")

        # Update the tooltip with the storage usage details if enabled
        if self.config.get("tooltip", False):
            self.set_tooltip_text(
                f"󰾆 {percent}%\n{text_icons['storage']} {self.ratio()}"
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.disk.used, self.config.get("unit", "MB"))

    def get_total(self):
        return helpers.convert_bytes(self.disk.total, self.config.get("unit", "MB"))

    def ratio(self):
        return f"{self.get_used()}/{self.get_total()}"


class NetworkUsageWidget(ButtonWidget):
    """A widget to display the current network usage."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            name="network_usage",
            **kwargs,
        )

        show_download = self.config.get("download", True)
        show_upload = self.config.get("upload", False)
        # Thresholds (in bytes/ms)
        self.download_threshold = self.config.get("download_threshold", 0)
        self.upload_threshold = self.config.get("upload_threshold", 0)

        # Number of digits for formatting
        self.kb_digits = self.config.get("kb_digits", 0)
        self.mb_digits = self.config.get("mb_digits", 2)

        self.upload_icon = nerd_font_icon(
            icon=self.config.get("upload_icon", "󰕸"),
            props={"style_classes": ["panel-font-icon"], "visible": show_upload},
        )

        self.upload_label = Label(
            name="upload_label",
            label="0 MB",
            style_classes=["panel-text"],
            visible=show_upload,
            style="margin-right: 10px;",
        )

        self.download_icon = nerd_font_icon(
            icon=self.config.get("download_icon", "󰕸"),
            props={"style_classes": ["panel-font-icon"], "visible": show_download},
        )

        self.download_label = Label(
            name="download_label",
            label="0 MB",
            style_classes=["panel-text"],
            visible=show_download,
        )

        self.container_box.children = (
            self.upload_icon,
            self.upload_label,
            self.download_icon,
            self.download_label,
        )

        self.client = NetworkSpeed()

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self._update_ui)

    def format_speed(self, speed: int):
        # speed is in bytes/ms, so *1000 = bytes/s
        speed_bps = speed * 1000
        if speed_bps < 1024:
            return f"{speed_bps:.0f} B/s"
        elif speed_bps < 1024 * 1024:
            return f"{speed_bps / 1024:.{self.kb_digits}f} KB/s"
        else:
            return f"{speed_bps / (1024 * 1024):.{self.mb_digits}f} MB/s"

    def _update_ui(self, *_):
        """Update the network usage label with the current network usage."""

        network_speed = self.client.get_network_speed()

        download_speed = network_speed.get("download", 0)
        upload_speed = network_speed.get("upload", 0)

        if upload_speed >= self.upload_threshold:
            self.upload_label.set_label(self.format_speed(upload_speed))
        else:
            self.upload_label.set_label("")

        if download_speed >= self.download_threshold:
            self.download_label.set_label(self.format_speed(download_speed))
        else:
            self.download_label.set_label("")

        if self.config.get("tooltip", False):
            tooltip_text = (
                f"Download: {self.format_speed(download_speed)}\n"
                f"Upload: {self.format_speed(upload_speed)}"
            )
            self.set_tooltip_text(tooltip_text)

        return True
