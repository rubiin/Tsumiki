import time
from datetime import datetime

import gi
from fabric.utils import bulk_connect, cooldown, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.svg import Svg
from gi.repository import Gtk
from loguru import logger

from services.weather import WeatherService
from shared.widget_container import ButtonWidget
from utils.functions import check_if_day
from utils.icons import weather_icons
from utils.widget_utils import (
    nerd_font_icon,
    reusable_fabricator,
)

gi.require_versions({"Gtk": "3.0"})


class BaseWeatherWidget:
    """Base class for weather widgets."""

    def get_description(self):
        return self.current_weather["weatherDesc"][0]["value"]

    def get_humidity(self):
        return self.current_weather["humidity"] + "%"

    def sunrise_sunset_time(self) -> str:
        return f" {self.sunrise_time}  {self.sunset_time}"

    def update_app_data(self, data):
        """Update the weather data."""
        self.data = data

        # Get the current weather
        self.current_weather = self.data["current"]

        # Get the hourly forecast
        self.hourly_forecast = self.data["hourly"]

        # Update sunrise and sunset times
        # Get the sunrise and sunset times
        self.sunrise_time = self.data["astronomy"]["sunrise"]
        self.sunset_time = self.data["astronomy"]["sunset"]

        return True

    def get_wind_speed(self):
        if self.config.get("wind_speed_unit", "kmh") == "kmh":
            return self.current_weather["windspeedKmph"] + " Km/h"

        return self.current_weather["windspeedMiles"] + " Mph"

    def get_temperature(self):
        """Get the current temperature in the specified unit."""

        if self.config.get("temperature_unit", "celsius") == "celsius":
            return self.current_weather["temp_C"] + "°C"

        return self.current_weather["temp_F"] + "°F"

    def get_temperature_hour(self, index):
        """Get the temperature for a specific hour in the specified unit."""

        if self.config.get("temperature_unit", "celsius") == "celsius":
            return self.hourly_forecast[index]["tempC"] + "°C"

        return self.hourly_forecast[index]["tempF"] + "°F"

        # wttr.in time are in 300,400...2100 format ,
        #  we need to convert it to 4:00...21:00

    def convert_to_12hr_format(self, time: str) -> str:
        time = int(time)
        hour = time // 100  # Get the hour (e.g., 1200 -> 12)
        minute = time % 100  # Get the minutes (e.g., 1200 -> 00)

        # Convert to 12-hour format
        period = "AM" if hour < 12 else "PM"

        # Adjust hour for 12-hour format
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        # Format the time as a string
        return f"{hour}:{minute:02d} {period}"


class WeatherMenu(Box, BaseWeatherWidget):
    """A menu to display the weather information."""

    def __init__(
        self,
        config,
        **kwargs,
    ):
        super().__init__(
            style_classes="weather-box",
            orientation="v",
            h_expand=True,
            spacing=5,
            **kwargs,
        )

        self.config = config

        self.next_values = None

        self.update_time = datetime.now()

        self.weather_icons_dir = get_relative_path("../assets/icons/svg/weather")

        self.current_weather_image = Svg(
            svg_file=f"{self.weather_icons_dir}/clear-day.svg",
            v_align="start",
            h_align="start",
            size=100,
        )

        self.title_box = Grid(
            name="weather-header-grid",
            column_spacing=20,
        )

        self.location = Label(
            style_classes="header-label",
            h_align="start",
            label="",
        )

        self.weather_description = Label(
            style_classes="header-label",
            h_align="start",
            label="",
        )

        self.humidity = Label(
            style_classes="header-label",
            h_align="start",
            label="",
        )

        self.wind_speed = Label(
            style_classes="header-label",
            h_align="start",
            label="",
        )

        self.temperature = Label(
            style_classes="header-label",
            h_align="start",
            label="",
        )

        self.sunset_sunrise = Label(
            style_classes="header-label",
            h_align="start",
            name="sunrise-sunset",
            label="",
        )

        self.title_box.attach(
            self.current_weather_image,
            0,
            0,
            2,
            3,
        )

        self.title_box.attach(
            self.location,
            2,
            0,
            1,
            1,
        )

        self.title_box.attach(
            self.weather_description,
            2,
            1,
            1,
            1,
        )

        self.title_box.attach(
            self.sunset_sunrise,
            2,
            2,
            1,
            1,
        )

        self.title_box.attach(
            self.temperature,
            3,
            0,
            1,
            1,
        )

        self.title_box.attach(
            self.humidity,
            3,
            1,
            1,
            1,
        )

        self.title_box.attach(
            self.wind_speed,
            3,
            2,
            1,
            1,
        )

        # Create a grid to display the hourly forecast
        self.forecast_box = Grid(
            row_spacing=10,
            column_spacing=20,
            name="weather-grid",
        )

        expander = Gtk.Expander(
            name="weather-expander",
            visible=True,
            child=self.forecast_box,
            expanded=self.config.get("expanded", True),
        )

        self.children = (self.title_box, expander)

        WeatherService().get_weather_async(
            location=self.config.get("location", ""),
            ttl=self.config.get("interval", 3600),
            callback=self.update_data,
        )

        # reusing the fabricator to call specified intervals
        reusable_fabricator.connect("changed", self.update_widget)

    def update_data(self, data):
        self.update_app_data(data)

        self.update_widget(forced=True)

    def update_widget(self, *args, **kwargs):
        forced = kwargs.get("forced", False)

        # Check if the update time is more than 4 minute ago
        if (datetime.now() - self.update_time).total_seconds() < 60 and not forced:
            return

        logger.debug("[Weather] Updating weather widget")

        self.update_time = datetime.now()

        current_time = int(time.strftime("%H00"))

        if forced:
            self.current_weather_image.set_from_file(
                self.get_weather_asset(self.current_weather["weatherCode"]),
            )

            self.location.set_label(self.data["location"])
            self.weather_description.set_label(self.get_description())
            self.sunset_sunrise.set_label(self.sunrise_sunset_time())
            self.humidity.set_label(f"󰖎 {self.get_humidity()}")
            self.temperature.set_label(f"  {self.get_temperature()}")
            self.wind_speed.set_label(f" {self.get_wind_speed()}")

        self.next_values = self.hourly_forecast[:4]

        if current_time > 1200:
            self.next_values = self.hourly_forecast[4:8]

            # clear the forecast box
            for child in self.forecast_box.get_children():
                self.forecast_box.remove(child)

        # show next 4 hours forecast, run this once on boot and after 1200

        if forced or current_time > 1200:
            for col, value in enumerate(self.next_values):
                hour = Label(
                    style_classes="weather-forecast-time",
                    label=f"{self.convert_to_12hr_format(value['time'])}",
                    h_align="center",
                )
                icon = Svg(
                    svg_file=self.get_weather_asset(
                        value["weatherCode"],
                        self.convert_to_12hr_format(value["time"]),
                    ),
                    size=65,
                    h_align="center",
                    h_expand=True,
                    style_classes="weather-forecast-icon",
                )

                temp = Label(
                    style_classes="weather-forecast-temp",
                    label=self.get_temperature_hour(col),
                    h_align="center",
                )
                self.forecast_box.attach(hour, col, 0, 1, 1)
                self.forecast_box.attach(icon, col, 1, 1, 1)
                self.forecast_box.attach(temp, col, 2, 1, 1)

    def get_weather_asset(self, code: int, time_str: str | None = None) -> str:
        is_day = check_if_day(
            current_time=time_str,
            sunrise_time=self.sunrise_time,
            sunset_time=self.sunset_time,
        )
        image_name = "image" if is_day else "image-night"
        return f"{self.weather_icons_dir}/{weather_icons[str(code)][image_name]}.svg"


class WeatherWidget(ButtonWidget, BaseWeatherWidget):
    """A widget to display the current weather."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="weather",
            **kwargs,
        )

        self.weather_icon = nerd_font_icon(
            icon="󱣶",
            props={
                "style_classes": "panel-font-icon",
            },
        )
        self.box.add(self.weather_icon)

        self.popover = None

        self.connect("button-press-event", self.on_button_press)

        self.update_time = datetime.now()

        if self.config.get("label", True):
            self.weather_label = Label(
                label="Fetching..",
                style_classes="panel-text",
            )

            if self.config.get("hover_reveal", True):
                self.revealer = Revealer(
                    child=self.weather_label,
                    transition_duration=500,
                    transition_type="slide_right",
                )
                self.box.add(self.revealer)
            else:
                self.box.add(self.weather_label)

        self.update_ui(forced=True)

        # Set up a fabricator to call the update_label method at specified intervals
        reusable_fabricator.connect("changed", self.update_ui)

        if self.config.get("hover_reveal", True):
            # Connect to enter and leave events to toggle the revealer
            bulk_connect(
                self,
                {
                    "enter-notify-event": self._toggle_revealer,
                    "leave-notify-event": self._toggle_revealer,
                },
            )

    def _toggle_revealer(self, *_):
        if hasattr(self, "revealer"):
            self.revealer.set_reveal_child(not self.revealer.get_reveal_child())

    def update_data(self, data):
        self.update_time = datetime.now()

        if data is None:
            self.weather_label.set_label("")
            self.weather_icon.set_label("")
            if self.config.get("tooltip", False):
                self.set_tooltip_text(
                    "Error fetching weather data,\nright click to refetch."
                )
            return

        # Get the current weather
        self.update_app_data(data)

        weather_icon = weather_icons[self.current_weather["weatherCode"]]

        text_icon = (
            weather_icon["icon"]
            if check_if_day(
                sunrise_time=self.sunrise_time, sunset_time=self.sunset_time
            )
            else weather_icon["icon-night"]
        )

        self.weather_icon.set_label(text_icon)

        if self.config.get("label", True):
            self.weather_label.set_label(
                self.config.get("label_format", "{location}").format(
                    location=self.data["location"],
                    temperature=self.get_temperature(),
                    condition=self.get_description(),
                    humidity=self.get_humidity(),
                    wind_speed=self.get_wind_speed(),
                )
            )

        # Update the tooltip with the city and weather condition if enabled
        if self.config.get("tooltip", False):
            tool_tip = f"{self.get_temperature()} {self.get_description()}"
            tool_tip += f"\n\n{weather_icon['quote']}"

            self.set_tooltip_text(tool_tip)

        # Create popover only once

        if self.popover is None:
            from shared.popover import Popover

            self.popover = Popover(
                content=WeatherMenu(config=self.config),
                point_to=self,
            )

        return False

    @cooldown(1)
    def on_button_press(self, _, event):
        if event.button == 1:
            self.popover.open() if self.popover else None
            return
        else:
            if self.config.get("label", True):
                self.weather_label.set_label("Fetching..")

            self.weather_icon.set_label("󱣶")
            self.update_ui(forced=True)

    def update_ui(self, *args, **kwargs):
        forced = kwargs.get("forced", False)

        # Check if the update time is more than 5 minutes ago, update the icon
        if (datetime.now() - self.update_time).total_seconds() > 300:
            text_icon = (
                weather_icons[self.current_weather["weatherCode"]]["icon"]
                if check_if_day(
                    sunrise_time=self.sunrise_time,
                    sunset_time=self.sunset_time,
                )
                else weather_icons[self.current_weather["weatherCode"]]["icon-night"]
            )

            self.weather_icon.set_label(text_icon)

        if (datetime.now() - self.update_time).total_seconds() < self.config[
            "interval"
        ] and not forced:
            # Check if the update time is more than interval seconds ago
            return

        WeatherService().get_weather_async(
            location=self.config.get("location", ""),
            ttl=self.config.get("interval", 3600),
            callback=self.update_data,
        )
