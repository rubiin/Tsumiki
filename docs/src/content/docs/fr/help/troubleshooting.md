---
title: Dépannage
description: Diagnostiquer et résoudre les problèmes courants de Tsumiki
---

Cette page couvre les problèmes au-delà de la [FAQ](/fr/help/faq).

## Le Panneau N'Apparaît Pas

1. Assurez-vous qu'Hyprland est en cours d'exécution et que les règles de couche de [Post Installation](/fr/resources/post-install) sont appliquées.
2. Tuez toute barre conflictuelle : `pkill nom-barre`.
3. Démarrez Tsumiki : `tsu -start` et surveillez la sortie du journal.

## Widget Manquant

- Confirmez que le widget est activé dans `config.toml` sous `[widgets.<nom>]`.
- Vérifiez que le widget est listé dans une section `layout`.
- Vérifiez `ModuleNotFoundError` et installez les dépendances avec `tsu -setup`.

## Le Thème Ne S'Applique Pas

- Confirmez que `theme_name` dans `config.toml` correspond à un fichier dans `themes/`.
- Recompilez les styles : `./init.sh -recompile`.
- Pour Matugen, consultez [Thématisation avec Matugen](/fr/theming/matugen).

## CPU ou Mémoire Élevée

- Réduisez les intervalles de sondage dans la configuration des widgets.
- Désactivez les widgets et modules inutilisés.
- Activez `auto_hide` pour réduire les rafraîchissements.

## Toujours Bloqué ?

Ouvrez un ticket avec votre `config.toml` et les journaux de `tsu -start`.
