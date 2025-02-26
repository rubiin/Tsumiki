Welcome to the HyDePanel wiki!

# System Configuration

This repository defines the configuration settings for a modular system, allowing users to customize the layout, icons, intervals, and various components. The configuration is written in Python and structured using typed dictionaries for strong typing.

## Default Configuration

The default configuration is stored in the `DEFAULT_CONFIG` dictionary. It includes default values for various sections, such as the layout of the bar, settings for battery, CPU, weather, and other system components.

## Layout Configuration

The layout configuration defines the sections of the bar and the components displayed in each section:

```json
"layout": {
    "left_section": ["workspaces", "window_title"],
    "middle_section": ["date_time"],
    "right_section": [
        "weather",
        "updates",
        "battery",
        "bluetooth",
        "system_tray",
        "power",
    ],
}
```

- left_section: Displays workspace and window title.
- middle_section: Displays datetime.
- right_section: Displays weather, updates, battery, bluetooth, system tray, and power.

# Component Configurations

Each component, such as hypr_sunset, battery, cpu, memory, etc., has its own configuration with customizable options. Here's an example for the battery component:

```json
"hypr_sunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "icon_size": "12px",
    "interval": 2000,
    "label": true,
    "tooltip": true
}
```

Other components follow a similar structure, where each configuration defines things like icon_size, label, and tooltip.

## Battery

```json
"battery": {
    "label": true,
    "tooltip": true,
    "hide_label_when_full": true,
    "full_battery_level": 100,
}
```

- hide_label_when_full: Hide battery level when battery is full.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.
- full_battery_level: The battery level at which the battery is considered full.

## Bluetooth

```json
"bluetooth": {
    "icon_size": 22,
    "label": true,
    "tooltip": true,
}
```

- icon_size: Size of the icon in number.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Brightness

```json
"brightness": {
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
    "icon": "󰏨",
    "step_size": 5,
}
```

- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip
- icon: The icon used to display the module.
- step_size: The brightness step size.

## CPU

```json
"cpu": {
    "icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.

## HyprIdle

```json
"hypr_idle": {
    "enabled_icon": "",
    "disabled_icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- enabled_icon: The icon used when enabled.
- disabled_icon: The icon used when disabled.
- icon_size: Size of the icon.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.

## HyprSunset

```json
"hypr_sunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- temperature: Sets the color temperature.
- enabled_icon: The icon used when enabled.
- disabled_icon: The icon used when disabled.
- icon_size: Size of the icon.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.

## Language

```json
"language": {"length": 3}

```

- length - Sets the length of the language display.

## Memory

```json
"memory": {
    "icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## MPRIS

```json
"mpris": {
    "truncation_size": 30,
    "format": "{artist} - {title}",
}
```

Configures the media player information system (MPRIS) display settings.

- truncation_size: The length of the MPRIS display.
- format: The format of the MPRIS display.

## Power Button

```json
"power": {"icon": "󰐥", "icon_size": "12px", "tooltip": true}

```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- tooltip: Whether to show a tooltip

## Recorder

```json
"recorder": {
    "videos": "Videos/Screencasting",
    "tooltip": true,
    "audio": true,
    "icon_size": 14
}

```

- videos: Path to the videos directory.
- audio: Whether to record video with audio.
- tooltip: Whether to show a tooltip
- icon_size: Size of the icon in number

## Submap

```json
"submap": {
    "icon": "󰋊",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Storage

```json
"storage": {
    "icon": "󰋊",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## TaskBar and System Tray

```json
"task_bar": {"icon_size": 22, "ignored": ["firefox"]},
"system_tray": {"icon_size": 22, "ignored": ["firefox"]},
```

- icon_size - the size of the icon in number
- ignored - list of applications to ignore

## Updates

```json
"updates": {
    "os": "arch",
    "icon": "󱧘",
    "icon_size": "14px",
    "interval": 60000,
    "tooltip": true,
    "label": true,
}
```

- os: The os to fetch updates count for.
- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- interval: The update interval for update.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Volume

```json
"volume": {
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
    "step_size": 5,
}
```

- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip
- step_size: The volume step size.

## Weather

```json
"weather": {
    "location": "Kathmandu",
    "interval": 60000,
    "tooltip": true,
    "label": true,
    "detect_location": false,
}
```

- location: The location to display weather for.
- interval: The update interval for weather.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip
- detect_location: Whether to detect the location automatically.

## Window Title

```json
"window_title": {
    "truncation": true,
    "truncation_size": 50,
    "enable_icon": true,
    "title_map": []
    }

```

- truncation: whether to limit the window title.
- truncation_size: Maximum length for the window title (requires truncation set to true).
- enable_icon: Whether to display the icon in the title bar.
- title_map: Map of window title to icon.

## Workspaces

```json
"workspaces": {
  "count": 8,
  "hide_unoccupied": true,
    "reverse_scroll": false,
    "empty_scroll": false,
    "icon_map": {
      "1":"",
      "2": "",
      "3": "",
      "4": "󰏆",
      "5": "",
      "6": "󰕼",
      "7": "󰏦",
      "8": "󰏧"
    },
    "ignored": [1]
    }
```

- count: Number of workspaces.
- hide_unoccupied: Indicates whether workspaces should show as occupied or not.
- reverse_scroll: Invert scroll direction
- empty_scroll: scroll to empty workspaces
- icon_map: map an icon to a workspace instead of number
- ignored: ignores workspaces from the widget
