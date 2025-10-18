from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.battery import BatteryService
from shared.widget_container import ButtonWidget
from utils.functions import format_seconds_to_hours_minutes, send_notification
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

        self.container_box.add(self.battery_icon)

        if self.config.get("label", True):
            self.battery_label = Label(label="100%", style_classes=["panel-text"])
            self.container_box.add(self.battery_label)

        self.client = BatteryService()

        # Simple notification tracking
        self.last_percentage = None
        self.last_charging_state = None
        self.low_battery_notified = False
        self.full_battery_notified = False
        self.charging_notified = False
        self.discharging_notified = False
        self.initialized = False

        self.client.connect("changed", self._update_ui)

        self._update_ui()

    def _update_ui(self, *_):
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
            self.client.get_property("IconName"), self.config.get("icon_size", 16)
        )

        # Update the label with the battery percentage if enabled
        if self.config.get("label", True):
            self.battery_label.set_text(f"{battery_percent}%")
            self.battery_label.show()

            ## Hide the label when the battery is full
            if (
                self.config.get("hide_label_when_full", False)
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

        # Check for notifications
        if self.initialized:
            self._check_notifications(battery_percent, is_charging)

        # Update tracking variables
        self.last_percentage = battery_percent
        self.last_charging_state = is_charging
        self.initialized = True

        return True

    def _check_notifications(self, percentage, is_charging):
        """Simple notification checking."""
        notifications = self.config.get("notifications", {})
        last_state_available = self.last_charging_state is not None

        # Handle state transitions for charging, discharging, and full battery
        if last_state_available:
            is_full = percentage >= self.full_battery_level

            # Transition from charging to not charging (could be disconnected or full)
            if not is_charging and self.last_charging_state:
                # Full battery event takes precedence
                if (
                    is_full
                    and notifications.get("full_battery", False)
                    and not self.full_battery_notified
                ):
                    send_notification(
                        title="Battery Full",
                        body=f"Battery charged to {percentage}%",
                        urgency="normal",
                        icon="battery-full",
                        app_name="Battery",
                    )
                    self.full_battery_notified = True
                    self.charging_notified = False
                    self.discharging_notified = False
                # Disconnected event
                elif (
                    not is_full
                    and notifications.get("charging", False)
                    and not self.discharging_notified
                ):
                    send_notification(
                        title="Charger Disconnected",
                        body=f"Battery at {percentage}% - On battery power",
                        urgency="normal",
                        icon="battery",
                        app_name="Battery",
                    )
                    self.discharging_notified = True
                    self.charging_notified = False

            # Transition to charging
            elif (
                is_charging
                and not self.last_charging_state
                and notifications.get("charging", False)
                and not self.charging_notified
            ):
                send_notification(
                    title="Charger Connected",
                    body=f"Battery at {percentage}% - Charging",
                    urgency="normal",
                    icon="battery-charging",
                    app_name="Battery",
                )
                self.charging_notified = True
                self.discharging_notified = False

        # Reset full battery flag when no longer full
        if percentage < self.full_battery_level:
            self.full_battery_notified = False

        # Low battery notification
        if notifications.get("low_battery", False):
            threshold = notifications.get("low_threshold", 10)
            if (
                percentage <= threshold
                and not is_charging
                and not self.low_battery_notified
                and (self.last_percentage is None or self.last_percentage > threshold)
            ):
                send_notification(
                    title="Low Battery",
                    body=f"Battery at {percentage}%",
                    urgency="critical",
                    icon="battery-caution",
                    app_name="Battery",
                )
                self.low_battery_notified = True
            elif percentage > threshold or is_charging:
                self.low_battery_notified = False
