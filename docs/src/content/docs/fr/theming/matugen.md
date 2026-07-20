---
title: Thématisation avec Matugen
description: Utiliser Matugen pour générer des palettes Material You
---

Tsumiki peut utiliser Matugen pour générer une palette Material You depuis votre fond d'écran.

```toml
[matugen]
enabled = true
wallpaper = "~/Pictures/wallpaper.jpg"
scheme = "scheme-tonal-spot"
mode = "dark"
contrast = 0.0
```

## Champs

- `enabled` : générer la palette au démarrage
- `wallpaper` : chemin vers l'image source
- `scheme` : schéma Matugen (`scheme-tonal-spot`, `scheme-content`, `scheme-expressive`, etc.)
- `mode` : `dark` ou `light`
- `contrast` : entre `-1.0` et `1.0`

## Utilisation

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark
```
