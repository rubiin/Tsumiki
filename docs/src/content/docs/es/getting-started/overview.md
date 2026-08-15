---
title: Descripción General
description: Qué es Tsumiki, requisitos previos y conceptos clave
sidebar:
  order: 1
---

## ¿Qué es Tsumiki?

Tsumiki (anteriormente Hydepanel) es una barra de estado modular para el compositor Wayland [Hyprland](https://hyprland.org). Construido sobre el sistema de widgets [Fabric](https://github.com/Fabric-Development/fabric), proporciona una arquitectura flexible para crear paneles de escritorio personalizados mediante widgets componibles.

El nombre **Tsumiki** (積み木) significa "bloques de construcción" en japonés — reflejando el diseño modular y apilable del proyecto.

## Requisitos Previos

Antes de instalar Tsumiki, asegúrate de que tu sistema cumpla con estos requisitos:

| Requisito | Notas |
|---|---|
| [Hyprland](https://hyprland.org) | Se requiere una instalación funcional de Hyprland |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Necesario para la renderización de iconos y glifos |
| **Python 3.12+** | Tsumiki requiere Python 3.12 |
| **uv** | Administrador de paquetes de Python usado para instalar dependencias (`uv sync`) |
| **Arch Linux** (recomendado) | Paquetes optimizados para Arch; otras distros pueden necesitar configuración manual |
| **NetworkManager** | Necesario para widgets y servicios de red |
| **PipeWire** | Necesario para widgets de audio y OSD |

## Conceptos Clave

### Widgets

Los widgets son los bloques de construcción individuales que aparecen en la barra. Hay más de 45 widgets integrados que cubren:

- **Información del sistema** — CPU, memoria, GPU, almacenamiento, uso de red
- **Control de hardware** — Volumen, brillo, micrófono, batería
- **Gestión del escritorio** — Espacios de trabajo, título de ventana, barra de tareas
- **Utilidades** — Captura de pantalla, OCR, portapapeles, grabación de pantalla
- **Productividad** — Temporizador Pomodoro, tablero Kanban, cronómetro, selector de emojis
- **Integración** — Clima, controles multimedia, acompañante Git, conmutador DNS

Cada widget se configura bajo `[widgets.<nombre>]` en `config.toml`. Consulta la [Referencia de Widgets](/es/features/widgets) para la lista completa.

### Módulos

Los módulos son superficies de UI más grandes que van más allá de la barra — son ventanas o superposiciones independientes:

- **Barra** — El panel principal
- **Sistema de Notificaciones** — Visualización de notificaciones del escritorio
- **Dock** — Dock de aplicaciones con intellihide
- **Overview** — Exposé de espacios de trabajo en pantalla completa
- **Lanzador de Aplicaciones** — Búsqueda de aplicaciones mediante teclado
- **OSD** — Visualizaciones en pantalla para volumen, brillo, etc.
- **Reloj de Escritorio** — Superposición decorativa de reloj
- **Citas de Escritorio** — Visualización de citas inspiradoras

Los módulos se configuran bajo `[modules.<nombre>]` en `config.toml`. Consulta la [Referencia de Módulos](/es/features/modules) para más detalles.

### Diseño (Layout)

La colocación de widgets en la barra se controla mediante la sección `[layout]` de `config.toml`:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Los widgets también se pueden agrupar o colocar en grupos plegables. Consulta [Configuración](/es/configuring/config) para más detalles.

### Servicios

Los servicios son procesos en segundo plano que suministran datos a los widgets — monitorean niveles de batería, estado de red, reproductores multimedia, clima y más. Los widgets se conectan a los servicios mediante señales GTK, manteniendo las actualizaciones eficientes.

## Arquitectura

La arquitectura de Tsumiki sigue un diseño en capas:

```text
┌──────────────────────────────────────────────┐
│                  main.py                       │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│   │ Config    │  │ CSS      │  │ Module     │  │
│   │ Loader   │  │ Compiler │  │ Init       │  │
│   └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────┬────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Services │  │ Widgets  │  │ Modules  │
  │ (DBus,   │──▶│ (Panel   │──▶│ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **Servicios** se ejecutan en segundo plano y emiten señales GTK en los cambios de estado
- **Widgets** son botones del panel que se suscriben a las señales de los servicios
- **Módulos** son ventanas GTK independientes para superposiciones y ventanas emergentes

Consulta la página de [Arquitectura](/es/resources/architecture) para una visión más profunda.

## Ruta Recomendada

1. **[Instalar Tsumiki](/es/getting-started/installation)** — Clonar, instalar dependencias, configurar el entorno.
2. **Seguir [Primeros Pasos](/es/getting-started/first-steps)** — Iniciar la barra, configurar el diseño, aplicar reglas post-instalación.
3. **Aprender [Configuración](/es/configuring/config)** — Entender la estructura TOML y las opciones disponibles.
4. **Elegir un tema** — Comenzar con un tema incorporado o crear el tuyo propio con [Creación de Temas](/es/theming/making-themes).
5. **Explorar** — Añadir widgets, activar módulos, personalizar el comportamiento.

## ¿Necesitas Ayuda?

- Consulta las [Preguntas Frecuentes](/es/help/faq) para problemas comunes.
- Visita [Solución de Problemas](/es/help/troubleshooting) para orientación de depuración.
- Únete al [Discord](https://discord.gg/8nWbDC4SnP) para soporte de la comunidad.
