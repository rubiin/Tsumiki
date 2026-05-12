---
title: Theming with Matugen
description: Making Tsumiki use Matugen to generate Material You color palettes from images
---

Tsumiki can use Matugen to generate a Material You palette from your wallpaper.

Add or update this section in `theme.toml`:

```toml
[matugen]
enabled = true
wallpaper = "~/Pictures/wallpaper.jpg"
scheme = "scheme-tonal-spot"
mode = "dark"
contrast = 0.0
```

## Fields

- `enabled` (`bool`): generate palette on startup when possible.
- `wallpaper` (`string`): path to image source. Supports `~`.
- `scheme` (`string`): Matugen scheme identifier. Common values:
  - `scheme-tonal-spot` (default)
  - `scheme-content`
  - `scheme-expressive`
  - `scheme-fidelity`
  - `scheme-fruit-salad`
  - `scheme-monochrome`
  - `scheme-neutral`
  - `scheme-rainbow`
- `mode` (`string`): `dark` or `light`.
- `contrast` (`float`): between `-1.0` and `1.0`.

## Config Template Path

Tsumiki ships a template at `assets/matugen/config.toml`.
By default, the service uses:

`~/.config/tsumiki/assets/matugen/config.toml`

If you need custom behavior, copy that file and adjust it.

## Running Matugen

- Automatic: When `matugen.enabled = true`, Tsumiki runs Matugen during startup.

- Manual (shell):

```bash
matugen image -q ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml
```

- Manual (Python service):

```python
from services.matugen import MatugenService
mat = MatugenService()
mat.generate_sync('/home/user/Pictures/wallpaper.jpg')
# or
mat.generate('/home/user/Pictures/wallpaper.jpg')  # async
```

## Troubleshooting

- Ensure the `matugen` binary is installed and on `PATH`.
- Ensure the `wallpaper` path exists and is accessible.
- If colors look stale, restart Tsumiki and regenerate.
- If imports/cache become inconsistent after local edits, clear `*.pyc` and `__pycache__`.

## Notes

Matugen produces color variables consumed by `styles/theme.scss` during CSS compilation.
When you change wallpaper or Matugen config, regenerate and recompile styles.

## Quick Example

Generate palette and recompile in one command:

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml && ./init.sh -recompile
```

Interactive (Python REPL within Tsumiki environment):

```py
from services.matugen import MatugenService
m = MatugenService()
m.generate_sync('~/Pictures/wallpaper.jpg')
```

Enable `matugen` in `theme.toml`, ensure `matugen` is installed, and Tsumiki will generate colors on startup or when you run the service manually.
