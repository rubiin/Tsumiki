---
title: Modules Reference
description: Complete documentation for all Tsumiki modules
sidebar:
  order: 2
---

Modules are larger UI surfaces beyond the bar, such as the dock, notifications, overview, and OSD. They are configured under `[modules.<name>]` in `config.toml`.

Unlike widgets, most modules are standalone windows or overlays that need to be explicitly enabled.

---

## Bar

The bar itself is a module. Configures position, layer, auto-hide behavior.

```toml
[modules.bar]
layer = "top"           # "top" | "overlay" | "bottom" | "background"
auto_hide = false
auto_hide_timeout = 3000   # milliseconds
location = "top"           # "top" | "bottom"
```

- **`layer`**: Hyprland layer — `top` renders above windows, `background` renders below.
- **`auto_hide`**: Hides the bar after the timeout when not hovered.
- **`location`**: Bar position on screen.

---

## Notification System

Displays desktop notifications as they arrive, with stacking, grouping, and Do Not Disturb.

```toml
[modules.notification]
enabled = true
anchor = "top-right"
auto_dismiss = true
respect_expire = true
dnd_on_screencast = true
ignored = []
transition_type = "slide-left"       # "slide-left" | "slide-right" | "slide-up" | "slide-down" | "crossfade"
transition_duration = 350
per_app_limits = {}
play_sound = false
max_actions = 3
dismiss_on_hover = false
sound_file = "notification4"
max_lines = 4
max_expanded_lines = 20

[modules.notification.timeout]
low = 3000
normal = 8000
critical = 15000

[modules.notification.persist]
enabled = true
low = true
normal = true
critical = true
max_count = 200
```

- **`anchor`**: Screen position for the notification window.
- **`auto_dismiss`**: Automatically dismiss notifications after their timeout.
- **`respect_expire`**: Whether to respect the expire timeout from the notification sender.
- **`dnd_on_screencast`**: Enables Do Not Disturb mode during screen recording.
- **`per_app_limits`**: Limit notifications per application: `{ "app_name": 5 }`.
- **`persist`**: Save notifications to disk for recall after restart.

---

## Dock

A pinned-application launcher with intellihide, window previews, and app grouping.

```toml
[modules.dock]
enabled = false
ignored_apps = []
icon_size = 40
behavior = "intellihide"            # "intellihide" | "always_show"
tooltip = false
layer = "top"
show_when_no_windows = false
preview_apps = true
preview_size = [200, 130]
group_apps = true
truncation_size = 20
orientation = "horizontal"
always_show_focused = true
hide_special_workspace_apps = false
show_launcher = true
launcher_position = "last"          # "first" | "last"
ignored = []
```

- **`behavior`**: `intellihide` hides the dock when a window overlaps it; `always_show` keeps it visible.
- **`preview_apps`**: Shows window preview thumbnails on hover.
- **`group_apps`**: Groups multiple windows from the same application.
- **`show_launcher`**: Adds an application launcher icon to the dock.
- **`hide_special_workspace_apps`**: Hides apps on special workspaces (scratchpads).

### Keybindings

Navigate the dock with:

| Action | Keybinding |
|---|---|
| Focus next client | `Super+Tab` |
| Focus previous client | `Super+Shift+Tab` |
| Open launcher | `Super+Space` |
| Move client to workspace | Right-click → "Move to Workspace" |

---

## Overview (Workspace Exposé)

Full-screen overview of all workspaces and their windows.

```toml
[modules.overview]
enabled = false
layer = "top"
anchor = "center"
transition_type = "crossfade"       # "crossfade" | "slide-left" | "slide-right" | "slide-up" | "slide-down"
transition_duration = 350
```

Opens with a configurable keybinding (default: `Super+W`). Shows workspace thumbnails with click-to-focus.

---

## Application Launcher

Keyboard-driven application launcher with search, grid/list layout, and drag-to-pin.

```toml
[modules.app_launcher]
enabled = false
tooltip = true
icon_size = 35
ignored = []
anchor = "center"
width = 280
height = 320
layout = "grid"                    # "grid" | "list"
grid_columns = 3
```

- **`layout`**: `grid` shows app icons in a grid; `list` shows them as a list with names.
- **`anchor`**: Position on screen (`center`, `top`, `bottom`, etc.).
- **`ignored`**: List of desktop file names to exclude from search results.

### Keybindings

| Action | Keybinding |
|---|---|
| Open launcher | `Super+Space` |
| Navigate | Arrow keys |
| Launch app | `Enter` |
| Close | `Escape` |

---

## OSD (On-Screen Display)

Transient overlays for volume, brightness, and other adjustments.

```toml
[modules.osd]
enabled = false
timeout = 3000
anchor = "bottom-center"
orientation = "horizontal"
percentage = true
icon_size = 25
play_sound = false
transition_type = "slide-up"       # "slide-up" | "slide-down" | "slide-left" | "slide-right" | "crossfade"
transition_duration = 500
osds = ["brightness", "volume"]
```

- **`osds`**: Which OSD types to show. Available: `brightness`, `volume`, `microphone`, `lockkeys`.
- **`percentage`**: Shows a percentage indicator alongside the icon.
- **`play_sound`**: Plays a sound when the OSD appears.

---

## Desktop Clock

A decorative clock overlay on the desktop (layer bottom).

```toml
[modules.desktop_clock]
enabled = false
type = "cookie"                    # Clock widget type
layer = "bottom"
anchor = "bottom-right"
date_format = "%A, %d %B %Y"
time_format = "%H:%M"
cookie_size = 230
cookie_sides = 9
cookie_dial_style = "dots"
cookie_hour_hand_style = "fill"
cookie_minute_hand_style = "medium"
cookie_second_hand_style = "dot"
cookie_date_style = "bubble"
cookie_show_seconds = false
cookie_show_hour_marks = false
cookie_background_opacity = 1.0
cookie_widget_scale = 1.0
```

The `cookie_*` options configure the visual style of the analog clock widget.

---

## Desktop Quotes

Displays rotating inspirational quotes on the desktop.

```toml
[modules.desktop_quotes]
enabled = false
anchor = "bottom-right"
layer = "bottom"
interval = 600      # Seconds between quote rotations
```

Quotes are fetched from an external API.

---

## Activate Linux

Shows a window activation hint overlay (similar to GNOME's window overview on Alt+Tab).

```toml
[modules.activate_linux]
enabled = false
anchor = "bottom-right"
layer = "bottom"
```

---

## Screen Corners

Adds hot corners to the screen edges.

```toml
[modules.screen_corners]
enabled = false
size = 20
```

---

## Cheatsheet

A searchable Hyprland keybinding cheatsheet.

Configured under `[widgets.cheatsheet]` — see the [Widgets Reference](/en/features/widgets) for details.

---

## Settings GUI

An in-app GUI for editing Tsumiki configuration.

Triggered from the Settings widget (`[widgets.settings]`). No module-level configuration needed.
