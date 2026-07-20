---
title: Theming mit Matugen
description: Material You-Farbpaletten aus Ihrem Hintergrundbild generieren
---

Tsumiki kann Matugen verwenden, um eine Material You-Palette aus Ihrem Hintergrundbild zu generieren.

```toml
[matugen]
enabled = true
wallpaper = "~/Pictures/wallpaper.jpg"
scheme = "scheme-tonal-spot"
mode = "dark"
contrast = 0.0
```

## Felder

- `enabled`: Palette beim Start generieren
- `wallpaper`: Pfad zum Bild (unterstützt `~`)
- `scheme`: Matugen-Schema (`scheme-tonal-spot`, `scheme-content`, `scheme-expressive`, etc.)
- `mode`: `dark` oder `light`
- `contrast`: zwischen `-1.0` und `1.0`

## Verwendung

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark
```
