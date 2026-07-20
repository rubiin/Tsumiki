---
title: Geavanceerde Configuratie
description: Geavanceerde Tsumiki-configuratiepatronen
---

Zodra u vertrouwd bent met de [Configuratie](/nl/configuring/config) basisprincipes, helpen deze patronen u om Tsumiki verder af te stemmen.

## Widget Groepen

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

## Inklapbare Groepen

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Hulpmiddelen"
style_classes = ["utility-tools"]
```

## Multi-Monitor

```toml
[general]
multi_monitor = true
```

## Automatisch Verbergen

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```
