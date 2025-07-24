from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.battery import BatteryService
from shared.widget_container import ButtonWidget
from utils.functions import format_seconds_to_hours_minutes
from utils.icons import symbolic_icons


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

        self.full_battery_level = self.config.get("full_battery_level", 100)

        self.battery_icon = Image(
            icon_name=symbolic_icons["battery"]["full"],
            icon_size=self.config.get("icon_size", 14),
        )

        self.box.add(self.battery_icon)

        if self.config.get("label", True):
            self.battery_label = Label(label="100%", style_classes="panel-text")
            self.box.add(self.battery_label)

        self.client = BatteryService()

        self.notification_time = 0

        self.client.connect("changed", self.update_ui)

        self.update_ui()

    def update_ui(self, *_):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        is_present = self.client.get_property("IsPresent") == 1

        if not is_present:
            if self.config.get("hide_when_missing", True):
                self.set_visible(False)
            self.set_tooltip_text("󰂎 No battery present")
            if self.config.get("label", True):
                self.battery_label.set_text("N/A")
            return True

        battery_percent = (
            round(self.client.get_property("Percentage")) if is_present else 0
        )

        battery_state = self.client.get_property("State")

        is_charging = battery_state == 1 if is_present else False

        temperature = self.client.get_property("Temperature") or 0
        energy = self.client.get_property("Energy") or 0

        time_remaining = (
            self.client.get_property("TimeToFull")
            if is_charging
            else self.client.get_property("TimeToEmpty")
        ) or 0

        self.battery_icon.set_from_icon_name(
            self.client.get_property("IconName"), self.config["icon_size"]
        )

        # Update the label with the battery percentage if enabled
        if self.config.get("label", True):
            self.battery_label.set_text(f"{battery_percent}%")
            self.battery_label.show()

            ## Hide the label when the battery is full
            if (
                self.config["hide_label_when_full"]
                and battery_percent == self.full_battery_level
            ):
                self.battery_label.hide()

        # Update the tooltip with the battery status details if enabled
        if self.config.get("tooltip", False):
            status_text = (
                "󱠴 Status: Charging" if is_charging else "󱠴 Status: Discharging"
            )
            tool_tip_text = (
                f"󱐋 Energy : {round(energy, 2)} Wh\n Temperature: {temperature}°C"
            )
            formatted_time = format_seconds_to_hours_minutes(time_remaining)
            if battery_percent == self.full_battery_level:
                self.set_tooltip_text(f"󱠴 Status: Fully Charged\n{tool_tip_text}")

            elif is_charging and battery_percent < self.full_battery_level:
                self.set_tooltip_text(
                    f"{status_text}\n󰄉 Full in : {formatted_time}\n{tool_tip_text}"
                )
            else:
                self.set_tooltip_text(
                    f"{status_text}\n󰄉 Empty in : {formatted_time}\n{tool_tip_text}"
                )

        return True
