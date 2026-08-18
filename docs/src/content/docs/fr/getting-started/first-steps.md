---
title: Premiers Pas
description: Que faire juste après avoir installé Tsumiki
sidebar:
  order: 3
---

Vous avez installé Tsumiki et appliqué les étapes de [Post Installation](/fr/resources/post-install). Voici comment obtenir un panneau fonctionnel rapidement.

## 1. Démarrer le Panneau

Depuis le répertoire du projet Tsumiki, exécutez :

```sh
./tsumiki.sh -start
```

Si Hyprland est en cours d'exécution, la barre devrait apparaître en haut de votre écran. Si la barre n'apparaît pas, vérifiez la sortie d'erreur dans le terminal et consultez [Dépannage](/fr/help/troubleshooting).

:::tip
Vous pouvez arrêter Tsumiki à tout moment avec :

```sh
pkill tsumiki
```

:::

## 2. Configurer le Démarrage Automatique

Ajoutez Tsumiki à votre configuration Hyprland pour qu'il se lance automatiquement à la connexion :

Ouvrez `~/.config/hypr/hyprland.conf` et ajoutez :

```sh
exec-once = sleep 5; ~/.config/tsumiki/tsumiki.sh -start
```

Le délai `sleep 5` donne le temps à Hyprland de s'initialiser complètement. Ajustez le chemin si vous avez cloné Tsumiki dans un répertoire différent.

## 3. Copier la Configuration Exemple

Tsumiki est livré avec une configuration exemple complète. Copiez-la pour obtenir un point de départ valide :

```sh
cp example/config.toml config.toml
```

:::tip
Ouvrez `example/config.toml` dans un éditeur de texte pour voir toutes les options disponibles avec documentation.
:::

## 4. Personnaliser Votre Disposition

Modifiez `config.toml` et ajustez la section `[layout]`. Chaque section (`left_section`, `middle_section`, `right_section`) est un tableau de noms de widgets :

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Cela crée une barre avec :

| Section    | Widgets                                                                     |
| ---------- | --------------------------------------------------------------------------- |
| **Gauche** | Sélecteur d'espaces de travail, titre de la fenêtre active                  |
| **Centre** | Date et heure actuelles                                                     |
| **Droite** | Contrôle du volume, état de la batterie, barre système, menu d'alimentation |

## 5. Recharger pour Appliquer les Modifications

Après avoir enregistré vos modifications, redémarrez Tsumiki :

```sh
pkill tsumiki
./tsumiki.sh -start
```

Si la configuration est valide, la barre devrait réapparaître avec votre nouvelle disposition.

## 6. Tester les Widgets Courants

Essayez d'interagir avec vos widgets :

- **Espaces de travail** — Cliquez pour changer, faites défiler pour parcourir les bureaux.
- **Volume** — Cliquez pour couper/rétablir le son, faites défiler pour ajuster.
- **Batterie** — Survolez pour voir le temps restant et l'état de charge.
- **Date/Heure** — Cliquez pour ouvrir le calendrier et le panneau de notifications.
- **Barre système** — Les icônes de la barre système devraient apparaître automatiquement.

## 7. Personnalisez-le

- **Changez les couleurs** — Voir [Création de Thèmes](/fr/theming/making-themes) pour la personnalisation SCSS ou [Matugen](/fr/theming/matugen) pour une thématisation automatique basée sur le fond d'écran.
- **Ajoutez plus de widgets** — Parcourez la [Référence des Widgets](/fr/features/widgets) pour les plus de 45 widgets disponibles.
- **Activez des modules** — Essayez le [Dock](/fr/features/modules#dock), le [Lanceur d'Applications](/fr/features/modules#lanceur-d-applications) ou l'[OSD](/fr/features/modules#osd-affichage-à-l-écran).
- **Configurez le comportement** — Voir la référence complète de [Configuration](/fr/configuring/config) pour chaque option.

## Dépannage

Si quelque chose semble incorrect :

- **La barre n'apparaît pas** — Vérifiez que vous exécutez Hyprland et qu'aucune autre barre n'est en cours d'exécution (`pkill waybar`).
- **Pas d'icônes** — Vérifiez que [JetBrains Nerd Font](https://www.nerdfonts.com) est installée et configurée comme police de votre terminal/UI.
- **Fonctionnalité manquante** — Certains widgets nécessitent des outils externes (ex., `playerctl` pour les médias, `brightnessctl` pour la luminosité). Exécutez `./tsumiki.sh -setup` pour vous assurer que toutes les dépendances sont installées (les dépendances Python sont installées avec `uv sync`).
- **Erreurs SASS** — Votre `config.toml` peut être invalide. Comparez-le avec `example/config.toml`.

Pour plus d'aide, consultez les pages [FAQ](/fr/help/faq) ou [Dépannage](/fr/help/troubleshooting).
