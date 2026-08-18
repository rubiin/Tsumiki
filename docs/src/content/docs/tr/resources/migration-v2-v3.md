---
title: v2'den v3'e Geçiş
description: Tsumiki yapılandırmanızı yükseltme kılavuzu
sidebar:
  order: 2
---

| Değişiklik       | Detay                                           |
| ---------------- | ----------------------------------------------- |
| Biçim            | JSON5 → TOML                                    |
| Dock             | `[modules.dock]` altında                        |
| Otomatik gizleme | `[modules.bar]` altında                         |
| Gruplar          | `[[widget_groups]]` ve `[[collapsible_groups]]` |

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
