---
title: Création de Thèmes
description: Comment créer des thèmes pour Tsumiki
---

Créez votre fichier de thème dans `themes/` avec une extension `.toml`.

```bash
touch themes/mon-theme.toml
```

## Thème Minimum

```toml
[dark.background]
main = "#121212"
alt = "#1a1a1a"
dark = "#0a0a0a"

[dark.text]
main = "#e0e0e0"
secondary = "#c5c5c5"
muted = "#8e8e8e"

[dark.accent]
blue = "#00d0ff"
green = "#00ff00"
red = "#ff1744"
purple = "#9c00ff"

[light.background]
main = "#ededed"
alt = "#e5e5e5"

[light.text]
main = "#1f1f1f"
secondary = "#3a3a3a"
```

## Activer Votre Thème

```toml
[styling]
theme_name = "mon-theme"
```

## Groupes de Variables

- `background*` : fonds du panneau et des popups
- `text*` : lisibilité du contenu
- `surface*` : cartes, boutons, états de survol
- `accent*` : couleurs sémantiques pour les actions
