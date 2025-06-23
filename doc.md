Welcome to the HyDePanel wiki!

# System Configuration

This repository defines the configuration settings for a modular system, allowing users to customize the layout, icons, intervals, and various components. The configuration is written in Python and structured using typed dictionaries for strong typing.

## Default Configuration

The default configuration is stored in the `DEFAULT_CONFIG` dictionary. It includes default values for various sections, such as the layout of the bar, settings for battery, CPU, weather, and other system components.
By default, `config.json` is read. If the config is not found, then `config.toml` is read. For sample configuration, please see `example` folder.

# General Configuration

```json
    "general": {
        "screen_corners": {
            "enabled": false,
            "size": 20,
        },
        "desktop_clock": {
            "enabled": false,
            "anchor": "center",
            "date_format": "%A, %d %B %Y",
        },
        "check_updates": false,
        "debug": false,
        "layer": "top",
        "auto_hide": false,
        "location": "top",
        "widget_style": "default",
    }

```

- **debug** (boolean):
  Enable or disable debug mode for the panel. When set to true, additional debugging output or features may be activated.

- **location** (string; enum: "top", "bottom"):
  Determines where the panel is positioned on the screen. It can either be at the top or the bottom.

- **layer** (string; enum: "background", "bottom", "top", "overlay"):
  Specifies the stacking order or z-index of the panel, determining which layer it should be rendered on.

- **widget_style** (string; enum: "default", "wave1", "wave2", "flat", "shadow"):
  Sets a visual style for the widgets on the panel. Each option represents a predefined look.

- **screen_corners.enabled** (boolean):
  Determines whether the screen corner feature is enabled or disabled.

- **screen_corners.size** (integer):
  Defines the size of the screen corner feature when enabled.

- **desktop_clock.enabled** (boolean):
  Enables or disables the desktop clock.

- **desktop_clock.anchor** (string; enum: "left", "center", "right"):
  Sets the anchor position of the desktop clock on the screen.

- **desktop_clock.date_format** (string):
  Specifies the format of the date displayed on the desktop clock. Example: `%A, %d %B %Y`.

- **check_updates** (boolean):
  Determines whether the system should automatically check for updates on bar launch.

- **auto_hide** (boolean):
  Defines whether the panel should automatically hide when not in use.

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

- **layout.left_section** (array of strings):
  Specifies the elements to be displayed in the left section of the panel. The order in the array determines the sequence.

  - `"workspaces"`: Displays workspace-related information.
  - `"window_title"`: Shows the title of the currently focused window.

- **layout.middle_section** (array of strings):
  Specifies the elements to be displayed in the middle section of the panel. The order in the array determines the sequence.

  - `"date_time"`: Displays the current date and time.

- **layout.right_section** (array of strings):
  Specifies the elements to be displayed in the right section of the panel. The order in the array determines the sequence.

# Component Configurations

Each component, such as hyprsunset, battery, cpu, memory, etc., has its own configuration with customizable options. Here's an example for the battery component:

```json
"hyprsunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "interval": 2000,
    "label": true,
    "tooltip": true
}
```

Other components follow a similar structure, where each configuration defines things like label, and tooltip.

## Battery

```json
"battery": {
    "label": true,
    "tooltip": true,
    "hide_label_when_full": true,
    "full_battery_level": 100,
    "icon_size": 22,
}
```

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

- **hide_label_when_full** (boolean):
  Specifies whether the label should be hidden when the relevant item is at full capacity or status. When set to true, the label will be hidden if the item is full.

- **full_battery_level** (integer):
  Defines the battery level percentage at which the system is considered to be fully charged. The default is 100.


## Bluetooth

```json
"bluetooth": {
    "icon_size": 22,
    "label": true,
    "tooltip": true,
}
```

- **icon_size** (integer):
  Specifies the size of the icons. The value is in pixels, and in this case, the icon size is set to 22 pixels.

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

## Brightness

```json
"brightness": {
    "label": true,
    "tooltip": true,
    "icon": "󰏨",
    "step_size": 5,
}
```

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

- **icon** (string):
  Defines the icon to be displayed. In this case, the icon is represented by the Unicode character `"󰏨"`.

- **step_size** (integer):
  Specifies the step size for any actions that involve incrementing or changing values. In this case, the step size is set to `5`.

## cava

```json
"cava": {
    "bars": 10,
    "color": "#89b4fa"
}
```

- **bars** (integer):
  Specifies the number of bars to be displayed. In this case, the number of bars is set to `10`.

- **color** (string):
  Defines the color to be used. The color is represented in hexadecimal format, and in this case, the color is `"#89b4fa"`.

## CPU

```json
"cpu": {
    "icon": "",
		"mode": "label",
    "tooltip": true,
    "show_icon": true,
}
```

- icon: The icon used to display the module.
- mode: The mode of the CPU display. It can be "label","progress" or "graph".
- tooltip: Whether to show a tooltip.
- round: Whether to round the temperature.
- unit: The unit of the temperature.
- show_unit: Whether to show the unit.
- sensor: The sensor to use for temperature.
- show_icon: Whether to show the icon.

## HyprIdle

```json
"hypridle": {
    "enabled_icon": "",
    "disabled_icon": "",
    "label": true,
    "tooltip": true,
}
```

- **enabled_icon** (string):
  Specifies the icon to be displayed when the element is enabled. In this case, the enabled icon is represented by `""`.

- **disabled_icon** (string):
  Specifies the icon to be displayed when the element is disabled. In this case, the disabled icon is represented by `""`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

## HyprSunset

```json
"hyprsunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "label": true,
    "tooltip": true,
}
```

- **temperature** (string):
  Specifies the color temperature. In this case, the temperature is set to `"2800k"`.

- **enabled_icon** (string):
  Specifies the icon to be displayed when the element is enabled. In this case, the enabled icon is represented by `"󱩌"`.

- **disabled_icon** (string):
  Specifies the icon to be displayed when the element is disabled. In this case, the disabled icon is represented by `"󰛨"`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

## Hyprpicker

```json
"hyprpicker": {
    "icon": "",
    "label": true,
    "tooltip": true,
    "show_icon": true,
}
```

- **icon** (string):
  Specifies the icon to be displayed. In this case, the icon is represented by `""`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

- **show_icon** (boolean):
  Specifies whether the icon should be displayed. In this case, the value is `true`, meaning the icon will be shown.

## Language

```json
"language": {"length": 3}

```

- length - Sets the length of the language display.

## Memory

```json
"memory": {
    "icon": "",
    "mode": "label",
    "tooltip": true,
    "show_icon": true,
}
```

- **icon** (string):
  Specifies the icon to be displayed. In this case, the icon is represented by `""`.

- **label** (string):
  The mode of the CPU display. It can be "label","progress" or "graph".

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

- **show_icon** (boolean):
  Specifies whether the icon should be displayed. In this case, the value is `true`, meaning the icon will be shown.

## MPRIS

```json
"mpris": {
    "truncation_size": 30,
    "format": "{artist} - {title}",
}
```

- **truncation_size** (integer):
  Specifies the length of the MPRIS display. In this case, it is set to 30.

- **format** (string):
  Defines the format of the MPRIS display. In this case, it is set to "{artist} - {title}".

## OCR

```json
"ocr": {
"icon": "󰐳",
"label": true,
"tooltip": true,
}

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰐳".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

## Power Button

```json
"power": {"icon": "󰐥","tooltip": true,
        "items_per_row": 3,
        "icon_size": 100,
        "show_icon": true,
        "label": true,
        "buttons": {
            "shutdown": "systemctl poweroff",
            "reboot": "systemctl reboot",
            "hibernate": "systemctl hibernate",
            "suspend": "systemctl suspend",
            "lock": "loginctl lock-session",
            "logout": "loginctl terminate-user $USER",
        }, }

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰐥".

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **buttons** (object):
  A dictionary of buttons and their corresponding commands. In this case, the buttons are defined as follows:
  - **shutdown**: Executes the command "systemctl poweroff".
  - **reboot**: Executes the command "systemctl reboot".
  - **hibernate**: Executes the command "systemctl hibernate".
  - **suspend**: Executes the command "systemctl suspend".
  - **lock**: Executes the command "loginctl lock-session".
  - **logout**: Executes the command "loginctl terminate-user $USER".

- **items_per_row** (integer):
  The number of items to display per row. In this case, it is set to 3.

- **icon_size** (integer):
  The size of the icon in number. In this case, it is set to 100.
- **show_icon** (boolean):
  Whether to show the icon. In this case, it is set to true.
- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

## Recorder

```json
"recorder": {
"videos": "Videos/Screencasting",
"tooltip": true,
"audio": true,
"icon_size": 14
}

```

- **videos** (string):
  The path to the videos directory. In this case, it is set to "Videos/Screencasting".

- **audio** (boolean):
  Whether to record video with audio. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **icon_size** (integer):
  The size of the icon in number. In this case, it is set to 14.

## Submap

```json
"submap": {
"icon": "󰋊",
"label": true,
"tooltip": true,
"show_icon": true,
}

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰋊".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **show_icon** (boolean):
  Whether to show the icon. In this case, it is set to true.

## Storage

```json
"storage": {
"icon": "󰋊",
"mode": "label",
"tooltip": true,
"show_icon": true,
}
```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰋊".

- **mode** (string):
  The mode of the CPU display. It can be "label","progress" or "graph".

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.


- **show_icon** (boolean):
  Whether to show the icon. In this case, it is set to true.

## TaskBar and System Tray

```json
"taskbar": {"icon_size": 22, "ignored": ["firefox"]},
"system_tray": {"icon_size": 22, "ignored": ["firefox"]},
```

- **icon_size** (integer):
  The size of the icon in number. In this case, it is set to 22.

- **ignored** (array):
  List of applications to ignore. In this case, it is set to ["firefox"].

## Updates

```json
"updates": {
"os": "arch",
"icon": "󱧘",
"interval": 60000,
"tooltip": true,
"label": true,
"show_icon": true,
}
```

- **os** (string):
  The OS to fetch updates count for. In this case, it is set to "arch".

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󱧘".

- **interval** (integer):
  The update interval for updates. In this case, it is set to 60000 milliseconds.

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **show_icon** (boolean):
  Whether to show the icon. In this case, it is set to true.

## Volume

```json
"volume": {
"label": true,
"tooltip": true,
"step_size": 5,
}
```

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **step_size** (integer):
  The volume step size. In this case, it is set to 5.

## Weather

```json
"weather": {
"location": "",
"interval": 60000,
"tooltip": true,
"label": true
}
```

- **location** (string):
  The location to display weather for. In this case, it is set to blank string.This is optional as the weather service resolves the location with the IP thus blank. However if you are using vpn or want to fine tune the weather,  you can supply the location , which can be city name, latitude, longitude or zip code example: "Kathmandu", "27.7172,85.324", "12345".

- **interval** (integer):
  The update interval for weather. In this case, it is set to 60000 milliseconds.

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.


## Window Title

```json
"window_title": {
"truncation": true,
"truncation_size": 50,
"icon": true,
"title_map": []
}
```

- **truncation** (boolean):
  Whether to limit the window title. In this case, it is set to true.

- **truncation_size** (integer):
  Maximum length for the window title (requires truncation set to true). In this case, it is set to 50.

- **icon** (boolean):
  Whether to display the icon in the title bar. In this case, it is set to true.

- **title_map** (array):
  A map of window titles to icons. In this case, it is an empty array [].

## Workspaces

```json
"workspaces": {
  "count": 8,
  "hide_unoccupied": true,
  "reverse_scroll": false,
  "empty_scroll": false,
  "icon_map": {
    "1": "",
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

- **count** (integer):
  Number of workspaces. In this case, it is set to 8.

- **hide_unoccupied** (boolean):
  Indicates whether workspaces should show as occupied or not. In this case, it is set to true.

- **reverse_scroll** (boolean):
  Invert scroll direction. In this case, it is set to false.

- **empty_scroll** (boolean):
  Scroll to empty workspaces. In this case, it is set to false.

- **icon_map** (object):
  Map an icon to a workspace instead of the number. In this case, the icons are mapped as shown.

- **ignored** (array):
  Ignores specific workspaces from the widget. In this case, workspace 1 is ignored.
