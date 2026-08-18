---
title: Primeros Pasos
description: Qué hacer justo después de instalar Tsumiki
sidebar:
  order: 3
---

Has instalado Tsumiki y aplicado los pasos de [Post Instalación](/es/resources/post-install). Aquí te mostramos cómo obtener un panel funcional rápidamente.

## 1. Iniciar el Panel

Desde el directorio del proyecto Tsumiki, ejecuta:

```sh
./init.sh -start
```

Si Hyprland está en ejecución, la barra debería aparecer en la parte superior de tu pantalla. Si la barra no aparece, verifica la salida de errores en la terminal y consulta [Solución de Problemas](/es/help/troubleshooting).

:::tip
Puedes detener Tsumiki en cualquier momento con:

```sh
pkill tsumiki
```

:::

## 2. Configurar Inicio Automático

Añade Tsumiki a tu configuración de Hyprland para que se lance automáticamente al iniciar sesión:

Abre `~/.config/hypr/hyprland.conf` y añade:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

El retardo `sleep 5` le da tiempo a Hyprland para inicializarse completamente. Ajusta la ruta si clonaste Tsumiki en un directorio diferente.

## 3. Copiar la Configuración de Ejemplo

Tsumiki incluye una configuración de ejemplo completa. Cópiala para obtener un punto de partida válido:

```sh
cp example/config.toml config.toml
```

:::tip
Abre `example/config.toml` en un editor de texto para ver todas las opciones disponibles con documentación.
:::

## 4. Personalizar tu Diseño

Edita `config.toml` y ajusta la sección `[layout]`. Cada sección (`left_section`, `middle_section`, `right_section`) es un array de nombres de widgets:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Esto crea una barra con:

| Sección       | Widgets                                                                     |
| ------------- | --------------------------------------------------------------------------- |
| **Izquierda** | Selector de espacios de trabajo, título de ventana activa                   |
| **Centro**    | Fecha y hora actuales                                                       |
| **Derecha**   | Control de volumen, estado de batería, bandeja del sistema, menú de energía |

## 5. Recargar para Aplicar Cambios

Después de guardar tus ediciones, reinicia Tsumiki:

```sh
pkill tsumiki
./init.sh -start
```

Si la configuración es válida, la barra debería reaparecer con tu nuevo diseño.

## 6. Probar Widgets Comunes

Intenta interactuar con tus widgets:

- **Espacios de trabajo** — Haz clic para cambiar, desplázate para recorrer los escritorios.
- **Volumen** — Haz clic para silenciar/activar sonido, desplázate para ajustar.
- **Batería** — Pasa el cursor para ver el tiempo restante y el estado de carga.
- **Fecha/Hora** — Haz clic para abrir el calendario y el panel de notificaciones.
- **Bandeja del Sistema** — Los iconos de la bandeja deberían aparecer automáticamente.

## 7. Hazlo Tuyo

- **Cambia colores** — Consulta [Creación de Temas](/es/theming/making-themes) para personalización SCSS o [Matugen](/es/theming/matugen) para tematización automática basada en el fondo de pantalla.
- **Añade más widgets** — Explora la [Referencia de Widgets](/es/features/widgets) para los más de 45 widgets disponibles.
- **Activa módulos** — Prueba el [Dock](/es/features/modules#dock), el [Lanzador de Aplicaciones](/es/features/modules#lanzador-de-aplicaciones) o el [OSD](/es/features/modules#osd-visualización-en-pantalla).
- **Configura el comportamiento** — Consulta la referencia completa de [Configuración](/es/configuring/config) para cada opción.

## Solución de Problemas

Si algo parece incorrecto:

- **La barra no aparece** — Verifica que estés ejecutando Hyprland y que no haya otras barras en ejecución (`pkill waybar`).
- **Sin iconos** — Verifica que [JetBrains Nerd Font](https://www.nerdfonts.com) esté instalada y configurada como fuente de tu terminal/UI.
- **Funcionalidad faltante** — Algunos widgets requieren herramientas externas (ej., `playerctl` para medios, `brightnessctl` para brillo). Ejecuta `./init.sh -setup` para asegurarte de que todas las dependencias estén instaladas (las dependencias de Python se instalan con `uv sync`).
- **Errores SASS** — Tu `config.toml` puede ser inválido. Compáralo con `example/config.toml`.

Para más ayuda, consulta las páginas de [Preguntas Frecuentes](/es/help/faq) o [Solución de Problemas](/es/help/troubleshooting).
