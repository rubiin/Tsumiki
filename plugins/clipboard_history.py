"""Launcher slash command: /clipboard-history — search clipboard history."""

import subprocess
from typing import ClassVar

from utils.functions import find_executable
from utils.plugin_manager import LauncherPlugin, PluginResult, copy_to_clipboard

_MAX_RESULTS = 20
_TIMEOUT_SECONDS = 5
# Null bytes or UTF-8 replacement chars in a listing usually mean binary
# content (images) — show a marker instead of garbled text.
_BINARY_MARKERS = ("\x00", "\ufffd")


def parse_list(output: str) -> list[tuple[str, str]]:
    """Return [(item_id, content)] from ``cliphist list`` output."""
    items = []
    for line in output.strip().splitlines():
        if not line or "<meta http-equiv" in line:
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            items.append((parts[0], parts[1].strip()))
    return items


def is_binary(content: str) -> bool:
    """Heuristic: True for image/binary clipboard items."""
    return any(marker in content for marker in _BINARY_MARKERS)


class ClipboardHistoryPlugin(LauncherPlugin):
    """Slash command: /clipboard-history — search and re-copy history items."""

    name = "clipboard-history"
    description = "Search clipboard history (cliphist)"
    icon = "edit-paste-symbolic"
    aliases: ClassVar[list[str]] = ["clip", "cb", "history"]

    def handle(self, args: str) -> list[PluginResult]:
        query = args.strip().casefold()

        if find_executable("cliphist") is None:
            return [
                PluginResult(
                    "/clipboard-history requires cliphist",
                    subtitle="Install cliphist, e.g. sudo pacman -S cliphist",
                    icon="dialog-error-symbolic",
                )
            ]

        try:
            result = subprocess.run(
                ["cliphist", "list"],
                capture_output=True,
                text=True,
                timeout=_TIMEOUT_SECONDS,
            )
            lines = result.stdout
        except Exception as exc:
            return [
                PluginResult(
                    "Failed to read clipboard history",
                    subtitle=f"{exc}",
                    icon="network-error-symbolic",
                )
            ]
        if result.returncode != 0:
            return [
                PluginResult(
                    "Failed to read clipboard history",
                    subtitle=result.stderr.strip()
                    or f"cliphist failed (exit {result.returncode})",
                    icon="network-error-symbolic",
                )
            ]

        items = [
            (item_id, content)
            for item_id, content in parse_list(lines)
            if not query or query in content.casefold()
        ]
        if not items:
            return [
                PluginResult(
                    "No matching clipboard items",
                    subtitle="Copy something first, or try another query",
                    icon="dialog-info-symbolic",
                )
            ]

        rows = []
        for item_id, content in items[:_MAX_RESULTS]:
            preview = content.replace("\n", " ").strip()
            if is_binary(content):
                preview = "[Image or binary]"
            elif len(preview) > 80:
                preview = preview[:77] + "..."
            rows.append(
                PluginResult(
                    preview,
                    subtitle="Press Enter to copy",
                    icon=self.icon,
                    data=item_id,
                )
            )
        return rows

    def execute(self, result: PluginResult | None = None) -> bool:
        if result is not None and result.data:
            self._recopy(str(result.data))
        return False  # close the launcher after copying

    @staticmethod
    def _recopy(item_id: str):
        """Decode a history item and copy it back to the clipboard."""
        try:
            decoded = subprocess.run(
                ["cliphist", "decode", item_id],
                capture_output=True,
                timeout=_TIMEOUT_SECONDS,
            )
        except Exception:
            return
        if decoded.returncode != 0 or not decoded.stdout:
            return
        if b"\x00" in decoded.stdout:
            # Binary content (images) can't be copied as text — skip it.
            return
        copy_to_clipboard(decoded.stdout.decode("utf-8", errors="replace"))
