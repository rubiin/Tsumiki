import json
import os
import ssl
import time
from urllib import error, parse, request

from fabric.core.service import Service
from loguru import logger

from utils.colors import Colors
from utils.constants import WEATHER_CACHE_FILE

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService(Service):
    """This class provides weather information for a given city."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WeatherService, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = request.build_opener()
        self.request.addheaders = [
            (
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa: E501
            )
        ]

    def simple_weather_info(self, location: str):
        try:
            url = f"https://wttr.in/{parse.quote_plus(location.title())}?format=j1"

            logger.info(f"[WeatherService] Fetching weather information from {url}")

            # Open the URL and read the contents
            contents = self.request.open(url, timeout=20).read().decode("utf-8")

            # Parse the weather information
            logger.log(f"{Colors.INFO}[WeatherService] Parsing weather information")
            # Use json.loads to parse the JSON data

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

        except error.HTTPError as e:
            if e.code == 404:
                logger.exception(
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
