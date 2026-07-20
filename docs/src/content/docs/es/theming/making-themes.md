---
title: Creación de Temas
description: Cómo crear temas para Tsumiki
---

Esta guía te muestra cómo crear un tema personalizado de Tsumiki desde cero.

## Dónde Viven los Temas

Crea tu archivo de tema en `themes/` con extensión `.toml`.

Ejemplo:

```bash
touch themes/mi-tema.toml
```

## Plantilla de Tema Mínimo

Copia este iniciador y ajusta los valores:

```toml
[dark.background]
main =  "#121212"  # Fondo principal (oscuro, casi negro con un ligero matiz grisáceo)
alt =  "#1a1a1a"  # Fondo secundario (gris oscuro industrial)
dark =  "#0a0a0a"  # Fondo más oscuro (negro profundo, ultra oscuro)


[dark.text]
main =  "#e0e0e0"  # Color de texto principal (gris claro, casi blanco)
secondary =  "#c5c5c5"  # Color de texto secundario (gris claro suave)
muted =  "#8e8e8e"  # Texto terciario, atenuado (gris oscuro)
disabled =  "#666666"  # Texto deshabilitado (gris atenuado)
muted_light =  "#999999"  # Texto claro atenuado para sugerencias (gris claro)
muted_dark =  "#444444"  # Texto oscuro atenuado (gris con un ligero tinte violáceo)


[dark.surface]
disabled =  "#444444"  # Elementos deshabilitados (gris oscuro)
neutral =  "#333333"  # Superficie neutral para tarjetas, paneles (gris oscuro con ligeros matices azules)
highlight =  "#00f0f0"  # Selección y resaltados (cian neón)


[dark.accent]
light =  "#ff007f"  # Acento claro (rosa neón)
pink =  "#ff007f"  # Acento rosa (rosa neón)
purple =  "#9c00ff"  # Acento púrpura (púrpura eléctrico)
red =  "#ff1744"  # Rojo para errores y advertencias (rojo neón brillante)
orange =  "#ff6d00"  # Naranja para alertas (naranja neón vibrante)
yellow =  "#ffea00"  # Amarillo para resaltados (amarillo eléctrico)
green =  "#00ff00"  # Verde para éxito (verde neón)
teal =  "#00b3b3"  # Verde azulado para información (cian brillante)
blue =  "#00d0ff"  # Azul para enlaces y acciones (azul eléctrico)
light_blue =  "#00d0ff"  # Acento azul cielo (azul eléctrico)
lavender =  "#b084ff"  # Lavanda para resaltados sutiles (lavanda neón)


[dark.general]
bar_background =  "rgba(18, 18, 18, 0.8)"  # Fondo del panel (fondo oscuro semi-transparente)
shadow_color =  "rgba(0, 0, 0, 0.6)"  # Color de sombra (sombras profundas con alto contraste)


[light.background]
main =  "#ededed"  # Fondo principal
alt =  "#e5e5e5"  # Fondo secundario
dark =  "#f5f5f5"  # Fondo más oscuro


[light.text]
main =  "#1f1f1f"  # Color de texto principal
secondary =  "#3a3a3a"  # Color de texto secundario
muted =  "#717171"  # Texto terciario, atenuado
disabled =  "#999999"  # Texto deshabilitado
muted_light =  "#666666"  # Texto claro atenuado para sugerencias
muted_dark =  "#bbbbbb"  # Texto oscuro atenuado


[light.surface]
disabled =  "#bbbbbb"  # Elementos deshabilitados
neutral =  "#cccccc"  # Superficie neutral para tarjetas, paneles
highlight =  "#ff0f0f"  # Selección y resaltados


[light.accent]
light =  "#00ff80"  # Acento claro
pink =  "#00ff80"  # Acento rosa
purple =  "#63ff00"  # Acento púrpura
red =  "#00e8bb"  # Rojo para errores y advertencias
orange =  "#0092ff"  # Naranja para alertas
yellow =  "#0015ff"  # Amarillo para resaltados
green =  "#ff00ff"  # Verde para éxito
teal =  "#ff4c4c"  # Verde azulado para información
blue =  "#ff2f00"  # Azul para enlaces y acciones
light_blue =  "#ff2f00"  # Acento azul cielo
lavender =  "#4f7b00"  # Lavanda para resaltados sutiles


[light.general]
bar_background =  "rgba(237, 237, 237, 0.8)"  # Fondo del panel
shadow_color =  "rgba(255, 255, 255, 0.6)"  # Color de sombra

```

## Activar tu Tema

Establece el nombre del tema en `config.toml` bajo styling:

```toml
[styling]
theme_name = "mi-tema"
```

Luego reinicia Tsumiki o recarga tu configuración.

## Grupos de Variables

Usa estos grupos como modelo mental mientras editas:

- `background*`: fondos del panel y popups.
- `text*`: legibilidad del contenido y énfasis.
- `surface*`: tarjetas, botones y estados de hover.
- `accent*`: colores semánticos para acciones y estado.
- `bar-background`, `shadow-color`, `ws-*`: detalles específicos de la barra.

## Buenas Prácticas de Temas

1. Mantén el contraste del texto alto contra los colores de fondo.
2. Reserva colores de acento fuertes para estados importantes.
3. Mantén una saturación similar entre colores relacionados.
4. Prueba superficies comunes: barra, ajustes rápidos, notificaciones, popups.

## Ejemplo: Tema Océano

```toml
[dark.background]
main =  "#1e1e2e"  # Fondo principal
alt =  "#181825"  # Fondo secundario
dark =  "#11111b"  # Fondo más oscuro


[dark.text]
main =  "#cdd6f4"  # Color de texto principal
secondary =  "#bac2de"  # Color de texto secundario
muted =  "#a6adc8"  # Texto terciario, atenuado
disabled =  "#6c7086"  # Texto para elementos deshabilitados
muted_light =  "#7f849c"  # Texto claro atenuado para sugerencias
muted_dark =  "#9399b2"  # Texto oscuro atenuado


[dark.surface]
disabled =  "#313244"  # Fondo para elementos deshabilitados
neutral =  "#45475a"  # Superficie neutral para tarjetas, paneles
highlight =  "#585b70"  # Selección y resaltados


[dark.accent]
light =  "#f5e0dc"  # Acento más claro (Rosewater)
pink =  "#f5c2e7"  # Acento rosa
purple =  "#cba6f7"  # Acento malva
red =  "#f38ba8"  # Rojo para errores y advertencias
orange =  "#fab387"  # Naranja para advertencias y alertas
yellow =  "#f9e2af"  # Amarillo para resaltados
green =  "#a6e3a1"  # Verde para éxito
teal =  "#94e2d5"  # Verde azulado para información
blue =  "#89b4fa"  # Azul para enlaces y acciones
light_blue =  "#89dceb"  # Acento azul cielo
lavender =  "#b4befe"  # Lavanda para resaltados sutiles


[dark.general]
bar_background =  "rgb(36, 35, 35)"
shadow_color =  "rgba(0, 0, 0, 0.6)"


[light.background]
main =  "#e1e1d1"  # Fondo principal
alt =  "#e7e7da"  # Fondo secundario
dark =  "#eeeee4"  # Fondo más oscuro


[light.text]
main =  "#32290b"  # Color de texto principal
secondary =  "#453d21"  # Color de texto secundario
muted =  "#595237"  # Texto terciario, atenuado
disabled =  "#938f79"  # Texto para elementos deshabilitados
muted_light =  "#807b63"  # Texto claro atenuado para sugerencias
muted_dark =  "#6c664d"  # Texto oscuro atenuado


[light.surface]
disabled =  "#cecdbb"  # Fondo para elementos deshabilitados
neutral =  "#bab8a5"  # Superficie neutral para tarjetas, paneles
highlight =  "#a7a48f"  # Selección y resaltados


[light.accent]
light =  "#0a1f23"  # Acento más claro
pink =  "#0a3d18"  # Acento rosa
purple =  "#345908"  # Acento púrpura
red =  "#0c7457"  # Rojo para errores y advertencias
orange =  "#054c78"  # Naranja para advertencias y alertas
yellow =  "#061d50"  # Amarillo para resaltados
green =  "#591c5e"  # Verde para éxito
teal =  "#6b1d2a"  # Verde azulado para información
blue =  "#764b05"  # Azul para enlaces y acciones
light_blue =  "#762314"  # Acento azul cielo
lavender =  "#4b4101"  # Lavanda para resaltados sutiles


[light.general]
bar_background =  "rgb(36, 35, 35)"
shadow_color =  "rgba(0, 0, 0, 0.6)"


```

## Aprende de Temas Existentes

Explora `styles/themes/` para referencias como `nord.scss`, `dracula.scss` y `gruvbox.scss`.
