import json
from typing import Iterator

from fabric.hyprland.widgets import get_hyprland_connection
from loguru import logger

MODMASK_MAP = {
    64: "SUPER",
    8: "ALT",
    4: "CTRL",
    1: "SHIFT",
}


def modmask_to_key(modmask: int) -> str:
    keys = [key for bf, key in MODMASK_MAP.items() if (modmask & bf) == bf]
    known_bits = sum(bf for bf in MODMASK_MAP)
    unknown_bits = modmask & (~known_bits)
    if unknown_bits != 0:
        keys.append(f"({unknown_bits})")
    return " + ".join(keys)


class KeybindLoader:
    """Loads and filters keybinds from Hyprland."""

    def __init__(self):
        self.keybinds = []
        self._hyprland_connection = get_hyprland_connection()

    def load_keybinds(self):
        try:
            output = self._hyprland_connection.send_command("j/binds").reply.decode()
            binds = json.loads(output)
        except Exception as e:
            logger.exception(f"ERROR: Failed to load keybinds from hyprctl: {e}")
            self.keybinds = []
            return

        self.keybinds.clear()
        for bind in binds:
            mod_keys = modmask_to_key(bind["modmask"])
            if mod_keys:
                key_combo = f"{mod_keys} + {bind['key']}:"
            else:
                key_combo = f"{bind['key']}:"
            description = bind.get("description", "").strip()
            dispatcher = bind.get("dispatcher", "").strip()
            arg = bind.get("arg", "").strip()
            cmd = f"{dispatcher}: {arg}".strip(": ")
            self.keybinds.append(
                {"combo": key_combo.strip(), "description": description, "cmd": cmd}
            )

    def filter_keybinds(self, query: str = "") -> Iterator[tuple]:
        query_cf = query.casefold()
        return (kb for kb in self.keybinds if query_cf in " ".join(kb).casefold())
