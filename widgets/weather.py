import threading
import time
from datetime import datetime

from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.svg import Svg
from gi.repository import GLib, Gtk
from loguru import logger

from services import WeatherService
from shared import ButtonWidget, Popover
from shared.submenu import ScanButton
from utils import BarConfig
from utils.functions import check_if_day, convert_to_12hr_format
from utils.icons import weather_icons
from utils.widget_utils import (
    text_icon,
    util_fabricator,
)

weather_service = WeatherService()


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def sunrise_sunset_time(self) -> str:
        return f" {self.sunrise_time}  {self.sunset_time}"

    def temperature(self, celsius=True) -> str:
        if celsius:
            return f" {self.current_weather['temp_C']}°C"
        else:
            return f" {self.current_weather['temp_F']}°F"

    def __init__(
        self,
        data,
        **kwargs,
    ):
        super().__init__(
            style_classes="weather-box",
            orientation="v",
            h_expand=True,
            spacing=5,
            **kwargs,
        )
        self.scan_btn = ScanButton(h_align="start", visible=False)

        self.update_time = datetime.now()

        self.scan_btn.connect("clicked", lambda *_: self.scan_btn.play_animation())

        # Get the current weather
        self.current_weather = data["current"]

        # Get the hourly forecast
        self.hourly_forecast = data["hourly"]

        # Get the sunrise and sunset times
        [self.sunrise_time, self.sunset_time] = [
            data["astronomy"]["sunrise"],
            data["astronomy"]["sunset"],
        ]

        self.weather_icons_dir = get_relative_path("../assets/icons/svg/weather")

        self.current_weather_image = Svg(
            svg_file=self.get_weather_asset(self.current_weather["weatherCode"]),
            size=100,
            v_align="start",
            h_align="start",
        )

        self.title_box = Gtk.Grid(
            name="weather-header-grid",
            visible=True,
        )

        self.title_box.attach(
            self.current_weather_image,
            0,
            0,
            2,
            3,
        )

        self.title_box.attach(
            Label(
                style_classes="header-label",
                h_align="start",
                label=f"{data['location']}",
            ),
            2,
            0,
            1,
            1,
        )

        self.title_box.attach(
            Label(
                name="condition",
                h_align="start",
                label=f"{self.current_weather['weatherDesc'][0]['value']}",
            ),
            2,
            1,
            1,
            1,
        )

        self.title_box.attach(
            Label(
                style_classes="header-label",
                name="sunrise-sunset",
                h_align="start",
                label=self.sunrise_sunset_time(),
            ),
            2,
            2,
            1,
            1,
        )

        self.title_box.attach(
            Label(
                style_classes="stats",
                h_align="center",
                label=self.temperature(),
            ),
            3,
            0,
            1,
            1,
        )

        self.title_box.attach(
            Label(
                style_classes="stats",
                h_align="center",
                label=f"󰖎 {self.current_weather['humidity']}%",
            ),
            3,
            1,
            1,
            1,
        )

        self.title_box.attach(
            Label(
                style_classes="stats",
                h_align="center",
                label=f" {self.current_weather['windspeedKmph']} mph",
            ),
            3,
            2,
            1,
            1,
        )

        # Create a grid to display the hourly forecast
        self.forecast_box = Gtk.Grid(
            row_spacing=10,
            column_spacing=20,
            name="weather-grid",
            visible=True,
        )

        expander = Gtk.Expander(
            name="weather-expander",
            visible=True,
            child=self.forecast_box,
        )

        self.children = (self.scan_btn, self.title_box, expander)

        self.update_widget(initial=True)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", lambda *_: self.update_widget())

    def update_widget(self, initial=False):
        if (datetime.now() - self.update_time).total_seconds() < 60 and not initial:
            # Check if the update time is more than 10 minutes ago
            return

        logger.debug("[Weather] Updating weather widget")

        self.update_time = datetime.now()

        current_time = int(time.strftime("%H00"))

        next_values = self.hourly_forecast[:4]

        if current_time > 1200:
            next_values = self.hourly_forecast[4:8]

        # show next 4 hours forecast
        for col in range(4):
            column_data = next_values[col]

            hour = Label(
                style_classes="weather-forecast-time",
                label=f"{convert_to_12hr_format(column_data['time'])}",
                h_align="center",
            )
            icon = Svg(
                svg_file=self.get_weather_asset(
                    column_data["weatherCode"],
                    convert_to_12hr_format(column_data["time"]),
                ),
                size=65,
                h_align="center",
                h_expand=True,
                style_classes="weather-forecast-icon",
            )

            temp = Label(
                style_classes="weather-forecast-temp",
                label=f"{column_data['tempC']}°C",
                h_align="center",
            )
            self.forecast_box.attach(hour, col, 0, 1, 1)
            self.forecast_box.attach(icon, col, 1, 1, 1)
            self.forecast_box.attach(temp, col, 2, 1, 1)

    def get_weather_asset(self, code: int, time_str: str | None = None) -> str:
        is_day = check_if_day(
            sunrise_time=self.sunrise_time,
            sunset_time=self.sunset_time,
            current_time=time_str,
        )
        image_name = "image" if is_day else "image-night"
        return f"{self.weather_icons_dir}/{weather_icons[str(code)][image_name]}.svg"


class WeatherWidget(ButtonWidget):
    """A widget to display the current weather."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config["weather"],
            name="weather",
            **kwargs,
        )

        self.weather_icon = text_icon(
            icon="",
            props={
                "style_classes": "panel-icon",
            },
        )

        self.update_time = datetime.now()

        self.weather_label = Label(
            label="Fetching weather...",
            style_classes="panel-text",
        )
        self.box.children = (self.weather_icon, self.weather_label)

        self.update_ui(initial=True)

        # Set up a fabricator to call the update_label method at specified intervals
        util_fabricator.connect("changed", lambda *_: self.update_ui())

    def fetch_data_from_url(self):
        res = weather_service.get_weather(
            location=self.config["location"], ttl=self.config["interval"]
        )

        # Update label in main GTK thread
        GLib.idle_add(self.update_data, res)

    def update_data(self, res):
        self.update_time = datetime.now()

        if res is None:
            self.weather_label.set_label("")
            self.weather_icon.set_label("")
            if self.config["tooltip"]:
                self.set_tooltip_text("Error fetching weather data")
            return

        current_weather = res["current"]

        # Get the sunrise and sunset times
        [self.sunrise_time, self.sunset_time] = [
            res["astronomy"]["sunrise"],
            res["astronomy"]["sunset"],
        ]

        is_day = check_if_day(
            sunrise_time=self.sunrise_time, sunset_time=self.sunset_time
        )
        text_icon = (
            weather_icons[current_weather["weatherCode"]]["icon"]
            if is_day
            else weather_icons[current_weather["weatherCode"]]["icon-night"]
        )

        self.weather_label.set_label(f"{current_weather['FeelsLikeC']}°C")
        self.weather_icon.set_label(text_icon)

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"{res['location']}, {current_weather['weatherDesc'][0]['value']}"
            )

        popup = Popover(
            content_factory=lambda: WeatherMenu(data=res),
            point_to=self,
        )

        self.connect(
            "clicked",
            lambda *_: popup.open(),
        )

        return False

    # todo check for initial
    def update_ui(self, initial=False):
        if (datetime.now() - self.update_time).total_seconds() < self.config[
            "interval"
        ] and not initial:
            # Check if the update time is more than interval seconds ago
            return

            # Start background service
        threading.Thread(target=self.fetch_data_from_url, daemon=True).start()
