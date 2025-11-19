---
title: Creación de Temas
description: Cómo crear temas para HyDE
---

Aquí te guiaremos a través del proceso de creación de temas para HyDE paso a paso.
Este tutorial funcionará tanto para hyprdots como para HyDE.

### Guía de Inicio Rápido

Clona el repositorio hyde-theme-starter en tu directorio de temas

:::tip
Renombra `MyTheme` al nombre de tu tema, asegúrate de que no entre en conflicto con los nombres en [HyDE-Gallery](https://github.com/HyDE-Project/hyde-gallery)
:::

```bash
git clone https://github.com/richen604/hyde-theme-starter ~/MyTheme
```

1. Componentes requeridos - todos deben estar en formato `tar.*`:

   - Un tema GTK (obligatorio)
     - busca en [Gnome-Look Themes](https://www.gnome-look.org/browse?cat=135&ord=latest) para temas existentes
     - o consulta [Generar GTK4](#generate-gtk4-from-wallbash) para generar un tema GTK a partir del fondo de pantalla
   - Paquete de iconos (opcional) - por defecto es Tela-circle
     - busca en [Gnome-Look Icons](https://www.gnome-look.org/browse?cat=132&ord=latest) para paquetes de iconos existentes
   - Tema de cursor (opcional) - por defecto es Bibata-Modern-Ice
     - busca en [Gnome-Look Cursors](https://www.gnome-look.org/browse?cat=107&ord=latest) para temas de cursor existentes
   - Fuente (opcional)
     - busca en [fonts.google.com](https://fonts.google.com/) para fuentes web
     - busca en [nerdfonts.com](https://www.nerdfonts.com/) para fuentes de desarrollador parcheadas

2. Una colección de fondos de pantalla que coincidan con tu estilo/esquema de colores deseado

   - [Wallhaven](https://wallhaven.cc/) - Para fondos de pantalla
   - [farbenfroh.io](https://farbenfroh.io/) - Para fondos de pantalla con coincidencia de color si tienes en mente un esquema de colores específico
   - No agregues demasiados fondos de pantalla, 8-10 es un buen número

3. Instala `just` para ejecutar scripts de ayuda `yay -S just`

Ve a tu directorio de tema `cd ~/MyTheme` (reemplaza `MyTheme` con el nombre de tu tema)

:::tip
Renombra `MyTheme` en el archivo `justfile` al nombre de tu tema
:::

```bash
theme = "MyTheme"
```

Ejecuta `just init` para generar la estructura inicial de directorios

Tu tema debería tener la siguiente estructura:

```bash
~/MyTheme/
├── Config/                  # Parte de tu tema final - Archivos de configuración
│   └── hyde/
│       └── themes/
│           └── MyTheme/     # directorio principal del tema
│               └── wallpapers/
├── refs/                    # para archivos de referencia que generamos
├── screenshots/             # para capturas de pantalla de tu tema
├── Source/                  # Parte de tu tema final - Arcs es decir, gtk, cursor, icono, fuente
│   └── arcs/
├── .gitignore
├── justfile                 # para ejecutar scripts de ayuda
└── README.md                # enlaces a esta página web
```

### Arcs

Los Arcs son los componentes de tema GTK, icono, cursor y fuente que conforman partes de tu tema.
Agreguemos estos de inmediato al directorio `Source/arcs` para que estén listos para pruebas.

La estructura de tu carpeta debería verse algo así:

```bash
~/MyTheme/
├── Source/
│   └── arcs/
│       ├── Gtk_<Tu-Tema-GTK>.tar.*
│       ├── Cursor_<Tu-Tema-Cursor>.tar.*
│       └── Icon_<Tu-Tema-Icono>.tar.*
│       └── Font_<Tu-Nombre-Fuente>.tar.*
```

**Asegúrate de usar el prefijo correcto para cada arc**. Ej. `Gtk_<Tu-Tema-GTK>.tar.*`

### Ver tu tema con Wallbash

Copia tus fondos de pantalla a tu directorio de tema

```bash
cp -r ~/wallpapers ~/MyTheme/Config/.config/hyde/themes/MyTheme/wallpapers
```

Entra en tu directorio de tema

```bash
cd ~/MyTheme
```

Instala tu tema

```bash
just install
```

### Probar tu tema con wallbash

Hay dos formas de inicializar tu tema. Desde wallbash o desde un tema existente.

Vamos a usar wallbash para esta guía, ya que te da una buena comprensión de cómo wallbash genera los colores para tu tema. Puedes aprender más sobre wallbash [aquí](#understanding-wallbash).

Abre Wallbash, configurando auto, oscuro o claro (`Meta + Shift + R`). </br>
Establece tu fondo de pantalla elegido como el fondo de pantalla actual (`Meta + Shift + W`)

Observa cómo wallbash adapta los colores a tu fondo de pantalla para las siguientes aplicaciones:

- GTK (nwg-look)
  - para probar tu tema arc gtk, cambia del modo wallbash al modo tema (Meta + Shift + R)
  - luego verifica `pavucontrol` para ver si tu tema gtk se ve extraño. Si es así, sigue las instrucciones en [Generar GTK4](#generate-gtk4-from-wallbash) para generar archivos de tema GTK4 usando wallbash
- Kitty (kitty)
- QT (qt5ct + qt6ct)
- Waybar (waybar)
- Spotify (spotify)
- VSCode (code) - necesita wallbash habilitado como tema de color
- Cava (cava)

### Generar archivos de tema

Asegúrate de que el fondo de pantalla que elegiste sea el mejor fondo de pantalla que wallbash genere para tu tema. </br>
Ahora ejecuta los siguientes comandos para generar los archivos wallbash.

```bash
just gen-all
just set-wall
```

Verás un montón de nuevos archivos en el directorio `refs` de tu tema.

```bash
~/MyTheme/
├── refs/                   # para archivos de referencia que generamos
│   ├── gtk-4.0/            # archivos de tema GTK4
│   │   ├── gtk.css         # Tema claro
│   │   └── gtk-dark.css    # Tema oscuro
│   ├── kvantum/            # archivos de tema Kvantum
│   │   ├── kvantum.theme   # Configuración del tema Kvantum
│   │   └── kvconfig.theme  # Configuración de Kvantum
│   ├── hypr.theme          # Tema Hyprland
│   ├── kitty.theme         # Tema de terminal Kitty
│   ├── rofi.theme          # Tema Rofi
│   ├── theme.dcol          # anulaciones del modo "tema" de wallbash
│   └── waybar.theme        # Tema Waybar
│   └── wall.set            # Primer fondo de pantalla que usa el tema
```

Puedes copiar todos los archivos a tu directorio `Config/.config/hyde/themes/MyTheme`.

```bash
cp -r ./refs/* ./Config/.config/hyde/themes/MyTheme
```

Ejecuta install nuevamente para actualizar tu tema

```bash
just install
```

Estos archivos se utilizan para configurar el modo "tema" para tu tema. (`Meta + Shift + R`)

### Editar archivos \*.theme

Estos archivos son importantes para que los temas funcionen correctamente.

Deberías tomar como referencia un tema como [Bad Blood](https://github.com/HyDE-Project/hyde-gallery/blob/Bad-Blood/Configs/.config/hyde/themes/Bad%20Blood) junto con esta guía.

Cada archivo \*.theme contiene líneas de configuración

La primera línea tiene el formato: ruta_archivo | comando_a_ejecutar

- hypr.theme - `$HOME/.config/hypr/themes/theme.conf|> $HOME/.config/hypr/themes/colors.conf`
- kitty.theme - `$HOME/.config/kitty/theme.conf|killall -SIGUSR1 kitty`
- rofi.theme - `$HOME/.config/rofi/theme.rasi`
- waybar.theme - `$HOME/.config/waybar/theme.css|${scrDir}/wbarconfgen.sh`

el archivo más importante es `hypr.theme`

```bash
$HOME/.config/hypr/themes/theme.conf|> $HOME/.config/hypr/themes/colors.conf
# ~/.config/hypr/theme/theme.conf es un archivo generado automáticamente. No lo edites.

$GTK_THEME=Bad-Blood # nombre de carpeta dentro de `Source/arcs/Gtk_<Tu-Tema-GTK>.tar.*`
$ICON_THEME=besgnulinux-mono-red # nombre de carpeta dentro de `Source/arcs/Icon_<Tu-Tema-Icono>.tar.*`
$COLOR_SCHEME=prefer-dark # prefer-dark, prefer-light, o auto
$CURSOR_THEME=Night-Diamond-Red # nombre de carpeta dentro de `Source/arcs/Cursor_<Tu-Tema-Cursor>.tar.*`
$CURSOR_SIZE=30 # tamaño del cursor en píxeles
```

- Edita las variables para arcs, deben coincidir con el nombre de la carpeta **dentro** de cada arc en `Source/arcs` como se muestra arriba
- Configura bordes de hyprland, colores y otras configuraciones relacionadas con el tema
- Puedes usar hypr.theme para configurar programas adicionales para tu tema, como el tema SDDM o Vscode
- Se convierte en `$HOME/.config/hypr/themes/theme.conf`

Cualquier actualización a tu tema, ya sea en `Config` o `Source`, debe ejecutarse con `just install` para actualizar tu tema.

### Editar theme.dcol

El archivo `theme.dcol` se utiliza para anular algunos colores de wallbash generados para los modos wallbash.
Consulta [entendiendo wallbash](#understanding-wallbash) para obtener más información.

Este archivo es completamente opcional

### Finalizar tu tema

¡Tu tema ahora debería estar listo para ser agregado a hyde-gallery!

Algunos toques finales más:

- Agrega algunas capturas de pantalla a `~/screenshots`
- Agrega tu tema a Hyde-Gallery

### Agregar Temas a Hyde-Gallery

En tu directorio de tema, genera el archivo readme usando

```bash
python3 generate_readme.py
```

Inicializa git

```bash
git init && git branch -M main && git add . && git commit -m "Mi primer tema HyDE"
```

[crea un repositorio de github](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

```bash
git remote add origin <url-de-tu-repo>
git push -u origin main
```

Haz un fork de hyde-gallery <https://github.com/HyDE-Project/hyde-gallery> </br>
Agrega tu tema a la lista y a `hyde-themes.json`

## Más Información

### Generar GTK4 desde wallbash

Si tu tema no incluye soporte para GTK4, pavucontrol y otras aplicaciones GTK4 pueden aparecer con un tema blanco simple.

Ejecuta el siguiente comando para generar los archivos de tema GTK4

```bash
just gen-gtk4
```

Copia el directorio `refs/gtk-4.0` a tu directorio de tema

```bash
mkdir -p ./Config/.config/hyde/themes/MyTheme/gtk-4.0
cp -r ./refs/gtk-4.0/* ./Config/.config/hyde/themes/MyTheme/gtk-4.0/
```

### Entendiendo wallbash

Wallbash genera 4 colores primarios a partir de tu fondo de pantalla, luego crea grupos de colores alrededor de cada color primario con la siguiente estructura:

Para cada color primario (`wallbash_pry1` a `wallbash_pry4`):

- Color de texto (`wallbash_txt1` a `wallbash_txt4`)
- 9 colores de acento (`wallbash_1xa1` a `wallbash_1xa9` para el grupo 1, etc.)

Cada color tiene una variante RGBA con opacidad configurable (por ejemplo, `wallbash_pry1_rgba(0.95)`)

Total: 44 colores base (4 grupos × 11 colores) más variantes RGBA

Usa `just gen-dcol` para generar un `theme.dcol` con todos los colores generados por wallbash para tu fondo de pantalla activo como referencia
