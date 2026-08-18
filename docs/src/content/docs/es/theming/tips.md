---
title: Consejos de Tematización
description: Consejos prácticos de tematización para Tsumiki
---

Algunos consejos para aprovechar al máximo [Creación de Temas](/es/theming/making-themes) y [Matugen](/es/theming/matugen).

## Mantén el Contraste Alto

El texto debe ser legible en todas las superficies: barra, popups, notificaciones, ajustes rápidos. Usa los grupos `text*` y `background*` juntos y verifica con una comprobación de contraste.

## Prueba Superficies Comunes

Como mínimo, verifica estas después de editar un tema:

- Barra principal
- Popup de ajustes rápidos
- Notificación toast
- Lanzador y dock

## Usa Acentos Semánticos

Reserva los colores fuertes de `accent*` para estados importantes (errores, éxito, espacio de trabajo activo). Evita usar acentos neón para texto estático.

## Flujo de Trabajo con Matugen

1. Establece `matugen.enabled = true` en `config.toml`.
2. Apunta `wallpaper` a tu imagen.
3. Reinicia Tsumiki para generar la paleta.
4. Recompila los estilos si los colores se ven desactualizados: `./tsumiki.sh -recompile`.

## Aprende de Temas Existentes

Explora `styles/themes/` para referencias como `nord.scss`, `dracula.scss` y `gruvbox.scss`. Copia un tema cercano y ajústalo gradualmente.
