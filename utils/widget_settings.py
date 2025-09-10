from typing import Literal, TypedDict

from .types import (
    Anchor,
    Layer,
    Reveal_Animations,
    Temperature_Unit,
    Widget_Mode,
    Wind_Speed_Unit,
)

# Common configuration fields that will be reused
BaseConfig = TypedDict("BaseConfig", {"label": bool, "tooltip": bool})

# Layout configuration
Layout = TypedDict(
    "Layout", {"left": list[str], "middle": list[str], "right": list[str]}
)


# WallPaper configuration
WallPaper = TypedDict(
    "WallPaper",
    {
        "icon": str,
        "label": bool,
        "tooltip": bool,
    },
)

# Power button configuration
PowerButton = TypedDict(
    "PowerButton",
    {
        "icon": str,
        "tooltip": bool,
        "items_per_row": int,
        "icon_size": int,
        "label": bool,
        "show_icon": bool,
        "confirm": bool,
        "buttons": dict[
            dict[
                Literal["shutdown", "reboot", "hibernate", "suspend", "lock", "logout"],
                str,
            ],
            str,
        ],
    },
)

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
TaskBar = TypedDict(
    "TaskBar", {"icon_size": int, "ignored": list[str], "tooltip": bool}
)

# SystemTray configuration
SystemTray = TypedDict(
    "SystemTray",
    {
        "icon_size": int,
        "ignored": list[str],
        "hidden": list[str],
        "hide_when_empty": bool,
    },
)


# HyprIdle configuration
HyprIdle = TypedDict(
    "HyprIdle",
    {**BaseConfig.__annotations__, "enabled_icon": str, "disabled_icon": str},
)

# Window Count configuration
WindowCount = TypedDict(
    "WindowCount",
    {
        **BaseConfig.__annotations__,
        "label_format": str,
        "show_icon": bool,
        "hide_when_zero": bool,
    },
)

# Battery configuration
Battery = TypedDict(
    "Battery",
    {
        "label": bool,
        "tooltip": bool,
        "icon_size": int,
        "full_battery_level": int,
        "hide_label_when_full": bool,
        "hide_when_missing": bool,
        "notifications": dict,
    },
)

# Theme configuration
Theme = TypedDict("Theme", {"name": str})

# ClickCounter configuration
ClickCounter = TypedDict("ClickCounter", {"count": int})

# StopWatch configuration
StopWatch = TypedDict(
    "StopWatch",
    {
        "stopped_icon": str,
        "running_icon": str,
    },
)


# Notification configuration
Notification = TypedDict(
    "Notification",
    {
        "enabled": bool,
        "ignored": list[str],
        "timeout": int,
        "anchor": Anchor,
        "auto_dismiss": bool,
        "persist": bool,
        "play_sound": bool,
        "sound_file": str,
        "max_count": int,
        "dismiss_on_hover": bool,
        "dnd_on_screencast": bool,
        "max_actions": int,
        "per_app_limits": dict[str, int],
        "transition_type": Reveal_Animations,
        "transition_duration": int,
    },
)

# DesktopClock configuration
DesktopClock = TypedDict(
    "DesktopClock",
    {
        "enabled": bool,
        "anchor": Anchor,
        "layer": Layer,
        "date_format": str,
        "time_format": str,
    },
)

# Quotes configuration
Quotes = TypedDict(
    "Quotes",
    {
        "enabled": bool,
        "anchor": Anchor,
        "layer": Layer,
        "update_interval": int,
    },
)


# ScreenCorners configuration
ScreenCorners = TypedDict(
    "ScreenCorners",
    {"enabled": bool, "size": int},
)

# OSD configuration
OSD = TypedDict(
    "Osd",
    {
        "enabled": bool,
        "timeout": int,
        "anchor": Anchor,
        "percentage": bool,
        "icon_size": int,
        "play_sound": bool,
        "transition_type": Reveal_Animations,
        "transition_duration": int,
        "osds": list[Literal["brightness", "volume", "microphone"]],
    },
)


# Dock configuration
Dock = TypedDict(
    "Dock",
    {
        "enabled": bool,
        "tooltip": bool,
        "icon_size": int,
        "preview_apps": bool,
        "preview_size": tuple[int, int],
        "show_when_no_windows": bool,
        "ignored": list[str],
        "layer": Layer,
    },
)


# Dock configuration
AppLauncher = TypedDict(
    "AppLauncher",
    {"enabled": bool, "tooltip": bool, "icon_size": int},
)


Bar = TypedDict(
    "Bar",
    {
        "location": Literal["top", "bottom"],
        "layer": Layer,
        "auto_hide": bool,
    },
)


# Modules configuration
Modules = TypedDict(
    "Modules",
    {
        "dock": Dock,
        "bar": Bar,
        "quotes": Quotes,
        "osd": OSD,
        "desktop_clock": DesktopClock,
        "screen_corners": ScreenCorners,
        "notification": Notification,
        "app_launcher": AppLauncher,
    },
)


# Bar configuration
General = TypedDict(
    "General",
    {
        "check_updates": bool,
        "debug": bool,
        "monitor_styles": bool,
        "auto_reload": bool,
        "multi_monitor": bool,
    },
)

# Cpu configuration
Cpu = TypedDict(
    "Cpu",
    {
        **BaseConfig.__annotations__,
        "mode": Widget_Mode,
        "show_icon": bool,
        "sensor": str,
        "temperature_unit": Temperature_Unit,
        "show_unit": bool,
        "round": bool,
        "graph_length": int,
    },
)

# Mpris configuration
Mpris = TypedDict("Mpris", {**BaseConfig.__annotations__, "truncation_size": int})

# Memory configuration
Memory = TypedDict(
    "Memory",
    {
        **BaseConfig.__annotations__,
        "mode": Widget_Mode,
        "show_icon": bool,
        "icon": str,
        "graph_length": int,
        "unit": Literal["kb", "mb", "gb", "tb"],
    },
)


Gpu = TypedDict(
    "Gpu",
    {
        **BaseConfig.__annotations__,
        "show_icon": bool,
        "icon": str,
        "mode": Widget_Mode,
        "graph_length": int,
    },
)

# Submap configuration
Submap = TypedDict(
    "Submap",
    {
        **BaseConfig.__annotations__,
        "icon": str,
        "show_icon": bool,
        "hide_on_default": bool,
    },
)


# Network configuration
NetworkUsage = TypedDict(
    "NetworkUsage",
    {
        **BaseConfig.__annotations__,
        "upload_icon": str,
        "download_icon": str,
        "download": bool,
        "upload": bool,
        "upload_threshold": int,
        "download_threshold": int,
        "kb_digits": int,
        "mb_digits": int,
    },
)

# Storage configuration
Storage = TypedDict(
    "Storage",
    {
        "mode": Widget_Mode,
        "tooltip": bool,
        "show_icon": bool,
        "icon": str,
        "path": str,
        "graph_length": int,
        "unit": Literal["kb", "mb", "gb", "tb"],
    },
)

# Workspaces configuration
Workspaces = TypedDict(
    "Workspaces",
    {
        "count": int,
        "hide_unoccupied": bool,
        "default_label_format": str,
        "ignored": list[int],
        "icon_map": dict,
        "reverse_scroll": bool,
        "empty_scroll": bool,
    },
)

# WindowTitle configuration
WindowTitle = TypedDict(
    "WindowTitle",
    {
        "icon": bool,
        "tooltip": bool,
        "truncation": bool,
        "truncation_size": int,
        "title_map": list[dict[str, str]],
    },
)

# Updates configuration
Updates = TypedDict(
    "Updates",
    {
        **BaseConfig.__annotations__,
        "show_icon": bool,
        "available_icon": str,
        "no_updates_icon": str,
        "hover_reveal": bool,
        "reveal_duration": int,
        "os": str,
        "terminal": str,
        "auto_hide": bool,
        "interval": int,
        "pad_zero": bool,
        "tooltip": bool,
        "label": bool,
        "flatpak": bool,
        "snap": bool,
        "brew": bool,
    },
)


# Bluetooth configuration
BlueTooth = TypedDict("BlueTooth", {**BaseConfig.__annotations__, "icon_size": int})

# Weather configuration
Weather = TypedDict(
    "Weather",
    {
        **BaseConfig.__annotations__,
        "location": str,
        "interval": int,
        "expanded": bool,
        "temperature_unit": Temperature_Unit,
        "wind_speed_unit": Wind_Speed_Unit,
        "label_format": str,
        "hover_reveal": bool,
        "reveal_duration": int,
        "expanded": bool,
        "interval": int,
    },
)

App_Launcher_Button = TypedDict(
    "AppLauncher", {"tooltip": bool, "icon": str, "icon_size": int}
)

# Keyboard configuration
Keyboard = TypedDict(
    "Keyboard", {**BaseConfig.__annotations__, "icon": str, "show_icon": bool}
)

# MicroPhone configuration
MicroPhone = TypedDict("MicroPhone", {**BaseConfig.__annotations__, "show_icon": bool})

# Cava configuration
Cava = TypedDict("Cava", {"bars": int, "color": str})

# Overview configuration
Overview = TypedDict(
    "Overview", {"icon": str, **BaseConfig.__annotations__, "show_occupied": bool}
)


Cliphist = TypedDict("Cliphist", {"icon": str, **BaseConfig.__annotations__})

Kanban = TypedDict("kanban", {"icon": str, **BaseConfig.__annotations__})

EmojiPicker = TypedDict(
    "emoji_picker",
    {"icon": str, **BaseConfig.__annotations__, "per_row": int, "per_column": int},
)


# DateTime configuration
DateTimeNotification = TypedDict(
    "DateTimeNotification",
    {
        "enabled": bool,
        "hide_count_on_zero": bool,
        "count": bool,
    },
)

# DateTimeMenu configuration
DateTimeMenu = TypedDict(
    "DateTimeMenu",
    {
        "format": str,
        "notification": DateTimeNotification,
        "calendar": bool,
        "hover_reveal": bool,
        "auto_hide": bool,
        "auto_hide_timeout": int,
        "transition_type": str,
        "transition_duration": int,
        "hover_reveal": bool,
        "reveal_duration": int,
    },
)

# TODO: custom_button_group

# World clock configuration
WorldClock = TypedDict(
    "WorldClock",
    {
        "icon": str,
        "show_icon": bool,
        "timezones": list[str],
        "use_24hr": bool,
    },
)

# ThemeSwitcher configuration
ThemeSwitcher = TypedDict("ThemeSwitcher", {**BaseConfig.__annotations__, "icon": str})

# Hyprpicker configuration
HyprPicker = TypedDict(
    "HyprPicker",
    {**BaseConfig.__annotations__, "icon": str, "show_icon": bool, "quiet": bool},
)

# OCR configuration
OCR = TypedDict(
    "OCR", {**BaseConfig.__annotations__, "icon": str, "quiet": bool, "show_icon": bool}
)


# Media configuration
Media = TypedDict(
    "Media",
    {
        "ignore": list[str],
        "truncation_size": int,
        "truncation_size": int,
        "show_album": bool,
        "show_artist": bool,
        "show_time": bool,
        "show_time_tooltip": bool,
    },
)

# User configuration for QuickSettings
UserConfig = TypedDict(
    "UserConfig",
    {
        "image": str,
        "name": str,
        "distro_icon": bool,
    },
)


ShortcutsConfig = TypedDict(
    "Shortcuts", {"enabled": bool, "items": list[dict[str, str]]}
)

ControlsConfig = TypedDict(
    "Controls",
    {
        "sliders": list[Literal["brightness", "volume", "microphone"]],
    },
)

# QuickSettings configuration
QuickSettings = TypedDict(
    "QuickSettings",
    {
        "media": Media,
        "hover_reveal": bool,
        "auto_hide": bool,
        "auto_hide_timeout": int,
        "shortcuts": ShortcutsConfig,
        "user": UserConfig,
        "controls": ControlsConfig,
    },
)

# Spacing configuration
Spacing = TypedDict("Spacing", {"size": int})

# Divider configuration
Divider = TypedDict("Divider", {"size": int})

# Language configuration
Language = TypedDict(
    "Language", {**BaseConfig.__annotations__, "icon": str, "truncation_size": int}
)

# Volume configuration
Volume = TypedDict("Volume", {**BaseConfig.__annotations__, "step_size": int})

# Brightness configuration
Brightness = TypedDict("Brightness", {**BaseConfig.__annotations__, "step_size": int})


# Recording configuration
Recording = TypedDict(
    "Recording",
    {
        "path": str,
        "delayed": bool,
        "delayed_timeout": int,
        "tooltip": bool,
        "audio": bool,
    },
)

# ScreenShot configuration
ScreenShot = TypedDict(
    "ScreenShot",
    {
        "path": str,
        "tooltip": bool,
        "icon_size": int,
        "label": bool,
        "icon": str,
        "annotation": bool,
        "capture_sound": bool,
        "delayed": bool,
        "delayed_timeout": int,
    },
)


class Widgets(TypedDict):
    """Configuration for all widgets in the bar"""

    battery: Battery
    bluetooth: BlueTooth
    brightness: Brightness
    cava: Cava
    click_counter: ClickCounter
    cpu: Cpu
    emoji_picker: EmojiPicker
    kanban: Kanban
    date_time: DateTimeMenu
    divider: Divider
    hypridle: HyprIdle
    hyprsunset: HyprSunset
    hyprpicker: HyprPicker
    app_launcher_button: App_Launcher_Button
    keyboard: Keyboard
    language: Language
    gpu: Gpu
    memory: Memory
    microphone: MicroPhone
    mpris: Mpris
    network_usage: NetworkUsage
    ocr: OCR
    overview: Overview
    wallpaper: WallPaper
    power: PowerButton
    quick_settings: QuickSettings
    recorder: Recording
    screenshot: ScreenShot
    spacing: Spacing
    stopwatch: StopWatch
    storage: Storage
    system_tray: SystemTray
    submap: Submap
    taskbar: TaskBar
    theme: Theme
    theme_switcher: ThemeSwitcher
    updates: Updates
    volume: Volume
    weather: Weather
    window_title: WindowTitle
    window_count: WindowCount
    workspaces: Workspaces
    world_clock: WorldClock
    cliphist: Cliphist


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    widgets: Widgets
    layout: Layout
    modules: Modules
    general: General
