---
title: Migration v2 vers v3
description: Guide de mise à niveau de votre configuration
sidebar:
  order: 2
---

| Changement    | Détail                                          |
| ------------- | ----------------------------------------------- |
| Format        | JSON5 → TOML                                    |
| Dock          | Sous `[modules.dock]`                           |
| Auto-masquage | Sous `[modules.bar]`                            |
| Groupes       | `[[widget_groups]]` et `[[collapsible_groups]]` |

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
style_classes = ["bordered"]

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
```
