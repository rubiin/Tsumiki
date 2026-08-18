---
title: Personalización SCSS
description: Personalización avanzada de SCSS y variables en Tsumiki
sidebar:
  order: 3
---

Más allá de los colores del tema, Tsumiki expone variables SCSS para un control detallado sobre la apariencia de los widgets, el espaciado y el diseño.

## Cómo Funciona SCSS

Tsumiki compila SCSS de `styles/main.scss` a CSS usando `dart-sass`. La cadena de compilación es:

1. **Variables del tema** — definidas en `themes/*.toml`, compiladas en `styles/_theme.scss`
2. **Configuración SCSS** — auto-generada desde la sección styling de `config.toml` en `styles/_settings.scss`
3. **Estilos de widgets** — archivos individuales `_widgetname.scss` importan variables y componen estilos
4. **Salida** — `dist/main.css` es cargada por la aplicación

## Variables Basadas en Configuración

Algunas variables SCSS se pueden establecer directamente desde `config.toml` bajo `[styling]`:

```toml
[styling]
theme_name = "catpuccin-mocha"

[styling.bar]
background = "#1e1e2e"
border-color = "#313244"
border-radius = 16
border-enabled = true
border-width = 2
padding = "4px 12px"
margin = "0 8px"

[styling.bar.widgets]
spacing = 8

[styling.bar.widgets.workspaces]
spacing = 4
icon_size = 14
border-radius = 16
border-enabled = false
border-width = 1
pill-active_width = "1em"
pill-height = "2px"
pill-width = "0.5em"
pill-border-enabled = false
pill-border-radius = 16
pill-border-width = 2

[styling.bar.widgets.workspaces.border]
color = "#cba6f7"
```

## Referencia de Variables SCSS

Las variables se definen en `styles/_variable.scss` y `styles/_settings.scss`.

### Variables de la Barra

| Variable              | Predeterminado | Descripción                  |
| --------------------- | -------------- | ---------------------------- |
| `$bar-background`     | color del tema | Color de fondo de la barra   |
| `$bar-border-color`   | color del tema | Color del borde de la barra  |
| `$bar-border-radius`  | `16px`         | Radio de esquina de la barra |
| `$bar-border-enabled` | `false`        | Activar borde de la barra    |
| `$bar-border-width`   | `1px`          | Grosor del borde de la barra |
| `$bar-padding`        | `4px 12px`     | Relleno interno de la barra  |
| `$bar-margin`         | `0 8px`        | Margen externo de la barra   |

### Variables de Espacios de Trabajo

| Variable                                      | Predeterminado | Descripción                                        |
| --------------------------------------------- | -------------- | -------------------------------------------------- |
| `$bar-widgets-workspaces-spacing`             | `0.125em`      | Espaciado entre botones de espacios de trabajo     |
| `$bar-widgets-workspaces-icon_size`           | `12px`         | Tamaño de icono en botones de espacios de trabajo  |
| `$bar-widgets-workspaces-border-radius`       | `16px`         | Radio de borde del widget de espacios de trabajo   |
| `$bar-widgets-workspaces-border-enabled`      | `false`        | Activar borde del widget de espacios de trabajo    |
| `$bar-widgets-workspaces-border-width`        | `1px`          | Grosor del borde del widget de espacios de trabajo |
| `$bar-widgets-workspaces-pill-height`         | `1px`          | Altura del indicador de píldora                    |
| `$bar-widgets-workspaces-pill-width`          | `0.5em`        | Anchura del indicador de píldora                   |
| `$bar-widgets-workspaces-pill-active_width`   | `1em`          | Anchura expandida de píldora activa                |
| `$bar-widgets-workspaces-pill-border-enabled` | `false`        | Activar borde de píldora                           |
| `$bar-widgets-workspaces-pill-border-radius`  | `16px`         | Radio de borde de píldora                          |
| `$bar-widgets-workspaces-pill-border-width`   | `2px`          | Grosor del borde de píldora                        |

### Variables Comunes de Widgets

Cada widget que muestra un icono tiene variables de tamaño y espaciado siguiendo este patrón:

```
$bar-widgets-<nombre>-icon_size
$bar-widgets-<nombre>-spacing
```

Ejemplos comunes:

| Variable                           | Predeterminado | Widgets                      |
| ---------------------------------- | -------------- | ---------------------------- |
| `$bar-widgets-cpu-icon_size`       | `12px`         | CPU, Memoria, Almacenamiento |
| `$bar-widgets-battery-icon_size`   | `14px`         | Batería                      |
| `$bar-widgets-volume-icon_size`    | `14px`         | Volumen                      |
| `$bar-widgets-bluetooth-icon_size` | `14px`         | Bluetooth                    |
| `$bar-widgets-weather-icon_size`   | `14px`         | Clima                        |

### Variables de Diseño

| Variable               | Predeterminado   | Descripción                                      |
| ---------------------- | ---------------- | ------------------------------------------------ |
| `$quicksettings-width` | `370px`          | Anchura del panel de ajustes rápidos             |
| `$radius-large`        | `9999px`         | Radio de borde grande (completamente redondeado) |
| `$radius`              | de configuración | Radio de borde predeterminado                    |
| `$border-color`        | color del tema   | Color de borde predeterminado                    |
| `$border`              | de configuración | Abreviatura de borde                             |

## Sobreescribir SCSS

Para sobreescribir permanentemente una variable:

1. Copia la variable relevante de `_settings.scss` en tu tema personalizado.
2. O establece el valor bajo `[styling]` en `config.toml` (para variables soportadas).
3. Recompila con `./tsumiki.sh -recompile`.

## Clases de Estilo por Widget

Los grupos de widgets y widgets individuales pueden usar clases de estilo personalizadas:

```toml
[[widget_groups]]
widgets = ["workspaces", "window_title"]
spacing = 2
style_classes = ["compact"]     # Variante de espaciado más ajustado
```

Clases de estilo integradas disponibles:

| Clase      | Efecto                             |
| ---------- | ---------------------------------- |
| `compact`  | Relleno y espaciado reducidos      |
| `bordered` | Añade un borde alrededor del grupo |
| `pill`     | Contenedor en forma de píldora     |

## Añadir CSS Personalizado

Puedes añadir reglas CSS personalizadas directamente:

1. Crea `styles/custom.scss`
2. Impórtalo en `styles/main.scss`:
   ```scss
   @use "custom.scss";
   ```
3. Recompila: `./tsumiki.sh -recompile`

## Animaciones de Transición

Los botones de espacios de trabajo usan una variable de transición compartida:

```scss
$workspace-transition:
  padding 0.3s cubic-bezier(0.4, 0, 0.2, 1),
  background-color 0.4s cubic-bezier(0.4, 0, 0.2, 1);
```

Puedes sobreescribir esto en tu SCSS personalizado para diferentes curvas de animación.
