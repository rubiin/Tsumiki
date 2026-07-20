---
title: Referência de Widgets
description: Referência completa de configuração para todos os widgets do Tsumiki
sidebar:
  order: 1
---

## Sistema

```toml
[widgets.cpu]
mode = "graph"

[widgets.memory]
mode = "label"

[widgets.gpu]
mode = "circular"

[widgets.storage]
path = "/"

[widgets.network_usage]
label_format = "{upload}  {download} "

[widgets.updates]
os = "arch"
```

## Hardware

```toml
[widgets.battery]
label_format = "{icon} {percent}"

[widgets.volume]
step_size = 5

[widgets.brightness]
step_size = 5

[widgets.power]
confirm = true
```

## Área de Trabalho

```toml
[widgets.workspaces]
count = 10
style = "numbered"

[widgets.window_title]
truncation = true

[widgets.taskbar]
icon_size = 22
```

## Mídia

```toml
[widgets.mpris]
label_format = "{title} - {artist}"

[widgets.cava]
bars = 10
color = "#89b4fa"
```

## Grupos

```toml
[[widget_groups]]
widgets = ["workspaces", "window_title"]
spacing = 2
style_classes = ["compact"]

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
```
