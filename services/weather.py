import json
import os
import threading
import time
from typing import Callable, Optional

import requests
from fabric.core.service import Service
from gi.repository import GLib
from loguru import logger

from utils.colors import Colors
from utils.constants import WEATHER_CACHE_FILE


class WeatherService(Service):
    """A singleton service to fetch and cache weather information from wttr.in."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                )
            }
        )

    def simple_weather_info(
        self, location: str, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        url = f"https://wttr.in/{requests.utils.quote(location.title())}?format=j1"

        for attempt in range(1, retries + 1):
            try:
                logger.info(
                    f"[WeatherService] Fetching weather from {url} (Attempt {attempt})"
                )
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                current_weather = data.get("current_condition", [{}])[0]
                weather = data.get("weather", [{}])[0]
                hourly_weather = weather.get("hourly", [])
                astronomy = weather.get("astronomy", [{}])[0]
                area_name = (
                    data.get("nearest_area", [{}])[0]
                    .get("areaName", [{}])[0]
                    .get("value", location)
                )

                return {
                    "location": area_name.capitalize(),
                    "current": current_weather,
                    "hourly": hourly_weather,
                    "astronomy": astronomy,
                }

            except requests.HTTPError as e:
                if response.status_code == 404:
                    logger.error(
                        f"{Colors.ERROR}[WeatherService] City not found: {location}"
                    )
                    return None
                logger.warning(f"[WeatherService] HTTP error: {e}")
            except Exception as e:
                logger.warning(f"[WeatherService] Network error: {e}")

            time.sleep(delay * attempt)  # exponential backoff

        logger.error("[WeatherService] Failed after retries.")
        return None

    def get_weather(self, location: str, ttl=3600, refresh=False) -> Optional[dict]:
        if not refresh and os.path.exists(WEATHER_CACHE_FILE):
            last_modified = os.path.getmtime(WEATHER_CACHE_FILE)
            if time.time() - last_modified < ttl:
                logger.info(
                    f"[WeatherService] Using cached weather: {WEATHER_CACHE_FILE}"
                )
                try:
                    with open(WEATHER_CACHE_FILE, "r") as f:
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"[WeatherService] Failed to load cache: {e}")

        logger.info("[WeatherService] Cache stale or missing. Fetching new data.")
        weather = self.simple_weather_info(location)

        if weather:
            try:
                with open(WEATHER_CACHE_FILE, "w") as f:
                    json.dump(weather, f, indent=4, ensure_ascii=False)
            except Exception as e:
                logger.warning(f"[WeatherService] Failed to write cache: {e}")

        return weather

    def get_weather_async(
        self,
        location: str,
        callback: Callable[[Optional[dict]], None],
        ttl: int = 3600,
        refresh: bool = False,
    ):
        def worker():
            result = self.get_weather(location, ttl=ttl, refresh=refresh)
            GLib.idle_add(callback, result)

        threading.Thread(target=worker, daemon=True).start()
