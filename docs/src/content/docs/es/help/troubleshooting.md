---
title: Solución de Problemas
description: Diagnosticar y solucionar problemas comunes de Tsumiki
---

Esta página cubre problemas más allá de las [Preguntas Frecuentes](/es/help/faq).

## El Panel No Aparece

1. Asegúrate de que Hyprland esté ejecutándose y que las reglas de capa de [Post Instalación](/es/resources/post-install) estén aplicadas.
2. Mata cualquier barra conflictiva: `pkill nombre-barra`.
3. Inicia Tsumiki: `tsu -start` y observa la salida del registro.

## Widget Faltante

- Confirma que el widget esté habilitado en `config.toml` bajo `[widgets.<nombre>]`.
- Verifica que el widget esté listado en una sección de `layout`.
- Comprueba si hay `ModuleNotFoundError` e instala dependencias con `tsu -setup`.

## El Tema No se Aplica

- Confirma que `theme_name` en `config.toml` coincida con un archivo en `themes/`.
- Recompila los estilos: `./init.sh -recompile`.
- Para Matugen, consulta [Tematización con Matugen](/es/theming/matugen).

## Alto Uso de CPU o Memoria

- Reduce los intervalos de sondeo en la configuración de los widgets.
- Desactiva widgets y módulos no utilizados.
- Activa `auto_hide` para reducir el redespliegue.

## ¿Sigues Atascado?

Abre un issue con tu `config.toml` y los registros de `tsu -start`.
