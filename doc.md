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
        "bar_style": "default",
        "location": "top",
        "widget_style": "default",
        "desktop_clock": true,
    }

```

- **debug** (boolean):
  Enable or disable debug mode for the panel. When set to true, additional debugging output or features may be activated.

- **location** (string; enum: "top", "bottom"):
  Determines where the panel is positioned on the screen. It can either be at the top or the bottom.

- **bar_style** (string; enum: "default", "floating"):
  Selects the style of the panel bar. "default" provides a standard appearance, while "floating" gives it a floating look.

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
  Determines whether the system should automatically check for updates.

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
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
    "icon": "󰏨",
    "step_size": 5,
}
```

- **icon_size** (string):
  Specifies the size of the icons. The value is defined in CSS units (e.g., pixels), and in this case, the icon size is set to `"14px"`.

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
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.
- round: Whether to round the temperature.
- unit: The unit of the temperature.
- show_unit: Whether to show the unit.
- sensor: The sensor to use for temperature.

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

- **enabled_icon** (string):
  Specifies the icon to be displayed when the element is enabled. In this case, the enabled icon is represented by `""`.

- **disabled_icon** (string):
  Specifies the icon to be displayed when the element is disabled. In this case, the disabled icon is represented by `""`.

- **icon_size** (string):
  Defines the size of the icon. In this case, the icon size is set to `"12px"`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

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

- **temperature** (string):
  Specifies the color temperature. In this case, the temperature is set to `"2800k"`.

- **enabled_icon** (string):
  Specifies the icon to be displayed when the element is enabled. In this case, the enabled icon is represented by `"󱩌"`.

- **disabled_icon** (string):
  Specifies the icon to be displayed when the element is disabled. In this case, the disabled icon is represented by `"󰛨"`.

- **icon_size** (string):
  Defines the size of the icon. In this case, the icon size is set to `"12px"`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

## Hyprpicker

```json
"hypr_picker": {
    "icon": "",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- **icon** (string):
  Specifies the icon to be displayed. In this case, the icon is represented by `""`.

- **icon_size** (string):
  Defines the size of the icon. In this case, the icon size is set to `"14px"`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

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

- **icon** (string):
  Specifies the icon to be displayed. In this case, the icon is represented by `""`.

- **icon_size** (string):
  Defines the size of the icon. In this case, the icon size is set to `"12px"`.

- **label** (boolean):
  Specifies whether a label should be displayed. In this case, the value is `true`, meaning the label will be shown.

- **tooltip** (boolean):
  Specifies whether a tooltip should be displayed. In this case, the value is `true`, meaning the tooltip will be shown.

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
"icon_size": "14px",
"label": true,
"tooltip": true,
}

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰐳".

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "14px".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

## Power Button

```json
"power": {"icon": "󰐥", "icon_size": "12px", "tooltip": true, "buttons": ["power", "logout", "reboot", "shutdown"] }

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰐥".

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "12px".

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **buttons** (array):
  List of buttons to show. In this case, it is set to ["power", "logout", "reboot", "shutdown"].

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
"icon_size": "14px",
"label": true,
"tooltip": true,
}

```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰋊".

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "14px".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

## Storage

```json
"storage": {
"icon": "󰋊",
"icon_size": "14px",
"label": true,
"tooltip": true,
}
```

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󰋊".

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "14px".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

## TaskBar and System Tray

```json
"task_bar": {"icon_size": 22, "ignored": ["firefox"]},
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
"icon_size": "14px",
"interval": 60000,
"tooltip": true,
"label": true,
}
```

- **os** (string):
  The OS to fetch updates count for. In this case, it is set to "arch".

- **icon** (string):
  The icon used to display the module. In this case, the icon is "󱧘".

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "14px".

- **interval** (integer):
  The update interval for updates. In this case, it is set to 60000 milliseconds.

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

## Volume

```json
"volume": {
"icon_size": "14px",
"label": true,
"tooltip": true,
"step_size": 5,
}
```

- **icon_size** (string):
  The size of the icon in px. In this case, it is set to "14px".

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **step_size** (integer):
  The volume step size. In this case, it is set to 5.

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

- **location** (string):
  The location to display weather for. In this case, it is set to "Kathmandu".

- **interval** (integer):
  The update interval for weather. In this case, it is set to 60000 milliseconds.

- **label** (boolean):
  Whether to show a label. In this case, it is set to true.

- **tooltip** (boolean):
  Whether to show a tooltip. In this case, it is set to true.

- **detect_location** (boolean):
  Whether to detect the location automatically. In this case, it is set to false.

## Window Title

```json
"window_title": {
"truncation": true,
"truncation_size": 50,
"enable_icon": true,
"title_map": []
}
```

- **truncation** (boolean):
  Whether to limit the window title. In this case, it is set to true.

- **truncation_size** (integer):
  Maximum length for the window title (requires truncation set to true). In this case, it is set to 50.

- **enable_icon** (boolean):
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
