---
title: Migratie v2 naar v3
description: Gids voor het upgraden van uw Tsumiki-configuratie
sidebar:
  order: 2
---

| Wijziging | Detail |
|---|---|
| Formaat | JSON5 → TOML |
| Dock | Onder `[modules.dock]` |
| Autom. verbergen | Onder `[modules.bar]` |
| Groepen | `[[widget_groups]]` en `[[collapsible_groups]]` |

```sh
cp ~/.config/tsumiki/example/config.toml ~/.config/tsumiki/config.toml
```

```toml
[modules.dock]
icon_size = 28
behavior = "intellihide"

[modules.bar]
auto_hide = true
auto_hide_timeout = 3000

[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
```
