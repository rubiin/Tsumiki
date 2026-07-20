---
title: Themes erstellen
description: So erstellen Sie Themes für Tsumiki
---

Erstellen Sie Ihre Theme-Datei in `themes/` mit der Erweiterung `.toml`.

```bash
touch themes/mein-theme.toml
```

## Minimales Theme

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

## Theme aktivieren

```toml
[styling]
theme_name = "mein-theme"
```

## Variablengruppen

- `background*`: Panel- und Popup-Hintergründe
- `text*`: Lesbarkeit und Hervorhebung
- `surface*`: Karten, Buttons, Hover-Zustände
- `accent*`: Semantische Farben für Aktionen
