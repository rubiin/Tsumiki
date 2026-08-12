"""Launcher slash command: /translate — translate text.

Uses Google's public (keyless) translate endpoint through the shared httpx
client. ``handle`` runs on a worker thread, so typing stays responsive while
the request is in flight.

Examples:
    /translate bonjour
    /translate こんにちは
"""

from typing import ClassVar

from utils.functions import get_http_client
from utils.plugin_manager import LauncherPlugin, PluginResult, copy_to_clipboard

_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


class TranslatePlugin(LauncherPlugin):
    """Slash command: /translate — translate text and copy the result."""

    name = "translate"
    description = "Translate text (auto-detect source language)"
    icon = "preferences-desktop-locale-symbolic"
    aliases: ClassVar[list[str]] = ["tr", "t"]
    # Each query is a network request, so wait for the user to pause typing
    # before translating instead of hitting the API on every keystroke.
    debounce_ms = 400
    #: Target language code — change by editing this file.
    target_lang = "en"

    def _fetch(self, text: str) -> str:
        response = get_http_client().get(
            _TRANSLATE_URL,
            params={
                "client": "gtx",
                "sl": "auto",
                "tl": self.target_lang,
                "dt": "t",
                "q": text,
            },
        )
        response.raise_for_status()
        payload = response.json()
        segments = payload[0] if isinstance(payload, list) and payload else []
        return "".join(
            part[0] for part in segments if isinstance(part, list) and part and part[0]
        ).strip()

    def handle(self, args: str) -> list[PluginResult]:
        text = args.strip()
        if not text:
            return [
                PluginResult(
                    "Usage: /translate <text>",
                    subtitle=(
                        "e.g. /translate bonjour  (source language is auto-detected)"
                    ),
                    icon=self.icon,
                )
            ]
        try:
            translation = self._fetch(text)
        except Exception as exc:
            return [
                PluginResult(
                    "Translation failed",
                    subtitle=f"{exc}",
                    icon="network-error-symbolic",
                )
            ]
        if not translation:
            return [
                PluginResult(
                    "No translation returned",
                    icon="dialog-warning-symbolic",
                )
            ]
        return [
            PluginResult(
                translation,
                subtitle="Press Enter to copy the translation",
                icon=self.icon,
                data=translation,
            )
        ]

    def execute(self, result: PluginResult | None = None) -> bool:
        if result is not None and result.data:
            copy_to_clipboard(str(result.data))
        return False  # close the launcher after copying
