---
title: Gelişmiş Yapılandırma
description: Gelişmiş Tsumiki yapılandırma desenleri
---

## Widget Grupları

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

## Daraltılabilir Gruplar

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Araçlar"
```

## Çoklu Monitör

```toml
[general]
multi_monitor = true
```

## Otomatik Gizleme

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```
