---
title: Modules Referentie
description: Volledige documentatie van alle Tsumiki-modules
sidebar:
  order: 2
---

Modules zijn grotere UI-oppervlakken die verder gaan dan de balk, zoals het dock, meldingen, overzicht en OSD.

## Balk

```toml
[modules.bar]
layer = "top"
auto_hide = false
auto_hide_timeout = 3000
location = "top"
```

## Meldingensysteem

```toml
[modules.notification]
enabled = true
anchor = "top-right"
auto_dismiss = true
transition_type = "slide-left"
```

## Dock

```toml
[modules.dock]
enabled = false
icon_size = 40
behavior = "intellihide"
preview_apps = true
group_apps = true
```

## Overzicht

```toml
[modules.overview]
enabled = false
layer = "top"
anchor = "center"
transition_type = "crossfade"
```

## App Launcher

```toml
[modules.app_launcher]
enabled = false
layout = "grid"
grid_columns = 3
```

## OSD

```toml
[modules.osd]
enabled = false
timeout = 3000
osds = ["brightness", "volume"]
```

## Desktopklok

```toml
[modules.desktop_clock]
enabled = false
type = "cookie"
layer = "bottom"
```

## Desktopcitaten

```toml
[modules.desktop_quotes]
enabled = false
interval = 600
```

## Activate Linux

```toml
[modules.activate_linux]
enabled = false
```

## Schermhoeken

```toml
[modules.screen_corners]
enabled = false
size = 20
```
