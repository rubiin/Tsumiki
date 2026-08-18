---
title: Personnalisation SCSS
description: Personnalisation avancée des thèmes SCSS dans Tsumiki
sidebar:
  order: 3
---

## Comment fonctionne SCSS

Tsumiki compile SCSS depuis `styles/main.scss` en CSS via `dart-sass`.

### Variables de barre

| Variable             | Défaut           | Description         |
| -------------------- | ---------------- | ------------------- |
| `$bar-background`    | couleur du thème | Fond de la barre    |
| `$bar-border-radius` | `16px`           | Coins arrondis      |
| `$bar-padding`       | `4px 12px`       | Remplissage interne |
| `$bar-margin`        | `0 8px`          | Marge externe       |

### Personnalisation depuis config.toml

```toml
[styling.bar]
background = "#1e1e2e"
border-radius = 16
padding = "4px 12px"
```

### Classes de style intégrées

| Classe     | Effet                        |
| ---------- | ---------------------------- |
| `compact`  | Remplissage réduit           |
| `bordered` | Ajoute une bordure           |
| `pill`     | Conteneur en forme de pilule |

### CSS personnalisé

Créez `styles/custom.scss` et importez-le dans `styles/main.scss` :

```scss
@use "custom.scss";
```

Recompilez : `./init.sh -recompile`.
