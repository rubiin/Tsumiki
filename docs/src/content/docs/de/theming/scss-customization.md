---
title: SCSS-Anpassung
description: Erweiterte SCSS-Theme-Anpassung in Tsumiki
sidebar:
  order: 3
---

## Wie SCSS funktioniert

Tsumiki kompiliert SCSS aus `styles/main.scss` mit `dart-sass` in CSS.

### Leistenvariablen

| Variable             | Standard    | Beschreibung           |
| -------------------- | ----------- | ---------------------- |
| `$bar-background`    | Themenfarbe | Hintergrund der Leiste |
| `$bar-border-radius` | `16px`      | Eckenradius            |
| `$bar-padding`       | `4px 12px`  | Innenabstand           |
| `$bar-margin`        | `0 8px`     | Außenabstand           |

### Anpassung über config.toml

```toml
[styling.bar]
background = "#1e1e2e"
border-radius = 16
padding = "4px 12px"
```

### Integrierte Style-Klassen

| Klasse     | Effekt                   |
| ---------- | ------------------------ |
| `compact`  | Reduzierter Abstand      |
| `bordered` | Rahmen hinzufügen        |
| `pill`     | Pillenförmiger Container |

### Benutzerdefiniertes CSS

Erstellen Sie `styles/custom.scss` und importieren Sie es in `styles/main.scss`:

```scss
@use "custom.scss";
```

Kompilieren: `./tsumiki.sh -recompile`.
