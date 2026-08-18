---
title: Migration von v2 zu v3
description: Schritt-für-Schritt-Anleitung zur Aktualisierung Ihrer Tsumiki-Konfiguration
sidebar:
  order: 2
---

## Wichtige Änderungen

| Bereich                  | Änderung                                                   |
| ------------------------ | ---------------------------------------------------------- |
| Konfigurationsformat     | JSON5 nicht mehr unterstützt — TOML verwenden              |
| Dock                     | Einstellungen unter `[modules.dock]`                       |
| Automatisches Ausblenden | Konfiguriert unter `[modules.bar]`                         |
| Gruppen                  | `[[widget_groups]]` und `[[collapsible_groups]]` verwenden |

## Schritt-für-Schritt-Migration

### 1. Konfigurationsformat konvertieren

**Vorher (v2):** `~/.config/tsumiki/config.json5`
**Nachher (v3):** `~/.config/tsumiki/config.toml`

```sh
cp ~/.config/tsumiki/example/config.toml ~/.config/tsumiki/config.toml
```

### 2. `power_profile` entfernen

```toml
[general]
# power_profile = "balanced"  # Schlüssel entfernen
```

### 3. Dock-Konfiguration aktualisieren

```toml
[modules.dock]
icon_size = 28
behavior = "intellihide"
```

### 4. Auto-Hide konfigurieren

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

### 5. Gruppensyntax aktualisieren

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
```

### 6. Hyprland-Layer-Regeln aktualisieren

```sh
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
```
