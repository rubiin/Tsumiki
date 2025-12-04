---
title: Theming with Matugen
description: Making Tsumiki use Matugen to generate Material You color palettes from images
---

This explains how Tsumiki integrates with Matugen to generate Material You color palettes from a wallpaper or image, and how to control it.

Add a `matugen` section to your `theme.json` (or edit the existing one). Example:

```json
"matugen": {
  "enabled": true,
  "wallpaper": "~/Pictures/wallpaper.jpg",
  "scheme": "scheme-tonal-spot",
  "mode": "dark",
  "contrast": 0.0,
  "quiet": true
}
```

Fields

- `enabled` (bool): If true, Tsumiki will attempt to generate a palette at startup when the service is available.
- `wallpaper` (string): Path to the image used to extract colors. Can be an absolute path or `~` expansion.
- `scheme` (string): Matugen scheme identifier. Common choices:
  - `scheme-tonal-spot` (default)
  - `scheme-content`
  - `scheme-expressive`
  - `scheme-fidelity`
  - `scheme-fruit-salad`
  - `scheme-monochrome`
  - `scheme-neutral`
  - `scheme-rainbow`
- `mode` (string): `dark` or `light` output mode.
- `contrast` (float): Contrast adjustment between -1.0 and 1.0.
- `quiet` (bool): If true, runs Matugen with `-q` to reduce stdout noise.

Config file

Tsumiki ships a Matugen config template at `assets/matugen/config.toml`. The service uses `~/.config/tsumiki/assets/matugen/config.toml` by default. If you want a custom config file, edit that path in the service or copy the template and adjust it.

Running Matugen

- Automatic: When `matugen.enabled` is true, Tsumiki's startup code will call the Matugen service and generate the palette before compiling CSS.

- Manual (shell): You can run Matugen directly from the command line (Matugen must be installed):

```bash
matugen image -q ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml
```

- Manual (from inside Tsumiki/python): use the service exposed by the app (when running inside the Tsumiki environment):

```python
from services.matugen import MatugenService
mat = MatugenService()
mat.generate_sync('/home/user/Pictures/wallpaper.jpg')
# or
mat.generate('/home/user/Pictures/wallpaper.jpg')  # async
```

Troubleshooting

- Ensure the `matugen` binary is installed and on `PATH`.
- Ensure the `wallpaper` path exists and is accessible.
- If you see caching or stale values, restart Tsumiki to force regeneration.
- If you get import/cache issues after code edits, remove `*.pyc` and `__pycache__` directories and restart.

Notes

- Matugen produces color variables that are consumed by `styles/theme.scss` when Tsumiki compiles CSS. Editing the Matugen config or wallpaper requires regenerating the palette and recompiling CSS.
- The service emits signals (`colors_generated` and `generation_failed`) that other parts of Tsumiki can listen to for live updates.

Examples

1) Quick one-liner (generate and recompile CSS manually):

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark --contrast 0.0 --config ~/.config/tsumiki/assets/matugen/config.toml && ./init.sh -recompile
```

2) Interactive (Python REPL within Tsumiki venv):

```py
from services.matugen import MatugenService
m = MatugenService()
m.generate_sync('~/Pictures/wallpaper.jpg')
```

That's it — enable `matugen` in `theme.json`, ensure `matugen` is installed, and Tsumiki will pick up the generated palette on startup or when you trigger the service manually.
