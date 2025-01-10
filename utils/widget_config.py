from typing import List, TypedDict

import utils.functions as helpers
from utils.config import DEFAULT_CONFIG

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

# Bar configuration
Options = TypedDict("Options", {"screen_corners": bool, "check_updates": bool})

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
Recording = TypedDict("Recording", {"path": str, "icon_size": int, "tooltip": bool})


# OSD configuration
OSD = TypedDict("Notification", {"enabled": bool, "timeout": int, "anchor": str})


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    options: Options
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
parsed_data = helpers.read_config()

# Validate the widgets
helpers.validate_widgets(parsed_data=parsed_data, default_config=DEFAULT_CONFIG)

for key in DEFAULT_CONFIG:
    if key not in ["$schema"]:
        parsed_data[key] = helpers.merge_defaults(
            parsed_data.get(key, {}), DEFAULT_CONFIG[key]
        )

# Optionally, cast the parsed data to match our TypedDict using type hints
widget_config: BarConfig = parsed_data
