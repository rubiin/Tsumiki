---
title: Conseils de Thématisation
description: Conseils pratiques de thématisation pour Tsumiki
---

Conseils pour tirer le meilleur parti de [Création de Thèmes](/fr/theming/making-themes) et [Matugen](/fr/theming/matugen).

## Gardez un Contraste Élevé

Le texte doit rester lisible sur toutes les surfaces : barre, popups, notifications, paramètres rapides.

## Testez les Surfaces Courantes

Vérifiez au minimum : barre principale, popup des paramètres rapides, notification toast, lanceur et dock.

## Utilisez des Accents Sémantiques

Réservez les couleurs fortes `accent*` pour les états importants (erreurs, succès, espace de travail actif).

## Flux de Travail Matugen

1. Définissez `matugen.enabled = true` dans `config.toml`.
2. Pointez `wallpaper` vers votre image.
3. Redémarrez Tsumiki pour générer la palette.
4. Recompilez les styles si nécessaire : `./init.sh -recompile`.

## Apprenez des Thèmes Existants

Parcourez `styles/themes/` pour des références comme `nord.scss`, `dracula.scss` et `gruvbox.scss`.
