---
title: Migrating from v2 to v3
description: Step-by-step guide for upgrading your Tsumiki configuration from v2 to v3.
sidebar:
  order: 2
---

import { Steps, Aside } from "@astrojs/starlight/components";

This guide covers every breaking change between Tsumiki v2 and v3 and explains how to update your configuration.

---

## Overview of breaking changes

| Area | Change |
|---|---|
| Config format | JSON5 no longer supported — use TOML |
| Power profile | `power_profile` option removed from `general` |
| Dock config | Restructured under `[widgets.dock.behavior]` |
| Bar auto-hide | Moved to `[general]` |
| Widget groups | Renamed from `widget_groups` to `collapsible_groups` |
| `all_visible` param | Removed from widget constructors |

---

## Step-by-step migration

<Steps>

### 1. Convert your config file format

JSON5 is no longer supported. If you used a `.json5` config, convert it to TOML (recommended).

**Before (v2):** `~/.config/tsumiki/config.json`

**After (v3):** `~/.config/tsumiki/config.toml`

A quick conversion using `python-toml`:

```sh
python3 -c "
import json, sys
with open('config.json') as f:
    data = json.load(f)          # json must already be valid json
import tomllib, tomli_w
with open('config.toml', 'wb') as f:
    tomli_w.dump(data, f)
"
```

Or copy the example config and re-apply your customizations:

```sh
cp ~/.config/tsumiki/example/config.toml ~/.config/tsumiki/config.toml
```

### 2. Remove `power_profile` from general settings

The `power_profile` key is no longer recognized. Delete it from your `[general]` section.

```toml
# Before (v2) — remove this line
[general]
power_profile = "balanced"   # ← delete

# After (v3)
[general]
# (no power_profile key)
```

### 3. Update dock configuration

Dock behavior options are now nested under `[widgets.dock.behavior]`.

```toml
# Before (v2)
[widgets.dock]
show_when_no_windows = true
icon_size = 28

# After (v3)
[widgets.dock]
icon_size = 28

[widgets.dock.behavior]
show_when_no_windows = true
```

### 4. Add bar auto-hide if you use it

Auto-hide was added in v2.9.0. If you want it, add it to `[general]`:

```toml
[general]
auto_hide = true          # hide bar after timeout
auto_hide_timeout = 3000  # milliseconds
```

### 5. Update widget groups syntax

If you used `widget_groups`, the option is now `collapsible_groups` and each entry requires `style_classes` to be a list:

```toml
# Before (v2)
[[widgets.widget_groups]]
widgets = ["updates", "battery"]
spacing = 4

# After (v3)
[[widgets.collapsible_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

### 6. Add new required sections for new widgets

Several widgets added in v2 may not be present in old configs. Add them if you want to use them, or they will use defaults.

```toml
[widgets.settings]
icon = "󰒓"
tooltip = true
label = false

[widgets.wallpaper]
icon = "󰸉"
label = false
tooltip = true

[widgets.overview_button]
icon = "󱃬"
tooltip = true
label = false
```

### 7. Update Matugen theming (if used)

Matugen integration moved to its own section in `theme.toml`. Copy the latest example:

```sh
cp ~/.config/tsumiki/example/theme.toml ~/.config/tsumiki/theme.toml
```

Then re-apply your colour overrides. See the [Theming guide](/en/theming/overview) for full details.

### 8. Update Hyprland layer rules

The process name changed. Ensure your `hyprland.conf` uses `tsumiki`:

```sh
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
```

</Steps>

---

## Removed features

| Feature | Status |
|---|---|
| Cheatsheet module | Removed — configure keybinds in `[general.keybinds]` instead |
| `always_occluded` dock option | Removed — use `[widgets.dock.behavior]` instead |
| `all_visible` widget parameter | Removed — visibility is now derived automatically |
| `CircleImage` class (internal) | Renamed to `CircularImage` |

---

## New features in v3

These are opt-in and not required for existing configs to work, but worth adopting:

- **Settings GUI** — in-app settings editor (`[widgets.settings]`)
- **Multi-monitor support** — configure per-monitor bars
- **Swipe-to-dismiss** notifications
- **Notification battery alerts** — configure under `[widgets.battery.notifications]`
- **Custom module** — run arbitrary scripts and show output in the bar (`[widgets.custom_module]`)
- **Matugen palette theming** — auto-generate colours from your wallpaper

---

## Getting help

If you run into issues after migrating:

- Check the [FAQ](/en/help/faq)
- Open an issue on [GitHub](https://github.com/rubiin/tsumiki/issues)
- Join the [Discord](https://discord.gg/8nWbDC4SnP)
