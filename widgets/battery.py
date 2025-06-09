from datetime import datetime

from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services import BatteryService
from shared.widget_container import ButtonWidget
from utils.functions import format_time
from utils.icons import symbolic_icons

NOTIFICATION_TIMEOUT = 60 * 5  # 5 minutes


class BatteryWidget(ButtonWidget):
    """A widget to display the current battery status."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="battery",
            **kwargs,
        )

        self.full_battery_level = self.config["full_battery_level"]

        self.battery_icon = Image(
            icon_name=symbolic_icons["battery"]["full"],
            icon_size=self.config["icon_size"],
        )

        self.box.add(self.battery_icon)

        if self.config["label"]:
            self.battery_label = Label(label="100%", style_classes="panel-text")
            self.box.add(self.battery_label)

        self.client = BatteryService()

        self.notification_time = 0

        self.client.connect("changed", self.update_ui)
        self.time_since_last_notification = datetime.now()

        self.update_ui()

    def update_ui(self, *_):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        is_present = self.client.get_property("IsPresent") == 1

        battery_percent = (
            round(self.client.get_property("Percentage")) if is_present else 0
        )

        battery_state = self.client.get_property("State")

        is_charging = battery_state == 1 if is_present else False

        temperature = self.client.get_property("Temperature")
        energy = self.client.get_property("Energy")

        time_remaining = (
            self.client.get_property("TimeToFull")
            if is_charging
            else self.client.get_property("TimeToEmpty")
        )

        self.battery_icon.set_from_icon_name(
            self.client.get_property("IconName"), self.config["icon_size"]
        )

        # Update the label with the battery percentage if enabled
        if self.config["label"]:
            self.battery_label.set_text(f"{battery_percent}%")

            ## Hide the label when the battery is full
            if (
                self.config["hide_label_when_full"]
                and battery_percent == self.full_battery_level
            ):
                self.battery_label.hide()

        # Update the tooltip with the battery status details if enabled
        if self.config["tooltip"]:
            status_text = (
                "󱠴 Status: Charging" if is_charging else "󱠴 Status: Discharging"
            )
            tool_tip_text = (
                f"󱐋 Energy : {round(energy, 2)} Wh\n Temperature: {temperature}°C"
            )
            formatted_time = format_time(time_remaining)
            if battery_percent == self.full_battery_level:
                self.set_tooltip_text(
                    f"{status_text}\n󰄉 Time to full: 0\n{tool_tip_text}"
                )
            elif is_charging and battery_percent < self.full_battery_level:
                self.set_tooltip_text(
                    f"{status_text}\n󰄉 Time to full: {formatted_time}\n{tool_tip_text}"
                )
            else:
                self.set_tooltip_text(
                    f"{status_text}\n󰄉 Time to empty: {formatted_time}\n{tool_tip_text}"
                )

        return True
