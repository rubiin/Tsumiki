---
title: Glosario
description: Términos clave utilizados en la documentación de Tsumiki
---

Una referencia rápida para términos utilizados en los documentos de Tsumiki.

## Widget

Un elemento de UI pequeño y autocontenido en el panel (por ejemplo, reloj, batería, volumen). Los widgets se configuran bajo `[widgets.<nombre>]` en `config.toml`.

## Módulo

Una superficie de UI más grande que va más allá de la barra, como el dock, las notificaciones, la vista general, el OSD o la propia barra. Los módulos se activan bajo `[modules.<nombre>]`.

## Diseño (Layout)

Define dónde aparecen los widgets en la barra mediante las listas `left_section`, `middle_section` y `right_section`.

## Tema

Un conjunto de variables de color definidas en `themes/*.toml` y consumidas por SCSS durante la compilación de estilos.

## Matugen

Una herramienta que genera paletas de colores Material You a partir de una imagen de fondo de pantalla. Consulta [Tematización con Matugen](/es/theming/matugen).

## Fabric

El sistema de widgets sobre el que está construido Tsumiki, que proporciona las primitivas de UI y el modelo de eventos.

## Grupo Plegable (Collapsible Group)

Un grupo de widgets ocultos detrás de un solo alternador, definido con `[[collapsible_groups]]` en `config.toml`.

## Grupo de Widgets (Widget Group)

Una colección nombrada de widgets con espaciado y clases de estilo compartidos, definida con `[[widget_groups]]`.
