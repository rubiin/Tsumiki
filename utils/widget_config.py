from typing import List, TypedDict

from utils.config import HIGH_POLL_INTERVAL
from utils.functions import read_config

# Default configuration values
DEFAULT_CONFIG = {
    "theme": {
        "name": "catpuccin-mocha",
    },
    "layout": {
        "left_section": ["workspaces", "window_title"],
        "middle_section": ["date_time"],
        "right_section": [
            "updates",
            "battery",
            "bluetooth",
            "system_tray",
            "power",
        ],
    },
    "hypr_sunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "interval": 2000,
        "label": True,
        "tooltip": True,
    },
    "hypr_idle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "interval": 2000,
        "label": True,
        "tooltip": True,
    },
    "battery": {
        "label": True,
        "tooltip": True,
        "hide_label_when_full": True,
    },
    "date_time": {
        "format": "%b %d %H:%M",
    },
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "memory": {
        "icon": "",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "storage": {
        "icon": "󰋊",
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
    },
    "workspaces": {
        "count": 8,
        "hide_unoccupied": True,
        "ignored": [],
        "reverse_scroll": False,
        "empty_scroll": False,
        "icon_map": {},
    },
    "window_title": {
        "enable_icon": True,
        "truncation": True,
        "truncation_size": 50,
        "title_map": [],
    },
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "icon_size": "14px",
        "interval": HIGH_POLL_INTERVAL,
        "tooltip": True,
        "label": True,
    },
    "keyboard": {
        "icon": "󰌌",
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
    },
    "bluetooth": {
        "icon_size": 14,
        "label": True,
        "tooltip": True,
    },
    "weather": {
        "detect_location": True,
        "location": "kathmandu",
        "label": True,
        "tooltip": True,
        "interval": HIGH_POLL_INTERVAL,
    },
    "volume": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "brightness": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "mpris": {
        "length": 30,
        "tooltip": True,
    },
    "language": {"length": 3},
    "task_bar": {"icon_size": 22},
    "system_tray": {"icon_size": 20, "ignore": []},
    "power": {"icon": "󰐥", "icon_size": "18px", "tooltip": True},
    "theme_switcher": {
        "icon": "",
        "icon_size": "14px",
        "silent": True,  # Whether to show a notification when the theme is changed
    },
    "notification": {
        "ignored": ["t2"],
        "timeout": 5000,
        "anchor": "top right",
    },
    "osd": {
        "enabled": True,
        "timeout": 1500,
        "anchor": "bottom center",
    },
    "recorder": {
        "photos": "Pictures/Screenshots",
        "videos": "Videos/Screencasting",
        "icon_size": 16,
        "tooltip": True,
    },
}


# Common configuration fields that will be reused
BaseConfig = TypedDict(
    "BaseConfig", {"icon_size": str, "label": bool, "tooltip": bool, "interval": int}
)

# Layout configuration
Layout = TypedDict(
    "Layout", {"left": List[str], "middle": List[str], "right": List[str]}
)

# Power button configuration
PowerButton = TypedDict("PowerButton", {"icon": str, "icon_size": int, "tooltip": bool})

# HyprSunset configuration
HyprSunset = TypedDict(
    "HyprSunset",
    {
        **BaseConfig.__annotations__,
        "temperature": str,
        "enabled_icon": str,
        "disabled_icon": str,
    },
)

# TaskBar configuration
TaskBar = TypedDict("TaskBar", {"icon_size": int})

# SystemTray configuration
SystemTray = TypedDict("SystemTray", {"icon_size": int, "ignore": List[str]})

# HyprIdle configuration
HyprIdle = TypedDict(
    "HyprIdle",
    {**BaseConfig.__annotations__, "enabled_icon": str, "disabled_icon": str},
)

# Battery configuration
Battery = TypedDict(
    "Battery",
    {
        "label": bool,
        "tooltip": bool,
        "hide_label_when_full": bool,
    },
)

# Theme configuration
Theme = TypedDict("Theme", {"name": str})

# Cpu configuration
Cpu = TypedDict("Cpu", {**BaseConfig.__annotations__, "icon": str})

# Mpris configuration
Mpris = TypedDict("Mpris", {**BaseConfig.__annotations__, "length": int})

# Memory configuration
Memory = TypedDict("Memory", {**BaseConfig.__annotations__, "icon": str})

# Storage configuration
Storage = TypedDict("Storage", {**BaseConfig.__annotations__, "icon": str})

# Workspaces configuration
Workspaces = TypedDict(
    "Workspaces",
    {"count": int, "occupied": bool, "ignored": List[int], "icon_map": dict},
)

# WindowTitle configuration
WindowTitle = TypedDict(
    "WindowTitle",
    {
        "length": int,
        "enable_icon": bool,
        "truncation": bool,
        "truncation_size": int,
        "title_map": any,
    },
)

# Updates configuration
Updates = TypedDict("Updates", {**BaseConfig.__annotations__, "os": str, "icon": str})

# Bluetooth configuration
BlueTooth = TypedDict("BlueTooth", {"label": bool, "tooltip": bool, "icon_size": int})

# Weather configuration
Weather = TypedDict(
    "Weather",
    {
        "detect_location": bool,
        "location": str,
        "interval": int,
        "tooltip": bool,
        "label": bool,
    },
)

# Keyboard configuration
Keyboard = TypedDict("Keyboard", {**BaseConfig.__annotations__, "icon": str})

# DateTimeMenu configuration
DateTimeMenu = TypedDict("DateTimeMenu", {"format": str})

# ThemeSwitcher configuration
ThemeSwitcher = TypedDict("ThemeSwitcher", {**BaseConfig.__annotations__, "icon": str})

# Language configuration
Language = TypedDict("Language", {"length": int})

# Volume configuration
Volume = TypedDict("Volume", {**BaseConfig.__annotations__, "step_size": int})

# Brightness configuration
Brightness = TypedDict("Brightness", {**BaseConfig.__annotations__, "step_size": int})


# Notification configuration
Notification = TypedDict(
    "Notification", {"ignored": List[str], "timeout": int, "anchor": str}
)

# Recording configuration
Recording = TypedDict(
    "Recording", {"videos": str, "photos": str, "icon_size": int, "tooltip": bool}
)


# OSD configuration
OSD = TypedDict("Notification", {"enabled": bool, "timeout": int, "anchor": str})


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    notification: Notification
    bluetooth: BlueTooth
    cpu: Cpu
    recorder: Recording
    hypr_sunset: HyprSunset
    hypr_idle: HyprIdle
    keyboard: Keyboard
    language: Language
    theme: Theme
    theme_switcher: ThemeSwitcher
    layout: Layout
    memory: Memory
    date_time: DateTimeMenu
    mpris: Mpris
    storage: Storage
    system_tray: SystemTray
    task_bar: TaskBar
    updates: Updates
    power: PowerButton
    volume: Volume
    brightness: Brightness
    workspaces: Workspaces
    window_title: WindowTitle
    weather: Weather
    osd: OSD


# Read the configuration from the JSON file
parsed_data = read_config()


# Merge the parsed data with the default configuration
def merge_defaults(data: dict, defaults: dict):
    return {**defaults, **data}


# Now, `parsed_data` is a Python dictionary
# You can access individual items like this:
layout = parsed_data["layout"]


for key, value in parsed_data.items():
    if key in DEFAULT_CONFIG:
        parsed_data[key] = merge_defaults(value, DEFAULT_CONFIG[key])


## TODO: validate the name of widget is within the dict

# Optionally, cast the parsed data to match our TypedDict using type hints
widget_config: BarConfig = parsed_data
