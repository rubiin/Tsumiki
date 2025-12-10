import json
import os
import threading
import time
from contextlib import suppress
from typing import Callable, Optional

import requests
from fabric.core.service import Service
from fabric.utils import logger
from gi.repository import GLib

from utils.constants import WEATHER_CACHE_FILE
from utils.functions import write_json_file
from utils.thread import thread


class WeatherService(Service):
    """Lightweight singleton to fetch and cache weather from Open-Meteo or wttr.in."""

    __slots__ = (
        "api_url",
        "cache_file",
        "geocode_url",
        "provider",
        "wttr_url_template",
    )  # prevents __dict__ memory

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        api_url: str = "https://api.open-meteo.com/v1/forecast",
        geocode_url: str = "https://nominatim.openstreetmap.org/search",
        provider: str = "open-meteo",  # "open-meteo" or "wttr"
        wttr_url_template: str = "https://wttr.in/{location}?format=j1",
    ):
        super().__init__()
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.api_url = api_url
        self.geocode_url = geocode_url
        self.provider = provider.lower()
        self.wttr_url_template = wttr_url_template

    def _make_session(self) -> requests.Session:
        """Create a throwaway session to avoid holding state in memory."""
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                )
            }
        )
        return session

    def _geocode_location(self, location: str) -> Optional[tuple[float, float]]:
        """Convert location name to latitude and longitude using Nominatim."""
        session = self._make_session()
        params = {
            "q": location,
            "format": "json",
            "limit": 1,
        }

        try:
            response = session.get(self.geocode_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon
        except Exception:
            pass

        return None

    def _map_weather_code(self, code: int) -> int:
        """Map Open-Meteo weather codes to wttr.in compatible codes."""
        # Open-Meteo weather codes to wttr.in mapping
        mapping = {
            0: 113,  # Clear sky
            1: 116,  # Mainly clear -> Partly cloudy
            2: 119,  # Partly cloudy
            3: 122,  # Overcast
            45: 143,  # Fog
            48: 143,  # Depositing rime fog
            51: 176,  # Light drizzle
            53: 176,  # Moderate drizzle
            55: 176,  # Dense drizzle
            56: 182,  # Light freezing drizzle
            57: 182,  # Dense freezing drizzle
            61: 293,  # Slight rain
            63: 302,  # Moderate rain
            65: 308,  # Heavy rain
            66: 281,  # Light freezing rain
            67: 284,  # Heavy freezing rain
            71: 338,  # Slight snow fall
            73: 371,  # Moderate snow fall
            75: 395,  # Heavy snow fall
            77: 371,  # Snow grains
            80: 353,  # Slight rain showers
            81: 356,  # Moderate rain showers
            82: 359,  # Violent rain showers
            85: 368,  # Slight snow showers
            86: 395,  # Heavy snow showers
            95: 389,  # Thunderstorm
            96: 392,  # Thunderstorm with slight hail
            99: 395,  # Thunderstorm with heavy hail
        }
        return mapping.get(code, 113)  # Default to clear sky

    def _convert_to_12hr_format(self, time_24hr: str) -> str:
        """Convert 24-hour time format (HH:MM) to 12-hour format (HH:MM AM/PM)."""
        if not time_24hr or ":" not in time_24hr:
            return time_24hr

        try:
            hour, minute = map(int, time_24hr.split(":"))
            period = "AM" if hour < 12 else "PM"

            if hour == 0:
                hour = 12
            elif hour > 12:
                hour -= 12

            return f"{hour}:{minute:02d} {period}"
        except (ValueError, IndexError):
            return time_24hr

    def _get_weather_description(self, code: int) -> str:
        """Get weather description from Open-Meteo weather code."""
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return descriptions.get(code, "Clear sky")

    def simple_weather_info(
        self, location: str, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        """Fetch weather data from the configured API provider."""
        if self.provider == "wttr":
            return self._fetch_wttr_weather(location, retries, delay)
        elif self.provider == "open-meteo":
            return self._fetch_openmeteo_weather(location, retries, delay)
        else:
            # Default to open-meteo
            return self._fetch_openmeteo_weather(location, retries, delay)

    def _fetch_wttr_weather(
        self, location: str, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        """Fetch weather data from wttr.in API."""
        session = self._make_session()
        url = self.wttr_url_template.format(
            location=requests.utils.quote(location.title())
        )

        for attempt in range(retries):
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Extract only necessary parts and discard rest
                return {
                    "location": (
                        data.get("nearest_area", [{}])[0]
                        .get("areaName", [{}])[0]
                        .get("value", location)
                        .capitalize()
                    ),
                    "current": data.get("current_condition", [{}])[0],
                    "hourly": data.get("weather", [{}])[0].get("hourly", []),
                    "astronomy": data.get("weather", [{}])[0].get("astronomy", [{}])[0],
                }

            except Exception:
                time.sleep(delay * (attempt + 1))

        return None

    def _fetch_openmeteo_weather(
        self, location: str, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        """Fetch weather data from Open-Meteo API."""
        session = self._make_session()

        # First, geocode the location
        coords = self._geocode_location(location)
        if not coords:
            return None

        lat, lon = coords

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m,weathercode",
            "daily": "sunrise,sunset",
            "timezone": "auto",
            "forecast_days": 1,
        }

        for attempt in range(retries):
            try:
                response = session.get(self.api_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Transform Open-Meteo data to wttr.in compatible format
                current_weather = data.get("current_weather", {})
                hourly = data.get("hourly", {})
                daily = data.get("daily", {})

                if not current_weather or not hourly:
                    continue

                # Get current time index
                current_time = current_weather.get("time", "")
                if current_time:
                    # Find the index of current time in hourly data
                    try:
                        current_index = hourly["time"].index(current_time)
                    except ValueError:
                        current_index = 0
                else:
                    current_index = 0

                # Build wttr.in compatible structure
                weather_data = {
                    "location": location.title(),
                    "current": {
                        "weatherDesc": [
                            {
                                "value": self._get_weather_description(
                                    current_weather.get("weathercode", 0)
                                )
                            }
                        ],
                        "humidity": str(hourly["relative_humidity_2m"][current_index]),
                        "windspeedKmph": str(
                            int(current_weather.get("windspeed", 0) * 3.6)
                        ),  # m/s to km/h
                        "windspeedMiles": str(
                            int(current_weather.get("windspeed", 0) * 2.237)
                        ),  # m/s to mph
                        "temp_C": str(int(current_weather.get("temperature", 0))),
                        "temp_F": str(
                            int(current_weather.get("temperature", 0) * 9 / 5 + 32)
                        ),
                        "weatherCode": str(
                            self._map_weather_code(
                                current_weather.get("weathercode", 0)
                            )
                        ),
                    },
                    "hourly": [],
                    "astronomy": {
                        "sunrise": self._convert_to_12hr_format(
                            daily.get("sunrise", [""])[0].split("T")[1]
                            if daily.get("sunrise")
                            else ""
                        ),
                        "sunset": self._convert_to_12hr_format(
                            daily.get("sunset", [""])[0].split("T")[1]
                            if daily.get("sunset")
                            else ""
                        ),
                    },
                }

                # Build hourly forecast (next 24 hours)
                for i in range(min(24, len(hourly["time"]))):
                    hour_time = (
                        hourly["time"][i].split("T")[1].replace(":", "")
                    )  # HHMM format
                    weather_data["hourly"].append(
                        {
                            "time": hour_time,
                            "weatherCode": str(
                                self._map_weather_code(hourly["weathercode"][i])
                            ),
                            "tempC": str(int(hourly["temperature_2m"][i])),
                            "tempF": str(int(hourly["temperature_2m"][i] * 9 / 5 + 32)),
                        }
                    )

                return weather_data

            except Exception as e:
                logger.error("Error fetching weather data: %s", e)
                time.sleep(delay * (attempt + 1))

        return None

    def get_weather(
        self, location: str, ttl: int = 3600, refresh: bool = False
    ) -> Optional[dict]:
        now = time.time()

        if not refresh and os.path.exists(WEATHER_CACHE_FILE):
            try:
                if now - os.path.getmtime(WEATHER_CACHE_FILE) < ttl:
                    with open(WEATHER_CACHE_FILE, "r") as f:
                        cached_data = json.load(f)
                        # Check if cached provider and location match current ones
                        cached_provider = cached_data.get("provider")
                        cached_location = cached_data.get("cached_location")
                        if (
                            cached_provider == self.provider
                            and cached_location == location
                        ):
                            return cached_data
                        else:
                            # Provider or location mismatch, remove old cache
                            with suppress(OSError, PermissionError):
                                os.remove(WEATHER_CACHE_FILE)
            except (json.JSONDecodeError, OSError, PermissionError) as e:
                logger.warning(
                    "Failed to read cache file, will fetch fresh data: %s", e
                )
                # Remove corrupted cache file
                with suppress(OSError, PermissionError):
                    os.remove(WEATHER_CACHE_FILE)
            except Exception as e:
                logger.error("Unexpected error reading cache: %s", e)
                # Remove potentially corrupted cache file
                with suppress(OSError, PermissionError):
                    os.remove(WEATHER_CACHE_FILE)

        weather = self.simple_weather_info(location)
        if weather:
            # Add provider and location to cached data
            weather["provider"] = self.provider
            weather["cached_location"] = location
            write_json_file(WEATHER_CACHE_FILE, weather)

        return weather

    def _weather_worker(
        self,
        location: str,
        ttl: int,
        refresh: bool,
        callback: Callable[[Optional[dict]], None],
    ):
        result = self.get_weather(location, ttl=ttl, refresh=refresh)
        GLib.idle_add(callback, result)

    def get_weather_async(
        self,
        location: str,
        callback: Callable[[Optional[dict]], None],
        ttl: int = 3600,
        refresh: bool = False,
    ):
        thread(self._weather_worker, location, ttl, refresh, callback)

    def set_provider(self, provider: str):
        """Set the weather API provider ('open-meteo' or 'wttr')."""
        self.provider = provider.lower()
        # Cache will be invalidated automatically when provider mismatch is detected
