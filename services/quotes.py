import os
import random
import time
from typing import Callable, Optional

import requests
from gi.repository import GLib

from utils.constants import QUOTES_CACHE_FILE
from utils.functions import read_json_file, write_json_file

from .base import SingletonService


class QuotesService(SingletonService):
    """Lightweight singleton to fetch and cache quotes from ZenQuotes API."""

    __slots__ = ("api_url", "cache_file")  # prevents __dict__ memory

    def __init__(
        self,
    ):
        super().__init__()
        self.api_url = "https://zenquotes.io/api/quotes/"

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

    def simple_quotes_info(
        self, retries: int = 3, delay: float = 2.0
    ) -> Optional[dict]:
        session = self._make_session()

        for attempt in range(retries):
            try:
                response = session.get(self.api_url, timeout=10)
                response.raise_for_status()

                return response.json()

            except Exception:
                time.sleep(delay * (attempt + 1))

        return None

    def get_quotes(self) -> Optional[dict]:
        quotes = None

        if os.path.exists(QUOTES_CACHE_FILE):
            quotes = read_json_file(QUOTES_CACHE_FILE)
            return random.choice(quotes) if quotes else None

        quotes = self.simple_quotes_info()
        if quotes:
            write_json_file(QUOTES_CACHE_FILE, quotes)

        return random.choice(quotes) if quotes else None

    def _quotes_worker(self, callback: Callable[[Optional[dict]], None]):
        result = self.get_quotes()
        GLib.idle_add(callback, result)

    def get_quotes_async(
        self,
        callback: Callable[[Optional[dict]], None],
    ):
        from utils.decorators import thread

        thread(self._quotes_worker, callback)
