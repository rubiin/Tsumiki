"""Launcher slash command: /search — web search results in the launcher.

Searches DuckDuckGo (keyless, no API key) and shows the top results right
in the launcher; pressing Enter opens the selected result in your default
browser. ``handle`` runs on a worker thread, so typing stays responsive
while the request is in flight.

Examples:
    /search fabric hyprland
    /search python httpx timeout
"""

import re
import shlex
from html.parser import HTMLParser
from typing import ClassVar
from urllib.parse import parse_qs, urlencode, urlparse

from fabric.utils import exec_shell_command_async

from utils.functions import get_http_client
from utils.plugin_manager import (
    LauncherPlugin,
    PluginResult,
    copy_to_clipboard,
)

_DDG_HTML_URL = "https://html.duckduckgo.com/html/"
_MAX_RESULTS = 10

#: DuckDuckGo wraps result links in a redirect URL: //duckduckgo.com/l/?uddg=...
_DDG_REDIRECT_RE = re.compile(r"^//duckduckgo\.com/l/\?")


def resolve_url(href: str) -> str:
    """Decode a DuckDuckGo result link to the real destination URL."""
    if _DDG_REDIRECT_RE.match(href):
        query = parse_qs(urlparse(href).query)
        if query.get("uddg"):
            # parse_qs already decodes percent-encoding — don't unquote again
            # or URLs containing literal %xx sequences would be corrupted.
            return query["uddg"][0]
    if href.startswith("//"):
        return f"https:{href}"
    return href


class _ResultParser(HTMLParser):
    """Extract (title, url, snippet) triples from DuckDuckGo result HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.results: list[tuple[str, str, str]] = []
        self._in_link = False
        self._in_snippet = False
        self._href = ""
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "a" and "result__a" in classes:
            self._in_link = True
            self._href = attrs.get("href", "")
            self._buf = []
        elif tag == "a" and "result__snippet" in classes:
            self._in_snippet = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "a" and self._in_link:
            title = " ".join("".join(self._buf).split())
            if title and self._href:
                self.results.append((title, resolve_url(self._href), ""))
            self._in_link = False
        elif tag == "a" and self._in_snippet:
            snippet = " ".join("".join(self._buf).split())
            if self.results:
                title, url, _ = self.results[-1]
                self.results[-1] = (title, url, snippet)
            self._in_snippet = False

    def handle_data(self, data):
        if self._in_link or self._in_snippet:
            self._buf.append(data)


def parse_results(page: str, limit: int = _MAX_RESULTS) -> list[tuple[str, str, str]]:
    """Return up to *limit* (title, url, snippet) triples from DDG HTML."""
    parser = _ResultParser()
    try:
        parser.feed(page)
    except Exception:
        return []
    return parser.results[:limit]


def search(
    query: str, limit: int = _MAX_RESULTS, cancelled=None
) -> list[tuple[str, str, str]]:
    """Search DuckDuckGo and return (title, url, snippet) triples.

    *cancelled* is an optional zero-arg callable returning True when the
    query has been superseded; the request result is then discarded instead
    of parsed.
    """
    if cancelled is not None and cancelled():
        return []
    response = get_http_client().get(_DDG_HTML_URL, params={"q": query})
    if cancelled is not None and cancelled():
        return []  # superseded while in flight — skip HTML parsing
    response.raise_for_status()
    return parse_results(response.text, limit=limit)


def _domain(url: str) -> str:
    """Return the bare domain of *url* for subtitles."""
    try:
        return urlparse(url).netloc or url
    except ValueError:
        return url


def open_url(url: str):
    """Open *url* in the default browser."""
    exec_shell_command_async(f"xdg-open {shlex.quote(url)}", lambda *_: None)


class SearchPlugin(LauncherPlugin):
    """Slash command: /search — web search, Enter opens a result."""

    name = "search"
    description = "Search the web (DuckDuckGo) and open a result"
    icon = "web-browser-symbolic"
    aliases: ClassVar[list[str]] = ["s", "web"]
    # Each query is a network request — debounce like /translate.
    debounce_ms = 500

    def handle(self, args: str) -> list[PluginResult]:
        query = args.strip()
        if not query:
            return [
                PluginResult(
                    "Usage: /search <query>",
                    subtitle="e.g. /search fabric hyprland",
                    icon=self.icon,
                )
            ]
        if self.is_cancelled():
            return []  # superseded before the request went out
        try:
            results = search(query, cancelled=self.is_cancelled)
        except Exception as exc:
            return [
                PluginResult(
                    "Search failed",
                    subtitle=f"{exc}",
                    icon="network-error-symbolic",
                )
            ]
        if not results:
            # No scraped results — still offer to open the search page.
            fallback_url = f"{_DDG_HTML_URL}?{urlencode({'q': query})}"
            return [
                PluginResult(
                    f"No results for '{query}'",
                    subtitle="Press Enter to open the search in your browser",
                    icon=self.icon,
                    data=fallback_url,
                )
            ]
        rows = []
        for title, url, snippet in results:
            detail = (snippet or _domain(url))[:90]
            rows.append(
                PluginResult(
                    title,
                    subtitle=f"{detail} · Enter to open & copy URL",
                    icon=self.icon,
                    data=url,
                )
            )
        return rows

    def execute(self, result: PluginResult | None = None) -> bool:
        if result is not None and result.data:
            url = str(result.data)
            open_url(url)
            copy_to_clipboard(url)
        return False  # close the launcher after opening
