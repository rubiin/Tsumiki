---
title: Aperçu
description: Qu'est-ce que Tsumiki, prérequis et concepts clés
sidebar:
  order: 1
---

## Qu'est-ce que Tsumiki ?

Tsumiki (anciennement Hydepanel) est une barre d'état modulaire pour le compositeur Wayland [Hyprland](https://hyprland.org). Construit sur le système de widgets [Fabric](https://github.com/Fabric-Development/fabric), il offre une architecture flexible pour créer des panneaux de bureau personnalisés grâce à des widgets composites.

Le nom **Tsumiki** (積み木) signifie "blocs de construction" en japonais — reflétant la conception modulaire et empilable du projet.

## Prérequis

Avant d'installer Tsumiki, assurez-vous que votre système répond à ces exigences :

| Exigence | Remarques |
|---|---|
| [Hyprland](https://hyprland.org) | Une installation fonctionnelle d'Hyprland est requise |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Nécessaire pour le rendu des icônes et glyphes |
| **Python 3.12+** | Tsumiki cible Python 3.12 |
| **uv** | Gestionnaire de paquets Python utilisé pour installer les dépendances (`uv sync`) |
| **Arch Linux** (recommandé) | Paquets optimisés pour Arch ; autres distributions peuvent nécessiter une configuration manuelle |
| **NetworkManager** | Requis pour les widgets et services réseau |
| **PipeWire** | Requis pour les widgets audio et l'OSD |

## Concepts Clés

### Widgets

Les widgets sont les blocs de construction individuels qui apparaissent dans la barre. Plus de 45 widgets intégrés couvrent :

- **Infos système** — CPU, mémoire, GPU, stockage, utilisation réseau
- **Contrôle matériel** — Volume, luminosité, microphone, batterie
- **Gestion du bureau** — Espaces de travail, titre de fenêtre, barre des tâches
- **Utilitaires** — Capture d'écran, OCR, presse-papiers, enregistrement d'écran
- **Productivité** — Minuterie Pomodoro, tableau Kanban, chronomètre, sélecteur d'emoji
- **Intégration** — Météo, contrôles média, compagnon Git, commutateur DNS

Chaque widget est configuré sous `[widgets.<nom>]` dans `config.toml`. Voir la [Référence des Widgets](/fr/features/widgets) pour la liste complète.

### Modules

Les modules sont des surfaces d'interface plus grandes qui vont au-delà de la barre — ce sont des fenêtres ou des superpositions autonomes :

- **Barre** — Le panneau principal lui-même
- **Système de notifications** — Affichage des notifications du bureau
- **Dock** — Dock d'applications avec intellihide
- **Vue d'ensemble** — Exposé des espaces de travail en plein écran
- **Lanceur d'applications** — Recherche d'applications pilotée par le clavier
- **OSD** — Affichages à l'écran pour le volume, la luminosité, etc.
- **Horloge de bureau** — Superposition d'horloge décorative
- **Citations de bureau** — Affichage de citations inspirantes

Les modules sont configurés sous `[modules.<nom>]` dans `config.toml`. Voir la [Référence des Modules](/fr/features/modules) pour les détails.

### Disposition

Le placement des widgets dans la barre est contrôlé par la section `[layout]` de `config.toml` :

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Les widgets peuvent également être regroupés ou placés dans des groupes pliables. Voir [Configuration](/fr/configuring/config) pour les détails.

### Services

Les services sont des processus d'arrière-plan qui fournissent des données aux widgets — ils surveillent les niveaux de batterie, l'état du réseau, les lecteurs multimédias, la météo et plus encore. Les widgets se connectent aux services via des signaux GTK, ce qui maintient les mises à jour efficaces.

## Architecture

L'architecture de Tsumiki suit une conception en couches :

```text
┌──────────────────────────────────────────────┐
│                  main.py                       │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│   │ Config    │  │ CSS      │  │ Module     │  │
│   │ Loader   │  │ Compiler │  │ Init       │  │
│   └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────┬────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Services │  │ Widgets  │  │ Modules  │
  │ (DBus,   │──▶│ (Panel   │──▶│ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **Services** s'exécutent en arrière-plan et émettent des signaux GTK lors des changements d'état
- **Widgets** sont des boutons du panneau qui s'abonnent aux signaux des services
- **Modules** sont des fenêtres GTK autonomes pour les superpositions et les popups

Voir la page [Architecture](/fr/resources/architecture) pour un aperçu plus approfondi.

## Parcours Recommandé

1. **[Installer Tsumiki](/fr/getting-started/installation)** — Cloner, installer les dépendances, configurer l'environnement.
2. **Suivre [Premiers Pas](/fr/getting-started/first-steps)** — Démarrer la barre, configurer la disposition, appliquer les règles post-installation.
3. **Apprendre [Configuration](/fr/configuring/config)** — Comprendre la structure de configuration TOML et les options disponibles.
4. **Choisir un thème** — Commencer avec un thème intégré ou créer le vôtre avec [Création de Thèmes](/fr/theming/making-themes).
5. **Explorer** — Ajouter des widgets, activer des modules, personnaliser le comportement.

## Besoin d'Aide ?

- Consultez la [FAQ](/fr/help/faq) pour les problèmes courants.
- Visitez [Dépannage](/fr/help/troubleshooting) pour des conseils de débogage.
- Rejoignez le [Discord](https://discord.gg/8nWbDC4SnP) pour le support communautaire.
