---
title: Widgets Referentie
description: Volledige configuratiereferentie voor alle Tsumiki-widgets
sidebar:
  order: 1
---

Widgets worden geconfigureerd onder `[widgets.<naam>]` in `config.toml` en geplaatst via `layout`-secties.

## Systeeminformatie Widgets

```toml
[widgets.cpu]
mode = "graph"

[widgets.memory]
mode = "label"

[widgets.gpu]
mode = "circular"

[widgets.storage]
path = "/"
mode = "label"

[widgets.network_usage]
label_format = "{upload}  {download} "

[widgets.updates]
os = "arch"
interval = 3600
```

## Hardware & Energie Widgets

```toml
[widgets.battery]
label_format = "{icon} {percent}"

[widgets.volume]
step_size = 5

[widgets.brightness]
step_size = 5

[widgets.power]
icon = "󰐥"
confirm = true
```

## Desktop & Werkruimte Widgets

```toml
[widgets.workspaces]
count = 10
style = "numbered"

[widgets.window_title]
truncation = true

[widgets.taskbar]
icon_size = 22
show_current_workspace_only = false
```

## Media Widgets

```toml
[widgets.mpris]
label_format = "{title} - {artist}"

[widgets.cava]
bars = 10
color = "#89b4fa"
```

## Hulpmiddelen

```toml
[widgets.screenshot]
annotation = true

[widgets.recorder]
audio = true

[widgets.clipboard]
show_images = true

[widgets.system_tray]
icon_size = 16

[widgets.git_companion]
username = "rubiin"

[widgets.weather]
location = "kathmandu"
provider = "open-meteo"
```

## Widget Groepen

```toml
[[widget_groups]]
widgets = ["workspaces", "window_title"]
spacing = 2
style_classes = ["compact"]

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Hulpmiddelen"
```
