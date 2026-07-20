---
title: Configuração Avançada
description: Padrões de configuração avançada do Tsumiki
---

## Grupos de Widgets

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

## Grupos Recolhíveis

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Ferramentas"
```

## Multi-Monitor

```toml
[general]
multi_monitor = true
```

## Ocultar Automaticamente

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```
