---
title: Erweiterte Konfiguration
description: Erweiterte Tsumiki-Konfigurationsmuster
---

Sobald Sie mit den [Konfigurations](/de/configuring/config)-Grundlagen vertraut sind, helfen Ihnen diese Muster, Tsumiki weiter anzupassen.

## Widget-Gruppen

Gruppieren Sie Widgets mit gemeinsamem Abstand und Stil:

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

Referenzieren Sie eine Gruppe in Ihrem Layout mit `@group:N` (nullbasierter Index):

```toml
[layout]
right_section = ["@group:0", "system_tray"]
```

## Einklappbare Gruppen

Verbergen Sie weniger verwendete Widgets hinter einem Umschalter:

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Werkzeuge"
style_classes = ["utility-tools"]
```

## Multi-Monitor

Aktivieren Sie Pro-Monitor-Panels:

```toml
[general]
multi_monitor = true
```

## Automatisches Ausblenden

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

## Benutzerdefinierte Module

Fügen Sie Ihr eigenes Modul unter `modules` hinzu und referenzieren Sie es über `layout`. Halten Sie Änderungen klein und starten Sie mit `./init.sh -start` neu, um zu validieren.
