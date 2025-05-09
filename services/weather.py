import json
import os
import ssl
import time
import urllib.request
from urllib.error import HTTPError

from fabric.core.service import Service
from loguru import logger

from utils import Colors
from utils.constants import WEATHER_CACHE_FILE

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService(Service):
    """This class provides weather information for a given city."""

    _instance = None  # Class-level private instance variable

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WeatherService, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def simple_weather_info(self, location: str):
        try:
            url = ""
            # Construct the URL for fetching weather information
            if location != "":
                encoded_location = urllib.parse.quote_plus(location.capitalize())

                url = f"http://wttr.in/{encoded_location}?format=j1"
            else:
                url = "http://wttr.in/?format=j1"

            logger.info(f"[WeatherService] Fetching weather information from {url}")
            contents = (
                urllib.request.urlopen(url, context=context, timeout=10)
                .read()
                .decode("utf-8")
            )

            # Parse the weather information
            data = json.loads(contents)

            current_weather = data["current_condition"][0]
            weather = data["weather"][0]
            hourly_weather = weather["hourly"]
            location = data["nearest_area"][0]["areaName"][0]["value"]

            return {
                "location": location.capitalize(),
                "current": current_weather,  # the current weather information
                "hourly": hourly_weather,  # tri-hourly data for the next 24 hours
                "astronomy": weather["astronomy"][0],  # the sunrise and sunset times
            }

        except HTTPError as e:
            if e.code == 404:
                logger.error(
                    f"{Colors.ERROR}[WeatherService] Error: City not found. Try a different city."  # noqa: E501
                )
            return None
        except Exception as e:
            logger.exception(f"[WeatherService] Error: {e}")
            return None

    def get_weather(self, location: str, ttl=3600, refresh=False):
        if not refresh:
            # Check if cache exists and is fresh
            if os.path.exists(WEATHER_CACHE_FILE):
                last_modified = os.path.getmtime(WEATHER_CACHE_FILE)
                logger.info(
                    f"{Colors.INFO}[WeatherService] Reading weather from cache file{WEATHER_CACHE_FILE}"  # noqa: E501
                )

                if time.time() - last_modified < ttl:  # 1 hour
                    with open(WEATHER_CACHE_FILE, "r") as f:
                        return json.load(f)

            logger.info(
                (
                    f"{Colors.INFO}[WeatherService] Cache file {WEATHER_CACHE_FILE} stale, Fetching new data."  # noqa: E501
                )
            )

        weather = self.simple_weather_info(location)

        # If the weather data is None, return None
        if weather is None:
            return None
        # Save the weather data to the cache file
        with open(WEATHER_CACHE_FILE, "w") as f:
            json.dump(weather, f, indent=4, ensure_ascii=False)

        return weather
