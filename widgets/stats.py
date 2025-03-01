import json

from fabric import Fabricator
from fabric.utils import exec_shell_command
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from loguru import logger

import utils.functions as helpers
from shared.widget_container import ButtonWidget
from utils.icons import common_text_icons
from utils.widget_settings import BarConfig
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

        self.box.children = (self.text_icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Update the label with the current CPU usage if enabled
        avg_usage = value.get("cpu_freq")
        if self.config["label"]:
            self.cpu_level_label.show()
            self.cpu_level_label.set_label(value.get("cpu_usage"))

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            tooltip_text = ""

            for key, value in enumerate(avg_usage):
                tooltip_text += f"core{key}: {round(value.current)} Mhz\n"

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


class CPUTemperatureWidget(ButtonWidget):
    """A widget to display the current cpu temperature."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="cpu_temperature",
            **kwargs,
        )
        self.config = widget_config["cpu_temp"]

        self.box = Box()
        self.children = (self.box,)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.temp_level_label = Label(
            label="0", style_classes="panel-text", visible=False
        )

        self.box.children = (self.icon, self.temp_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Get the current disk usage
        value = value.get("temperature")

        temp = value.get(self.config["sensor"])

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

        label_text = f"{temp}°C" if self.config["unit"] == "celsius" else f"{temp}°F"
        if self.config["label"]:
            self.temp_level_label.set_label(label_text)
            self.temp_level_label.show()

        if self.config["tooltip"]:
            self.set_tooltip_text(f"󰾆 {label_text}")

        return True


class NetworkUsageWidget(ButtonWidget):
    """A widget to display the current network usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        super().__init__(
            name="network_usage",
            **kwargs,
        )
        self.nmcli_command = "nmcli -c no -t"

        self.config = widget_config["network_usage"]

        self.nmcli_wifi_adapter_name = self.config["adapter_name"]
        self.network_usage_upload_icon = self.config["upload_icon"]
        self.network_usage_download_icon = self.config["download_icon"]
        self.network_disconnected_icon = self.config["disconnected_icon"]

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["upload_icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.network_level_label = Label(
            name="network_usage", label="0 KB", style_classes="panel-text"
        ).build(
            lambda label, _: Fabricator(
                poll_from=f"vnstat -i {self.nmcli_wifi_adapter_name} -l --json",
                stream=True,
                on_changed=lambda _, value: self.update_usage(value),
            )
        )

        self.box = Box()

        self.children = (self.box,)

        self.box.children = (self.icon, self.network_level_label)

    def update_usage(self, value):
        try:
            data = json.loads(value)
        except Exception as e:
            logger.error(f"Error while deserializing network usage json: {e}")
            return

        if "jsonversion" in data or "index" not in data:
            return

        device_stats = exec_shell_command(
            f"{self.nmcli_command} d show {self.nmcli_wifi_adapter_name}"
        )

        connection_state = None
        connection_strength = None
        connection_name = "unknown"

        ip_address = None
        for line in device_stats.splitlines():
            if "STATE" in line:
                state = line.split(":")[1]
                connection_state = state.split(" ")[1][1:-1]
                connection_strength = int(state.split(" ")[0])
            elif "CONNECTION" in line:
                connection_name = line.split(":")[1]
            elif "IP4.ADDRESS" in line:
                ip_address = line.split(":")[1].split("/")[0]

        if not connection_state:
            return

        if connection_state != "connected":
            self.icon.set_markup(self.network_disconnected_icon)
            self.network_level_label.set_label("Disconnected")

            self.set_tooltip_markup("Disconnected")
            return

        tx_rate = int(data["tx"]["bytespersecond"])
        rx_rate = int(data["rx"]["bytespersecond"])

        def get_size(bytes):
            factor = 1024
            bytes /= factor
            for unit in ["KB", "MB"]:
                if bytes < factor:
                    return f"{
                        int(bytes)
                        if bytes < 1
                        else (float(int(bytes * 10)) / 10)
                        if bytes < 100
                        else int(bytes)
                    } {unit}"
                bytes /= factor

        if tx_rate >= rx_rate:
            self.icon.set_markup(self.network_usage_upload_icon)
            self.network_level_label.set_label(get_size(tx_rate))
        else:
            self.icon.set_markup(self.network_usage_download_icon)
            self.network_level_label.set_label(get_size(rx_rate))

        if self.config["tooltip"]:
            self.set_tooltip_markup(
                (
                    f"Connected to {connection_name}\n"
                    f"Connection strength: {connection_strength}\n"
                    if connection_state
                    else ""
                )
                + (f"IP Address: {ip_address}" if ip_address else "")
            )
