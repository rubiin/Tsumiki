---
title: Hyprland
description: Configuración relacionada con Hyprland
---

<link rel="stylesheet" href="/src/styles/tables.css">

# Estructura de configuración

```
. 📂 ~/.config/hypr
└── 📂 animations/
├── 📄 animations.conf
├── 📄 hyde.conf
├── 📄 hypridle.conf
├── 📄 hyprland.conf
└── 📂 hyprlock/
├── 📄 hyprlock.conf
├── 📄 keybindings.conf
├── 📄 monitors.conf
├── 📄 nvidia.conf
└── 📂 themes/
│ ├── 📄 colors.conf
│ ├── 📄 theme.conf
│ ├── 📄 wallbash.conf
├── 📄 userprefs.conf
└── 📄 windowrules.conf
├──
. 📂 ~/.local/share/hyde
│ ├── 📄 hyprland.conf
```

---

:::caution

**¡Lee primero la [Wiki de Hyprland](https://wiki.hyprland.org/)!**

:::

# Configuración de Hyprland en HyDE

Dado que Hyprland carga `~/.config/hypr/hyprland.conf`, la configuración de Hyprland en HyDE se divide en tres secciones:

- [Plantilla Base](#1-plantilla-base)
- [Sobrescrituras](#2-sobrescrituras)
- [Usuarios](#3-usuarios)

## 1. Plantilla Base

Esta sección contiene la configuración predeterminada de HyDE. Se recomienda no modificar esta sección.

**Ruta del archivo:** $XDG_DATA_HOME/hyde/hyprland.conf`

Este archivo se carga antes que otras configuraciones en ~/.config/hypr/hyprland.conf`.

```ini
# Configuración de plantilla base
source = ~/.local/share/hyde/hyprland.conf
```

## 2. Sobrescrituras

Esta sección es para sobrescribir la configuración predeterminada de HyDE.

Según la [Definición de Variables](https://wiki.hyprland.org/Hypr-Ecosystem/hyprlang/#defining-variables) de Hyprland, HyDE usa $VARIABLES para exponer configuraciones predeterminadas que pueden ser sobrescritas.

Modifica esta sección si deseas:

- Cambiar las variables de inicio y entorno
- Detener el inicio de una aplicación/servicio
- Sobrescribir las variables predeterminadas de HyDE

:::note

Para desactivar una variable, déjala en blanco

:::

**Ruta del archivo:** $XDG_CONFIG_HOME/hypr/hyde.conf`

### Variables de Configuración de HyDE

| Variable             | Descripción                 | Valor Predeterminado                |
| -------------------- | --------------------------- | ---------------------------- |
| $mainMod             | Modificador de teclado           | SUPER (tecla Windows)          |
| $QUICKAPPS           | Usado para el lanzador rápido de aplicaciones | (Vacío)                      |
| $BROWSER             | Navegador predeterminado             | firefox                      |
| $EDITOR              | Editor predeterminado              | code                         |
| $EXPLORER            | Gestor de archivos predeterminado        | dolphin                      |
| $TERMINAL            | Terminal predeterminada            | kitty                        |
| $LOCKSCREEN          | Pantalla de bloqueo predeterminada          | hyprlock                     |
| $IDLE                | Gestor de inactividad predeterminado        | hypridle                     |
| $GTK_THEME           | Tema GTK                   | Wallbash-Gtk                 |
| $ICON_THEME          | Tema de iconos                  | Tela-circle-dracula          |
| $COLOR_SCHEME        | Esquema de colores                | prefer-dark                  |
| $CURSOR_THEME        | Tema del cursor                | Bibata-Modern-Ice            |
| $CURSOR_SIZE         | Tamaño del cursor                 | 30                           |
| $FONT                | Fuente                        | Canterell                    |
| $FONT_SIZE           | Tamaño de fuente                   | 10                           |
| $DOCUMENT_FONT       | Fuente de documento               | Cantarell                    |
| $DOCUMENT_FONT_SIZE  | Tamaño de fuente de documento          | 10                           |
| $MONOSPACE_FONT      | Fuente monoespaciada              | CaskaydiaCove Nerd Font Mono |
| $MONOSPACE_FONT_SIZE | Tamaño de fuente monoespaciada         | 9                            |
| $FONT_ANTIALIASING   | Suavizado de fuentes           | rgba                         |
| $FONT_HINTING        | Hinting de fuentes                | full                         |

### Comandos de Inicio ($start.\*`)

Los comandos predeterminados al iniciar.

| Variable                    | Descripción                                                  | Valor Predeterminado                                                                                |
| --------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| $start.XDG_PORTAL_RESET     | Reinicia XDG Portal                                            | $scrPath/resetxdgportal.sh                                                                   |
| $start.DBUS_SHARE_PICKER    | Actualiza el entorno DBus para el selector de compartir                    | dbus-update-activation-environment --systemd --all                                           |
| $start.SYSTEMD_SHARE_PICKER | Importa variables de entorno para el selector de compartir usando systemd | systemctl --user import-environment QT_QPA_PLATFORMTHEME WAYLAND_DISPLAY XDG_CURRENT_DESKTOP |
| $start.BAR                  | Inicia Waybar                                            | waybar                                                                                       |
| $start.NOTIFICATIONS        | Inicia el daemon de notificaciones                               | swaync                                                                                       |
| $start.APPTRAY_BLUETOOTH    | Inicia el applet de Bluetooth                                  | blueman-applet                                                                               |
| $start.WALLPAPER            | Establece el fondo de pantalla                                           | $scrPath/swwwallpaper.sh                                                                     |
| $start.TEXT_CLIPBOARD       | Inicia el gestor de portapapeles de texto                            | wl-paste --type text --watch cliphist store                                                  |
| $start.IMAGE_CLIPBOARD      | Inicia el gestor de portapapeles de imágenes                           | wl-paste --type image --watch cliphist store                                                 |
| $start.BATTERY_NOTIFY       | Inicia el script de notificación de batería                       | $scrPath/batterynotify.sh                                                                    |
| $start.NETWORK_MANAGER      | Inicia el applet del gestor de red                            | nm-applet --indicator                                                                        |
| $start.REMOVABLE_MEDIA      | Inicia el gestor de medios extraíbles                           | udiskie --no-automount --smart-tray                                                          |
| $start.AUTH_DIALOGUE        | Inicia el script de diálogo de autenticación                    | $scrPath/polkitkdeauth.sh                                                                    |
| $start.IDLE_DAEMON          | Inicia el daemon de inactividad                                       | $IDLE                                                                                        |

### Variables de Entorno ($env.\*`)

| Variable                                 | Descripción                                    | Valor Predeterminado                 |
| ---------------------------------------- | ---------------------------------------------- | ----------------------------- |
| $env.GDK_BACKEND                         | Backend GTK a usar (Wayland preferido)         | wayland,x11,\*                |
| $env.QT_QPA_PLATFORM                     | Plataforma Qt a usar (Wayland)                   | wayland                       |
| $env.SDL_VIDEODRIVER                     | Controlador de video SDL2 (Wayland)                    | wayland                       |
| $env.CLUTTER_BACKEND                     | Backend Clutter (Wayland)                      | wayland                       |
| $env.XDG_CURRENT_DESKTOP                 | Entorno de escritorio actual XDG                | Hyprland                      |
| $env.XDG_SESSION_TYPE                    | Tipo de sesión XDG                               | wayland                       |
| $env.XDG_SESSION_DESKTOP                 | Escritorio de sesión XDG                            | Hyprland                      |
| $env.QT_AUTO_SCREEN_SCALE_FACTOR         | Escalado automático de pantalla Qt                    | 1                             |
| $env.QT_QPA_PLATFORM                     | Plataforma Qt                                    | wayland                       |
| $env.QT_WAYLAND_DISABLE_WINDOWDECORATION | Desactiva decoraciones de ventana en aplicaciones Qt | 1                             |
| $env.QT_QPA_PLATFORMTHEME                | Tema de plataforma Qt                              | qt6ct                         |
| $env.PATH                                | Variable de entorno PATH                      | (Vacío)                       |
| $env.MOZ_ENABLE_WAYLAND                  | Habilita Wayland para Firefox                    | 1                             |
| $env.GDK_SCALE                           | Escala GDK para Xwayland en HiDPI                | 1                             |
| $env.ELECTRON_OZONE_PLATFORM_HINT        | Pista de Plataforma Ozone de Electron                   | auto                          |
| $env.XDG_RUNTIME_DIR                     | Directorio de tiempo de ejecución XDG                          | $XDG_RUNTIME_DIR              |
| $env.XDG_CONFIG_HOME                     | Directorio de configuración XDG                           | $HOME/.config                 |
| $env.XDG_CACHE_HOME                      | Directorio de caché XDG                            | $HOME/.cache                  |
| $env.XDG_DATA_HOME                       | Directorio de datos XDG                             | $HOME/.local/share            |
| $LAYOUT_PATH                             | Ruta a la configuración de diseño de Hyprlock          | /path/to/hyprlock/layout.conf |
| $BACKGROUND_PATH                         | Ruta a la imagen de fondo de Hyprlock              | $HYPRLOCK_BACKGROUND          |

:::danger

¡Modificar esto significa que sabes lo que estás haciendo!

:::

## 3. Usuarios

Esta sección es para la configuración del usuario. Se recomienda modificar esta sección según tus preferencias.

**Rutas de archivos:**

- ./keybindings.conf
- ./windowrules.conf
- ./monitors.conf
- ./userprefs.conf

---

:::tip

Probablemente solo necesites estos archivos para configurar tus preferencias.
Las variables de Hyprland pueden ser sobrescritas, por lo que puedes cambiar los valores predeterminados según tus gustos.

Además, Hyprland puede recargar en caliente los archivos de configuración, por lo que puedes editarlos y ver los cambios inmediatamente.

:::

Ahora deberías saber qué archivo es cuál. Consulta la [Wiki de Hyprland](https://wiki.hyprland.org) para obtener más información y lograr tu experiencia de escritorio perfecta.

También consulta [Preguntas Frecuentes y Consejos](../help/faq#how-can-i-change-keyboard-layout)
