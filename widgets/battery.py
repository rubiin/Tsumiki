from services.battery import BatteryService
from shared.widget_container import ButtonWidget
from utils.functions import format_seconds_to_hours_minutes, send_notification
from utils.icons import get_text_icon
from utils.widget_utils import nerd_font_icon


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
        self.hide_percent_when_full = self.config.get("hide_percent_when_full", True)
        self.label_format = self.config.get("label_format", "{icon} {percent}")
        self.glyphs = self.config.get("icons", ["", "", "", "", ""])

        self.battery_icon = nerd_font_icon(
            icon=get_text_icon("battery.charging"),
            props={"style_classes": ["panel-font-icon", "battery-icon"]},
        )
        self.container_box.add(self.battery_icon)

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
            self.set_tooltip_text(f"{get_text_icon('battery.low')} No battery present")
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

        glyph = self._map_glyph(battery_percent, is_charging)

        formatted_time = format_seconds_to_hours_minutes(time_remaining)
        percent_color = self._get_color_for_percent(battery_percent)

        label_format = self.label_format

        if battery_percent == self.full_battery_level:
            label_format = (
                label_format.replace("{percent}", "")
                if self.hide_percent_when_full
                else label_format
            )

        label_text = label_format.format(
            icon=glyph,
            time_remaining=formatted_time,
            percent=f"{battery_percent}%",
        )

        self.battery_icon.set_markup(
            f'<span foreground="{percent_color}">{label_text}</span>'
        )

        # Update the tooltip with the battery status details if enabled
        if self.config.get("tooltip", False) and self.tooltips_enabled:
            status_text = (
                "󱠴 Status: Charging" if is_charging else "󱠴 Status: Discharging"
            )
            tool_tip_text = (
                f"󱐋 Energy : {round(energy, 2)} Wh\n Temperature: {temperature}°C"
            )

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

    def _map_glyph(self, percent: float, charging: bool) -> str:
        if charging:
            return get_text_icon("battery.charging")

        index = int(percent // 20)
        index = min(index, len(self.glyphs) - 1)
        return self.glyphs[index]

    def _get_color_for_percent(self, percent: float) -> str:
        """Return a pastel gradient color from red to green based on percent."""

        percent = max(0, min(percent, 100)) / 100.0

        # Pastel red (low %) to pastel green (high %)
        red_start, green_start, blue_start = (252, 56, 56)  # pastel red
        red_end, green_end, blue_end = (99, 252, 23)  # pastel green

        # Linear interpolation
        r = int(red_start + (red_end - red_start) * percent)
        g = int(green_start + (green_end - green_start) * percent)
        b = int(blue_start + (blue_end - blue_start) * percent)

        return f"#{r:02x}{g:02x}{b:02x}"
