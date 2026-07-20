---
title: Configuración Avanzada
description: Patrones avanzados de configuración de Tsumiki
---

Una vez que te sientas cómodo con los conceptos básicos de [Configuración](/es/configuring/config), estos patrones te ayudarán a ajustar Tsumiki aún más.

## Grupos de Widgets

Agrupa widgets con espaciado y estilo compartidos:

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

Referencia un grupo en tu diseño con `@group:N` (índice basado en cero):

```toml
[layout]
right_section = ["@group:0", "system_tray"]
```

## Grupos Plegables

Oculta widgets menos usados detrás de un alternador:

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Utilidades"
style_classes = ["utility-tools"]
```

## Múltiples Monitores

Activa paneles por monitor:

```toml
[general]
multi_monitor = true
```

## Auto-Ocultar

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

## Módulos Personalizados

Añade tu propio módulo bajo `modules` y referenciarlo desde `layout`. Mantén los cambios pequeños y reinicia con `./init.sh -start` para validar.
