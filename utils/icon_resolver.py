import json
import os
import re

import gi
from gi.repository import GdkPixbuf, GLib, Gtk
from loguru import logger

from utils.thread import run_in_thread

from .colors import Colors
from .constants import ICON_CACHE_FILE
from .icons import symbolic_icons

gi.require_versions({"Gtk": "3.0"})


class IconResolver:
    """A class to resolve icons for applications."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if os.path.exists(ICON_CACHE_FILE):
            with open(ICON_CACHE_FILE, "r") as file:
                try:
                    self._icon_dict = json.load(file)
                except json.JSONDecodeError:
                    logger.info(
                        f"{Colors.INFO}[ICONS] Cache file does not exist or corrupted."
                    )
        else:
            self._icon_dict = {}

    def get_icon_name(self, app_id: str):
        if app_id in self._icon_dict:
            return self._icon_dict[app_id]
        new_icon = self._compositor_find_icon(app_id)
        logger.info(
            f"[ICONS] found new icon: '{new_icon}' for app id: '{app_id}', storing."
        )
        self._store_new_icon(app_id, new_icon)
        return new_icon

    def resolve_icon(self, pixmap, icon_name: str, app_id: str, icon_size: int = 16):
        try:
            return (
                pixmap.as_pixbuf(icon_size, GdkPixbuf.InterpType.HYPER)
                if pixmap is not None
                else Gtk.IconTheme()
                .get_default()
                .load_icon(
                    icon_name,
                    icon_size,
                    Gtk.IconLookupFlags.FORCE_SIZE,
                )
            )
        except GLib.GError:
            return self.get_icon_pixbuf(app_id, icon_size)

    def get_icon_pixbuf(self, app_id: str, size: int = 16):
        icon_name = self.get_icon_name(app_id)
        try:
            return Gtk.IconTheme.get_default().load_icon(
                icon_name,
                size,
                Gtk.IconLookupFlags.FORCE_SIZE,
            )
        except GLib.GError:
            return (
                Gtk.IconTheme()
                .get_default()
                .load_icon(
                    "image-missing",
                    size,
                    Gtk.IconLookupFlags.FORCE_SIZE,
                )
            )

    @run_in_thread
    def _store_new_icon(self, app_id: str, icon: str):
        self._icon_dict[app_id] = icon
        with open(ICON_CACHE_FILE, "w") as f:
            json.dump(self._icon_dict, f, indent=4, ensure_ascii=False)
            f.close()

    def _get_icon_from_desktop_file(self, desktop_file_path: str):
        with open(desktop_file_path, "r") as f:
            for line in f.readlines():
                if "Icon=" in line:
                    return "".join(line[5:].split())
            return symbolic_icons["fallback"]["executable"]

    def _get_desktop_file(self, app_id: str) -> str | None:
        data_dirs = GLib.get_system_data_dirs()
        for data_dir in data_dirs:
            data_dir = data_dir + "/applications/"
            if os.path.exists(data_dir):
                # Do name resolving here
                files = os.listdir(data_dir)
                matching = [
                    s for s in files if "".join(app_id.lower().split()) in s.lower()
                ]
                if matching:
                    return data_dir + matching[0]

                for word in list(filter(None, re.split(r"-|\.|_|\s", app_id))):
                    matching = [s for s in files if word.lower() in s.lower()]
                    if matching:
                        return data_dir + matching[0]

        return None

    def _compositor_find_icon(self, app_id: str):
        if Gtk.IconTheme.get_default().has_icon(app_id):
            return app_id
        if Gtk.IconTheme.get_default().has_icon(app_id + "-desktop"):
            return app_id + "-desktop"
        desktop_file = self._get_desktop_file(app_id)
        return (
            self._get_icon_from_desktop_file(desktop_file)
            if desktop_file
            else symbolic_icons["fallback"]["executable"]
        )
