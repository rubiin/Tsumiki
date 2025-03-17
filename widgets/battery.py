from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services import battery_service
from shared import ButtonWidget
from utils import BarConfig
from utils.functions import format_time


class BatteryWidget(ButtonWidget):
    """A widget to display the current battery status."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config,
            name="battery",
            **kwargs,
        )
        self.config = widget_config["battery"]
        self.full_battery_level = self.config["full_battery_level"]

        self.box = Box()

        self.children = (self.box,)

        self.client = battery_service

        self.client.connect("changed", lambda *_: self.update_ui())

        self.update_ui()

    def update_ui(self):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        is_present = self.client.get_property("IsPresent")

        battery_percent = (
            round(self.client.get_property("Percentage")) if is_present else 0
        )

        self.battery_label = Label(
            label=f"{battery_percent}%", style_classes="panel-text", visible=False
        )

        battery_state = self.client.get_property("State")

        is_charging = battery_state == 1 if is_present else False

        temperature = self.client.get_property("Temperature")
        capacity = self.client.get_property("Capacity")

        time_remaining = (
            self.client.get_property("TimeToFull")
            if is_charging
            else self.client.get_property("TimeToEmpty")
        )

        self.battery_icon = Image(
            icon_name=self.client.get_property("IconName"),
            icon_size=14,
        )

        self.box.children = (self.battery_icon, self.battery_label)

        # Update the label with the battery percentage if enabled
        if self.config["label"]:
            self.battery_label.show()

            ## Hide the label when the battery is full
            if (
                self.config["hide_label_when_full"]
                and battery_percent == self.full_battery_level
            ):
                self.battery_label.hide()

        # Update the tooltip with the battery status details if enabled
        if self.config["tooltip"]:
            tool_tip_text = f"󱐋 Capacity : {capacity}\n Temperature: {temperature}°C"
            if battery_percent == self.full_battery_level:
                self.set_tooltip_text(f"Full\n{tool_tip_text}")
            elif is_charging and battery_percent < self.full_battery_level:
                self.set_tooltip_text(
                    f"󰄉 Time to full: {format_time(time_remaining)}\n{tool_tip_text}"
                )
            else:
                self.set_tooltip_text(
                    f"󰄉 Time to empty: {format_time(time_remaining)}\n{tool_tip_text}"
                )

        return True
