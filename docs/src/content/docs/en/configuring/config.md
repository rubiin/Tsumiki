---
title: Configuration
description: Tsumiki configuration options and widget settings
---

Tsumiki uses TOML for configuration.

## Config Files

- `config.toml`: widgets, layout, modules, runtime behavior.
- `theme.toml`: theme selection and optional Matugen settings.
- `tsumiki.schema.json`: schema source of truth.

:::note
The schema requires top-level `widget_groups` and `collapsible_groups` sections.
Starting from `example/config.toml` is the safest way to stay schema-valid.
:::

## Quick Start Example

```toml
$schema = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true
multi_monitor = false

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["@group:0", "system_tray", "volume", "battery"]

[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Utility Tools"
style_classes = ["utility-tools"]

[modules.bar]
layer = "top"
location = "top"
auto_hide = false
auto_hide_timeout = 3000

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.date_time]
format = "%b %d %H:%M"

[widgets.volume]
label = true
step_size = 5

[widgets.battery]
label = true
tooltip = true
```

## Main Sections

### `general`

Global behavior such as debug mode, auto reload, and multi-monitor controls.

### `layout`

Controls widget placement in bar sections:

- `left_section`
- `middle_section`
- `right_section`

Each value is a list of widget IDs.

### `modules`

Enables and configures larger UI modules such as:

- `bar`
- `notification`
- `dock`
- `overview`
- `osd`

Example dock keys are under `modules.dock`, not `widgets`:

```toml
[modules.dock]
enabled = true
behavior = "intellihide"
show_when_no_windows = false
icon_size = 40
```

### `widgets`

Per-widget settings (icons, labels, thresholds, polling intervals, behavior flags).

Common widgets include:

- `workspaces`
- `window_title`
- `date_time`
- `system_tray`
- `volume`
- `battery`
- `network_usage`
- `weather`

## Migration Note

If you are upgrading from older versions, review [Migration v2 to v3](/en/resources/migration-v2-v3) before copying old config blocks.

## Recommended Workflow

1. Start from `example/config.toml`.
2. Keep your custom file small and focused.
3. Change one section at a time.
4. Restart with `./init.sh -start` to validate behavior.

## Reference Source

This page is a practical overview.
For complete key definitions and defaults, use `tsumiki.schema.json` in the project root.
