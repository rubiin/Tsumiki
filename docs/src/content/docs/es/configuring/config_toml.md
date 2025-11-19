---
title: Config Toml
description: Guía de Configuración de HyDE
sidebar:
  order: 2
---

<link rel="stylesheet" href="/src/styles/tables.css">

HyDE expone el archivo `xdg_config/hyde/config.toml` para que los usuarios puedan modificarlo. Esto permite a los usuarios interactuar con los scripts sin necesidad de usar argumentos de línea de comandos.

---

### Variable de entorno

Ejemplo:

| Clave                 | Descripción            | Valor predeterminado |
| ------------------- | ---------------------- | ------- |
| WARP_ENABLE_WAYLAND | Habilitar soporte Wayland |         |

### [battery.notify]

| Clave      | Descripción             | Valor predeterminado |
| -------- | ----------------------- | ------- |
| dock     | Notificación de batería en dock     | true    |
| interval | Intervalo de notificación de batería | 5       |
| notify   | Notificación de batería          | 1140    |
| timer    | Temporizador de notificación de batería    | 120     |

### [battery.notify.execute]

| Clave         | Descripción                        | Valor predeterminado             |
| ----------- | ---------------------------------- | ------------------- |
| charging    | Ejecutar al cargar batería    | ""                  |
| critical    | Ejecutar en batería crítica    | "systemctl suspend" |
| discharging | Ejecutar al descargar batería | ""                  |
| low         | Ejecutar en batería baja         | ""                  |
| unplug      | Ejecutar al desconectar      | ""                  |

### [battery.notify.threshold]

| Clave      | Descripción                       | Valor predeterminado |
| -------- | --------------------------------- | ------- |
| critical | Umbral crítico de batería | 10      |
| full     | Umbral de batería llena     | 90      |
| low      | Umbral de batería baja      | 20      |
| unplug   | Umbral de desconexión   | 80      |

### [brightness]

| Clave    | Descripción                                     | Valor predeterminado |
| ------ | ----------------------------------------------- | ------- |
| notify | Notificación de control de brillo                       | true    |
| steps  | Número de pasos para aumentar/disminuir brillo | 5       |

### [cava.hyprlock]

| Clave           | Descripción                                   | Valor predeterminado    |
| ------------- | --------------------------------------------- | ---------- |
| bar           | Caracteres de barra cava para hyprlock              | "▁▂▃▄▅▆▇█" |
| max_instances | Número máximo de instancias cava para hyprlock | 1          |
| range         | Número de barras cava para hyprlock              | 7          |
| standby       | Carácter de espera cava para hyprlock           | "🎶"       |
| width         | Ancho de barra cava para hyprlock                   | 20         |

### [cava.stdout]

| Clave           | Descripción                      | Valor predeterminado    |
| ------------- | -------------------------------- | ---------- |
| bar           | Caracteres de barra cava              | "▁▂▃▄▅▆▇█" |
| max_instances | Número máximo de instancias cava | 1          |
| range         | Número de barras cava              | 7          |
| standby       | Carácter de espera cava           | "🎶"       |
| width         | Ancho de barra cava                   | 20         |

### [cava.waybar]

| Clave           | Descripción                                 | Valor predeterminado    |
| ------------- | ------------------------------------------- | ---------- |
| bar           | Caracteres de barra cava para waybar              | "▁▂▃▄▅▆▇█" |
| max_instances | Número máximo de instancias cava para waybar | 1          |
| range         | Número de barras cava                         | 7          |
| standby       | Carácter de espera cava                      | "🎶"       |
| width         | Ancho de barra cava                              | 20         |

### [hypr.config]

| Clave      | Descripción                                            | Valor predeterminado               |
| -------- | ------------------------------------------------------ | --------------------- |
| sanitize | Lista de expresiones regulares para sanitizar en THEME_NAME/hypr.theme | ['.*rgba\(.*,*,*,*,'] |

### [notification]

| Clave       | Descripción                 | Valor predeterminado              |
| --------- | --------------------------- | -------------------- |
| font      | Fuente para notificaciones      | "mononoki Nerd Font" |
| font_size | Tamaño de fuente para notificaciones | 8                    |

### [rofi]

| Clave   | Descripción          | Valor predeterminado |
| ----- | -------------------- | ------- |
| scale | Escalado predeterminado de Rofi | 10      |

### [rofi.animation]

| Clave   | Descripción                         | Valor predeterminado |
| ----- | ----------------------------------- | ------- |
| scale | Configuración de 'animation.sh select' | 8       |

### [rofi.cliphist]

| Clave   | Descripción               | Valor predeterminado |
| ----- | ------------------------- | ------- |
| scale | Configuración de cliphist.sh | 8       |

### [rofi.emoji]

| Clave   | Descripción                         | Valor predeterminado |
| ----- | ----------------------------------- | ------- |
| scale | Escala de configuración de emoji-picker.sh | 8       |
| style | Estilo de configuración de emoji-picker.sh | 2       |

### [rofi.glyph]

| Clave   | Descripción                   | Valor predeterminado |
| ----- | ----------------------------- | ------- |
| scale | Configuración de glyph-picker.sh | 8       |

### [rofi.hyprlock]

| Clave   | Descripción                        | Valor predeterminado |
| ----- | ---------------------------------- | ------- |
| scale | Configuración de 'hyprlock.sh select' | 10      |

### [rofi.keybind.hint]

| Clave       | Descripción            | Valor predeterminado |
| --------- | ---------------------- | ------- |
| delimiter | Delimitador de pista de teclas | "\t"    |
| height    | Altura de pista de teclas    | "40em"  |
| line      | Línea de pista de teclas      | 16      |
| width     | Ancho de pista de teclas     | "40em"  |

### [rofi.launcher]

| Clave   | Descripción                 | Valor predeterminado |
| ----- | --------------------------- | ------- |
| scale | Configuración de rofilaunch.sh | 5       |

### [rofi.theme]

| Clave   | Descripción                  | Valor predeterminado |
| ----- | ---------------------------- | ------- |
| scale | Configuración de themeselect.sh | 6       |

### [rofi.wallpaper]

| Clave   | Descripción                    | Valor predeterminado |
| ----- | ------------------------------ | ------- |
| scale | Configuración de swwwallselect.sh | 8       |

### [screenshot]

| Clave                     | Descripción                      | Valor predeterminado |
| ----------------------- | -------------------------------- | ------- |
| annotation_post_command | Comando posterior para herramienta de anotación | [""]    |
| annotation_pre_command  | Comando previo para herramienta de anotación  | []      |
| annotation_tool         | Herramienta de anotación                  | "satty" |

### [sysmonitor]

| Clave      | Descripción                                   | Valor predeterminado |
| -------- | --------------------------------------------- | ------- |
| commands | Opciones de comando alternativo para monitor del sistema   | [""]    |
| execute  | Comando predeterminado para monitor del sistema | ""      |

### [volume]

| Clave         | Descripción                                 | Valor predeterminado |
| ----------- | ------------------------------------------- | ------- |
| boost       | Habilitar aumento de volumen                         | false   |
| boost_limit | Límite de aumento de volumen                          | 120     |
| notify      | Notificación de control de volumen                       | true    |
| steps       | Número de pasos para aumentar/disminuir volumen | 5       |

### [wallbash]

| Clave           | Descripción                            | Valor predeterminado |
| ------------- | -------------------------------------- | ------- |
| skip_template | Omite la plantilla al usar wallbash | [""]    |

### [wallpaper]

| Clave          | Descripción                            | Valor predeterminado                       |
| ------------ | -------------------------------------- | ----------------------------- |
| backend      | Backend de fondo de pantalla                      | "swww"                        |
| custom_paths | Lista de rutas para buscar fondos de pantalla | ["$HOME/Pictures/Wallpapers"] |

### [wallpaper.swww]

| Clave                | Descripción                            | Valor predeterminado |
| ------------------ | -------------------------------------- | ------- |
| duration           | Duración de transición                    | 1       |
| framerate          | Cuadros por segundo de transición                   | 60      |
| transition_default | Tipo de transición para fondo predeterminado  | "grow"  |
| transition_next    | Tipo de transición para siguiente fondo     | "grow"  |
| transition_prev    | Tipo de transición para fondo anterior | "outer" |

### [waybar]

| Clave   | Descripción          | Valor predeterminado                   |
| ----- | -------------------- | ------------------------- |
| font  | Fuente de Waybar          | "JetBrainsMono Nerd Font" |
| scale | Escalado total de Waybar | 30                        |

### [weather]

| Clave              | Descripción                                    | Valor predeterminado |
| ---------------- | ---------------------------------------------- | ------- |
| forecast_days    | Number of days to show forecast                | 3       |
| location         | Location/coordinates string for weather output | ''      |
| show_icon        | Show weather icon in waybar                    | true    |
| show_location    | Show location in waybar                        | true    |
| show_today       | Detailed description of today in tooltip       | true    |
| temperature_unit | Temperature unit                               | 'c'     |
| time_format      | Time format                                    | '24h'   |
| windspeed_unit   | Windspeed unit                                 | 'km/h'  |

### [wlogout]

| Clave   | Description   | Default |
| ----- | ------------- | ------- |
| style | Wlogout style | 2       |
