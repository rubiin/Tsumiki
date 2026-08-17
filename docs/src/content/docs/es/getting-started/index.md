---
title: Inicio Rápido
description: Pon Tsumiki en funcionamiento en minutos
---

Tsumiki es una barra de estado modular para Hyprland construida sobre el sistema de widgets Fabric.

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- **Hyprland** — una instalación funcional de Hyprland
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` debe mostrar 3.12 o superior
- **uv** — Administrador de paquetes de Python usado para instalar dependencias (`uv sync`)

## Instalación Rápida

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

La bandera `-setup` instala todos los paquetes de sistema necesarios y las dependencias de Python. Es posible que se te solicite tu contraseña durante la configuración.

Para métodos de instalación alternativos (script bootstrap, configuración manual), consulta la [guía de instalación completa](/es/getting-started/installation).

## Inicio Automático

Añade esta línea a `~/.config/hypr/hyprland.conf`:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Configuración Mínima

Aquí tienes un `config.toml` mínimo para comenzar:

```toml
"$schema" = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

Después de guardar, reinicia la barra:

```sh
pkill tsumiki
./init.sh -start
```

## Siguientes Pasos

<CardGrid stagger>
  <Card title="Primeros Pasos" icon="rocket">
    Configura tu diseño, prueba widgets y personalízalo.
    <br />
    <a href="/es/getting-started/first-steps">Leer guía →</a>
  </Card>
  <Card title="Configuración" icon="setting">
    Aprende sobre cada widget, módulo y opción.
    <br />
    <a href="/es/configuring/config">Leer docs →</a>
  </Card>
  <Card title="Reglas Post-Instalación" icon="list">
    Añade reglas de capa de Hyprland para efectos de desenfoque y popup.
    <br />
    <a href="/es/resources/post-install">Ver reglas →</a>
  </Card>
  <Card title="FAQ y Ayuda" icon="question">
    Problemas comunes y consejos de solución.
    <br />
    <a href="/es/help/faq">Obtener ayuda →</a>
  </Card>
</CardGrid>
