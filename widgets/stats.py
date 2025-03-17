from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.label import Label

import utils.functions as helpers
from services import network_speed
from shared import ButtonWidget
from utils import BarConfig
from utils.icons import common_text_icons
from utils.widget_utils import text_icon, util_fabricator


class CpuWidget(ButtonWidget):
    """A widget to display the current CPU usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config,
            name="cpu",
            **kwargs,
        )

        self.box = Box()
        self.children = (self.box,)

        self.config = widget_config["cpu"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.cpu_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.cpu_name = ""

        exec_shell_command_async(
            "bash -c \"lscpu | grep 'Model name' | awk -F: '{print $2}'\"",
            lambda value: setattr(self, "cpu_name", value.strip()),
        )

        self.box.children = (self.text_icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Update the label with the current CPU usage if enabled
        cpu_freq = value.get("cpu_freq")
        if self.config["label"]:
            self.cpu_level_label.show()
            self.cpu_level_label.set_label(value.get("cpu_usage"))

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            temp = value.get("temperature")

            temp = temp.get(self.config["sensor"])

            if temp is None:
                return "N/A"

            # current temperature
            temp = temp.pop()[1]

            temp = round(temp) if self.config["round"] else temp

            temp = (
                temp
                if self.config["unit"] == "celsius"
                else helpers.celsius_to_fahrenheit(temp)
            )

            tooltip_text = f"{self.cpu_name}\n"
            tooltip_text += (
                f" Temperature: {temp}°C"
                if self.config["unit"] == "celsius"
                else f"{temp}°F"
            )
            tooltip_text += f"\n󰾆 Utilization: {value.get('cpu_usage')}"
            tooltip_text += f"\n Clock Speed: {round(cpu_freq[0], 2)} MHz"

            self.set_tooltip_text(tooltip_text)

        return True


class MemoryWidget(ButtonWidget):
    """A widget to display the current memory usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config,
            name="memory",
            **kwargs,
        )

        self.config = widget_config["memory"]

        self.box = Box()
        self.children = (self.box,)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )
        self.memory_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.box.children = (self.icon, self.memory_level_label)

        # Set up a fabricator to call the update_label method  at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Get the current memory usage
        memory = value.get("memory")
        self.used_memory = memory.used
        self.total_memory = memory.total
        self.percent_used = memory.percent

        # Update the label with the used memory if enabled
        if self.config["label"]:
            self.memory_level_label.set_label(self.get_used())
            self.memory_level_label.show()

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.percent_used}%\n{common_text_icons['memory']} {self.ratio()}",
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
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config,
            name="storage",
            **kwargs,
        )
        self.config = widget_config["storage"]

        self.box = Box()
        self.children = (self.box,)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.storage_level_label = Label(
            label="0", style_classes="panel-text", visible=False
        )

        self.box.children = (self.icon, self.storage_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Get the current disk usage
        self.disk = value.get("disk")

        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.storage_level_label.set_label(f"{self.get_used()}")
            self.storage_level_label.show()

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n{common_text_icons['storage']} {self.ratio()}"
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
        widget_config: BarConfig,
        **kwargs,
    ):
        super().__init__(
            widget_config,
            name="network_usage",
            **kwargs,
        )

        self.config = widget_config["network_usage"]

        show_download = self.config["download"]
        show_upload = self.config["upload"]

        # Create a TextIcon with the specified icon and size
        self.upload_icon = text_icon(
            icon=self.config["upload_icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon", "visible": show_upload},
        )

        self.upload_label = Label(
            name="network_usage",
            label="0 MB",
            style_classes="panel-text",
            visible=show_upload,
            style="margin-right: 10px;",
        )

        self.download_icon = text_icon(
            icon=self.config["download_icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon", "visible": show_download},
        )

        self.download_label = Label(
            name="network_usage",
            label="0 MB",
            style_classes="panel-text",
            visible=show_download,
        )

        self.box = Box()

        self.children = (self.box,)

        self.box.children = (
            self.upload_icon,
            self.upload_label,
            self.download_icon,
            self.download_label,
        )

        self.client = network_speed

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
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
