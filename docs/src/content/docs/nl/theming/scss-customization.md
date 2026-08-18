---
title: SCSS-aanpassing
description: Geavanceerde SCSS-thema-aanpassing in Tsumiki
sidebar:
  order: 3
---

| Variabele            | Standaard  | Beschrijving            |
| -------------------- | ---------- | ----------------------- |
| `$bar-background`    | themakleur | Achtergrond van de balk |
| `$bar-border-radius` | `16px`     | Hoekradius              |
| `$bar-padding`       | `4px 12px` | Interne vulling         |

| Klasse     | Effect               |
| ---------- | -------------------- |
| `compact`  | Verminderde afstand  |
| `bordered` | Rand toevoegen       |
| `pill`     | Pilvormige container |

```toml
[styling.bar]
background = "#1e1e2e"
border-radius = 16
```

Hercompileer: `./tsumiki.sh -recompile`.
