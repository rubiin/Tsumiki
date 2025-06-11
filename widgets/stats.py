from fabric.utils import exec_shell_command_async
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
        self.current_mode = self.config["mode"]

        exec_shell_command_async(
            "bash -c \"lscpu | grep 'Model name' | awk -F: '{print $2}'\"",
            self.set_cpu_name,
        )

        if self.current_mode == "graph":
            self.graph_values = []
            self.cpu_level_label = Label(
                label="0%",
                style_classes="panel-text",
            )
            self.box.children = self.cpu_level_label

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
                icon=self.config["icon"],
                props={
                    "style_classes": "panel-font-icon overlay-icon",
                },
            )

            # Create an event box to handle scroll events for volume control
            self.box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )

            self.cpu_level_label = Label(
                label="0%",
                style_classes="panel-text",
            )
            self.box.children = (self.icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self.update_ui)

    def set_cpu_name(self, cpu_name):
        self.cpu_name = cpu_name.strip()

    def update_ui(self, _, value):
        # Update the label with the current CPU usage if enabled
        frequency = value.get("cpu_freq")
        usage = value.get("cpu_usage")

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(usage))

            if len(self.graph_values) > self.config["graph_length"]:
                self.graph_values.pop(0)

            self.cpu_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(usage / 100.0)

        else:
            self.cpu_level_label.set_label(f"{usage}%")

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            temp = value.get("temperature")

            temp = temp.get(self.config["sensor"])

            if temp is None:
                return "N/A"

            # current temperature
            temp = temp.pop()[1]

            temp = round(temp) if self.config["round"] else temp

            is_celsius = self.config["temperature_unit"] == "celsius"

            temp = (
                f"{temp} °C"
                if is_celsius
                else f"{helpers.celsius_to_fahrenheit(temp)} °F"
            )

            tooltip_text = (
                f"{self.cpu_name}\n"
                f" Temperature: {temp}\n"
                f"󰾆 Utilization: {usage}\n"
                f" Clock Speed: {round(frequency[0], 2)} MHz"
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
        self.current_mode = self.config["mode"]

        if self.current_mode == "graph":
            self.graph_values = []
            self.memory_level_label = Label(
                label="0%", style_classes="panel-text", visible=False
            )

            self.box.children = self.memory_level_label

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
                icon=self.config["icon"],
                props={
                    "style_classes": "panel-font-icon overlay-icon",
                },
            )

            # Create an event box to handle scroll events for volume control
            self.box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )

            self.memory_level_label = Label(
                label="0%",
                style_classes="panel-text",
            )
            self.box.children = (self.icon, self.memory_level_label)

        # Set up a fabricator to call the update_label method  at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
        # Get the current memory usage
        memory = value.get("memory")
        self.used_memory = memory.used
        self.total_memory = memory.total
        self.percent_used = memory.percent

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(self.percent_used))

            if len(self.graph_values) > self.config["graph_length"]:
                self.graph_values.pop(0)

            self.memory_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(self.percent_used / 100.0)

        else:
            self.memory_level_label.set_label(f"{self.get_used()}")

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.percent_used}%\n{text_icons['memory']} {self.ratio()}",
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.used_memory, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.total_memory, "gb")

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
        self.current_mode = self.config["mode"]

        if self.current_mode == "graph":
            self.graph_values = []

            self.storage_level_label = Label(
                label="0",
                style_classes="panel-text",
            )

            self.box.children = self.storage_level_label

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
                icon=self.config["icon"],
                props={
                    "style_classes": "panel-font-icon overlay-icon",
                },
            )

            # Create an event box to handle scroll events for volume control
            self.box.children = (
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
            )

        else:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )

            self.storage_level_label = Label(
                label="0",
                style_classes="panel-text",
            )

            self.box.children = (self.icon, self.storage_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
        # Get the current disk usage
        self.disk = value.get("disk")
        percent = self.disk.percent

        if self.current_mode == "graph":
            self.graph_values.append(get_bar_graph(percent))

            if len(self.graph_values) > self.config["graph_length"]:
                self.graph_values.pop(0)

            self.storage_level_label.set_label("".join(self.graph_values))

        elif self.current_mode == "progress":
            self.progress_bar.set_value(percent / 100.0)

        else:
            self.storage_level_label.set_label(f"{self.get_used()}")

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {percent}%\n{text_icons['storage']} {self.ratio()}"
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.disk.used, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.disk.total, "gb")

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

        show_download = self.config["download"]
        show_upload = self.config["upload"]

        # Create a TextIcon with the specified icon and size
        self.upload_icon = nerd_font_icon(
            icon=self.config["upload_icon"],
            props={"style_classes": "panel-font-icon", "visible": show_upload},
        )

        self.upload_label = Label(
            name="upload_label",
            label="0 MB",
            style_classes="panel-text",
            visible=show_upload,
            style="margin-right: 10px;",
        )

        self.download_icon = nerd_font_icon(
            icon=self.config["download_icon"],
            props={"style_classes": "panel-font-icon", "visible": show_download},
        )

        self.download_label = Label(
            name="download_label",
            label="0 MB",
            style_classes="panel-text",
            visible=show_download,
        )

        self.box.children = (
            self.upload_icon,
            self.upload_label,
            self.download_icon,
            self.download_label,
        )

        self.client = NetworkSpeed()

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
        """Update the network usage label with the current network usage."""

        # Get the current network usage
        network_speed = self.client.get_network_speed()

        if self.config["tooltip"]:
            tooltip_text = (
                f"Download: {round(network_speed.get('download', 0), 2)} MB/s\n"
            )
            tooltip_text += f"Upload: {round(network_speed.get('upload', 0), 2)} MB/s"
            self.set_tooltip_text(tooltip_text)

        download_speed = network_speed.get("download", "0")
        upload_speed = network_speed.get("upload", "0")

        self.upload_label.set_label(f"{round(upload_speed, 2)} MB/s")

        self.download_label.set_label(f"{round(download_speed, 2)} MB/s")

        return True
