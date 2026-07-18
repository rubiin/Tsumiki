---
title: Advanced Configuration
description: Advanced Tsumiki configuration patterns
---

Once you are comfortable with the [Configuration](/en/configuring/config) basics, these patterns help you tune Tsumiki further.

## Widget Groups

Group widgets together with shared spacing and style:

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

Reference a group in your layout with `@group:N` (zero-based index):

```toml
[layout]
right_section = ["@group:0", "system_tray"]
```

## Collapsible Groups

Hide less-used widgets behind a toggle:

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Utility Tools"
style_classes = ["utility-tools"]
```

## Multi-Monitor

Enable per-monitor panels:

```toml
[general]
multi_monitor = true
```

## Auto Hide

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

## Custom Modules

Add your own module under `modules` and reference it from `layout`. Keep changes small and restart with `./init.sh -start` to validate.
