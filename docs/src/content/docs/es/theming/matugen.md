---
title: Tematización con Matugen
description: Hacer que Tsumiki use Matugen para generar paletas de colores Material You desde imágenes
---

Tsumiki puede usar Matugen para generar una paleta Material You desde tu fondo de pantalla.

Añade o actualiza esta sección en `config.toml` bajo styling:

```toml
[matugen]
enabled = true
wallpaper = "~/Pictures/wallpaper.jpg"
scheme = "scheme-tonal-spot"
mode = "dark"
contrast = 0.0
```

## Campos

- `enabled` (`bool`): generar paleta al inicio cuando sea posible.
- `wallpaper` (`string`): ruta a la imagen fuente. Soporta `~`.
- `scheme` (`string`): identificador de esquema de Matugen. Valores comunes:
  - `scheme-tonal-spot` (predeterminado)
  - `scheme-content`
  - `scheme-expressive`
  - `scheme-fidelity`
  - `scheme-fruit-salad`
  - `scheme-monochrome`
  - `scheme-neutral`
  - `scheme-rainbow`
- `mode` (`string`): `dark` o `light`.
- `contrast` (`float`): entre `-1.0` y `1.0`.

## Ruta de Plantilla de Configuración

Tsumiki incluye una plantilla en `assets/matugen/config.toml`.
Por defecto, el servicio usa:

`~/.config/tsumiki/assets/matugen/config.toml`

Si necesitas comportamiento personalizado, copia ese archivo y ajústalo.

## Ejecutar Matugen

- Automático: Cuando `matugen.enabled = true`, Tsumiki ejecuta Matugen durante el inicio.

- Manual (shell):

```bash
matugen image -q ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml
```

- Manual (servicio Python):

```python
from services.matugen import MatugenService

mat = MatugenService()
mat.generate_sync("/home/user/Pictures/wallpaper.jpg")
# o
mat.generate("/home/user/Pictures/wallpaper.jpg")  # asíncrono
```

## Solución de Problemas

- Asegúrate de que el binario `matugen` esté instalado y en `PATH`.
- Asegúrate de que la ruta `wallpaper` exista y sea accesible.
- Si los colores se ven desactualizados, reinicia Tsumiki y regenera.
- Si las importaciones/caché se vuelven inconsistentes después de ediciones locales, limpia `*.pyc` y `__pycache__`.

## Notas

Matugen produce variables de color consumidas por `styles/theme.scss` durante la compilación CSS.
Cuando cambies el fondo de pantalla o la configuración de Matugen, regenera y recompila los estilos.

## Ejemplo Rápido

Genera paleta y recompila en un solo comando:

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml && ./init.sh -recompile
```

Interactivo (REPL de Python dentro del entorno de Tsumiki):

```py
from services.matugen import MatugenService

m = MatugenService()
m.generate_sync("~/Pictures/wallpaper.jpg")
```

Activa `matugen` bajo styling en `config.toml`, asegúrate de que `matugen` esté instalado, y Tsumiki generará colores al inicio o cuando ejecutes el servicio manualmente.
