import json
import os
import threading
import time
from typing import Callable, Optional

import requests
from fabric.core.service import Service
from gi.repository import GLib

from utils.constants import WEATHER_CACHE_FILE
from utils.functions import write_json_file


class WeatherService(Service):
    """Lightweight singleton to fetch and cache weather from wttr.in."""

    __slots__ = ("api_url_template", "cache_file")  # prevents __dict__ memory

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
        cache_file: str = WEATHER_CACHE_FILE,
        api_url_template: str = "https://wttr.in/{location}?format=j1",
    ):
        super().__init__()
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.cache_file = cache_file
        self.api_url_template = api_url_template

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

    def simple_weather_info(
        self, location: str, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        session = self._make_session()
        url = self.api_url_template.format(
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

    def get_weather(
        self, location: str, ttl: int = 3600, refresh: bool = False
    ) -> Optional[dict]:
        now = time.time()

        if not refresh and os.path.exists(self.cache_file):
            try:
                if now - os.path.getmtime(self.cache_file) < ttl:
                    with open(self.cache_file, "r") as f:
                        return json.load(f)
            except Exception:
                pass

        weather = self.simple_weather_info(location)
        if weather:
            write_json_file(weather, self.cache_file)

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
        threading.Thread(
            target=self._weather_worker,
            args=(location, ttl, refresh, callback),
            daemon=True,
        ).start()
