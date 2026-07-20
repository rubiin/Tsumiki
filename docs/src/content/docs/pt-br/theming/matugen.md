---
title: Tematização com Matugen
description: Gerar paletas Material You a partir do papel de parede
---

```toml
[matugen]
enabled = true
wallpaper = "~/Pictures/wallpaper.jpg"
scheme = "scheme-tonal-spot"
mode = "dark"
contrast = 0.0
```

```bash
matugen image ~/Pictures/wallpaper.jpg -t scheme-tonal-spot --mode dark
```
