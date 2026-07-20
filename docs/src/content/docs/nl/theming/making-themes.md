---
title: Thema's Maken
description: Hoe u thema's maakt voor Tsumiki
---

Maak uw themabestand in `themes/` met de extensie `.toml`.

```bash
touch themes/mijn-thema.toml
```

## Minimaal Thema

```toml
[dark.background]
main = "#121212"
alt = "#1a1a1a"

[dark.text]
main = "#e0e0e0"
secondary = "#c5c5c5"

[dark.accent]
blue = "#00d0ff"
green = "#00ff00"

[light.background]
main = "#ededed"

[light.text]
main = "#1f1f1f"
```

## Thema inschakelen

```toml
[styling]
theme_name = "mijn-thema"
```
