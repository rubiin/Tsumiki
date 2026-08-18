---
title: الترحيل من v2 إلى v3
description: دليل ترقية إعدادات تسوميكي
sidebar:
  order: 2
---

| التغيير          | التفاصيل                                       |
| ---------------- | ---------------------------------------------- |
| الصيغة           | JSON5 → TOML                                   |
| الإرساء          | تحت `[modules.dock]`                           |
| الإخفاء التلقائي | تحت `[modules.bar]`                            |
| المجموعات        | `[[widget_groups]]` و `[[collapsible_groups]]` |

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
