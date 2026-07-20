---
title: Migración de v2 a v3
description: Guía paso a paso para actualizar su configuración de Tsumiki de v2 a v3
sidebar:
  order: 2
---

## Resumen de cambios importantes

| Área | Cambio |
|---|---|
| Formato de configuración | JSON5 ya no es compatible — use TOML |
| Dock | Los ajustes del dock están bajo `[modules.dock]` |
| Auto-ocultar barra | Configurado bajo `[modules.bar]` |
| Grupos | Use `[[widget_groups]]` y `[[collapsible_groups]]` |

## Migración paso a paso

### 1. Convertir el formato de configuración

**Antes (v2):** `~/.config/tsumiki/config.json5`
**Después (v3):** `~/.config/tsumiki/config.toml`

```sh
cp ~/.config/tsumiki/example/config.toml ~/.config/tsumiki/config.toml
```

### 2. Eliminar `power_profile`

```toml
[general]
# power_profile = "balanced"  # eliminar esta clave
```

### 3. Actualizar configuración del dock

```toml
[modules.dock]
icon_size = 28
behavior = "intellihide"
```

### 4. Configurar auto-ocultar

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

### 5. Actualizar sintaxis de grupos

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

### 6. Actualizar reglas de capa de Hyprland

```sh
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
```
