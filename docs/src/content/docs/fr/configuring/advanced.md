---
title: Configuration Avancée
description: Modèles de configuration avancée de Tsumiki
---

Une fois que vous êtes à l'aise avec les bases de la [Configuration](/fr/configuring/config), ces modèles vous aident à affiner Tsumiki davantage.

## Groupes de Widgets

Regroupez les widgets avec un espacement et un style partagés :

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

Référencez un groupe dans votre disposition avec `@group:N` (index basé sur zéro) :

```toml
[layout]
right_section = ["@group:0", "system_tray"]
```

## Groupes Pliables

Cachez les widgets moins utilisés derrière un bouton :

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "Outils utilitaires"
style_classes = ["utility-tools"]
```

## Multi-Moniteur

Activez les panneaux par moniteur :

```toml
[general]
multi_monitor = true
```

## Masquage Automatique

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

## Modules Personnalisés

Ajoutez votre propre module sous `modules` et référencez-le depuis `layout`. Gardez les modifications petites et redémarrez avec `./init.sh -start` pour valider.
