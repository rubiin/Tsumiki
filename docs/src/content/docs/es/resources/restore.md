---
title: Restaurar Configuración
description: Lógica del script de restauración
---

:::note

> "restore" en este contexto significa restaurar los dotfiles desde el repositorio a tu $HOME, no al revés.

```sh
./restore_cfg.sh </ruta/al/archivo.psv> <opcional /ruta/al/clon/de/hyde>
```

:::

## Valores Separados por Pipe (PSV)

Este es un archivo de valores separados por pipe. Contiene las rutas de los dotfiles y sus respectivas dependencias de paquetes.

#### Nota:

- Las líneas que comienzan con `#` son comentarios.
- La única variable conocida es `${HOME}`.
- Este es un archivo de 4 columnas separadas por `|`.
- Cada columna debe usar espacios para separar elementos de matriz.

#### Estructura:

```shell
bandera|ruta|destino|dependencia
```

#### Banderas:

- **( P ) Poblar/Preservar**

  - Esta bandera asegura que el destino solo se copie si aún no existe. Es útil para preservar el estado actual del destino, evitando cualquier sobrescritura o modificación a archivos o directorios existentes.

- **( S ) Sincronizar**

  - Si el/los archivo(s) de destino existen, sobrescríbelos.
  - Si el destino es un directorio, solo sobrescribe los archivos que están listados.
  - Preserva otros archivos en el directorio de destino que no están listados.
  - Este comportamiento es similar al comando `cp -r`.

- **( O ) Sobrescribir**

  - Esta bandera realiza una operación de sincronización agresiva. Asegura que el destino sea completamente reemplazado por la fuente.
  - Si el destino es un directorio, cada archivo y subdirectorio dentro de él será sobrescrito por los elementos correspondientes de la fuente.
  - Si el destino es un archivo, será completamente sobrescrito por el archivo fuente.
  - Esta operación no preserva ningún archivo o directorio existente en la ubicación de destino; todo es reemplazado.
  - Útil para actualizar configuraciones y scripts principales.

- **( B ) Respaldo**
  - Respalda el destino.
  - Todas las banderas P, S, O también respaldarán el archivo/directorio de destino.

<details>
<summary>Archivo PSV de ejemplo</summary>

```shell
 Archivos principales de Hyde 
P|${HOME}/.config/hyde|config.toml|hyprland
P|${HOME}/.config/hypr|hyde.conf animations.conf windowrules.conf keybindings.conf userprefs.conf monitors.conf|hyprland
P|${HOME}/.config/hypr|nvidia.conf|hyprland nvidia-utils
P|${HOME}/.config/hypr/themes|theme.conf wallbash.conf colors.conf|hyprland
P|${HOME}/.local/state|hyde|hyprland

S|${HOME}/.config/hypr|hyprland.conf|hyprland
S|${HOME}/.local|bin|hyprland
S|${HOME}/.config|gtk-3.0|nwg-look
S|${HOME}/.config|nwg-look|nwg-look
S|${HOME}/.config|xsettingsd|nwg-look
S|${HOME}|.gtkrc-2.0|nwg-look
S|${HOME}/.config|Kvantum|kvantum
S|${HOME}/.config|qt5ct|qt5ct
S|${HOME}/.config|qt6ct|qt6ct
S|${HOME}/.config/hyde|wallbash|hyprland
S|${HOME}/.config/hypr|animations|hyprland

O|${HOME}/.local/share|hyde|hyprland
O|${HOME}/.local/lib|hyde|hyprland

 Editor 
P|${HOME}/.config/Code - OSS/User|settings.json|code
P|${HOME}/.config/Code/User|settings.json|visual-studio-code-bin
P|${HOME}/.config/VSCodium/User|settings.json|vscodium-bin

 Barra 
P|${HOME}/.config/waybar|config.ctl|waybar
S|${HOME}/.config/waybar|modules config.jsonc theme.css style.css|waybar

 Terminal 
P|${HOME}/.config|lsd|lsd
S|${HOME}/.config|fastfetch|fastfetch
S|${HOME}/.config/kitty|hyde.conf theme.conf|kitty
P|${HOME}/.config/kitty|kitty.conf|kitty

 Shell 
P|${HOME}/.config|fish|fish
P|${HOME}|.zshrc .hyde.zshrc .p10k.zsh|zsh zsh-theme-powerlevel10k pokego-bin
S|${HOME}|.zshenv|zsh zsh-theme-powerlevel10k

 Explorador de archivos 
P|${HOME}/.local/state|dolphinstaterc|dolphin
P|${HOME}/.config|baloofilerc|dolphin
S|${HOME}/.config/menus|applications.menu|dolphin
S|${HOME}/.config|dolphinrc|dolphin
S|${HOME}/.config|kdeglobals|dolphin
S|${HOME}/.local/share/kio/servicemenus|hydewallpaper.desktop|dolphin
S|${HOME}/.local/share/kxmlgui5|dolphin|dolphin
S|${HOME}/.local/share|dolphin|dolphin

 Entrada 
P|${HOME}/.config|libinput-gestures.conf|libinput-gestures

 Wayland 
P|${HOME}/.config|spotify-flags.conf|spotify
P|${HOME}/.config|code-flags.conf|code
P|${HOME}/.config|code-flags.conf|visual-studio-code-bin
P|${HOME}/.config|vscodium-flags.conf|vscodium-bin
P|${HOME}/.config|electron-flags.conf|electron

 Notificaciones 
S|${HOME}/.config|dunst|dunst

 Juegos 
S|${HOME}/.config|MangoHud|mangohud

 Lanzador 
S|${HOME}/.config|rofi|rofi
S|${HOME}/.config|wlogout|wlogout

 Pantalla de bloqueo 
S|${HOME}/.config|swaylock|swaylock-effects
P|${HOME}/.config/hypr|hyprlock.conf|hyprlock
S|${HOME}/.config/hypr|hyprlock|hyprlock

 Demonio de inactividad 
P|${HOME}/.config/hypr|hypridle.conf|hypridle
```

</details>

## Configuración TOML

🚧 🚧 Trabajo en progreso 🚧🚧

El archivo de configuración PSV es conveniente para que el script lo lea y escriba. Sin embargo, es muy restrictivo y no es fácil de usar.
Para una mayor personalización, podemos usar archivos de configuración TOML.

...
