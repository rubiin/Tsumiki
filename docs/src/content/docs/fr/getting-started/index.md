---
title: Démarrage Rapide
description: Mettez Tsumiki en service en quelques minutes
---

Tsumiki est une barre d'état modulaire pour Hyprland construite sur le système de widgets Fabric.

## Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Hyprland** — une installation fonctionnelle d'Hyprland
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` doit afficher 3.12 ou supérieur
- **uv** — Gestionnaire de paquets Python utilisé pour installer les dépendances (`uv sync`)

## Installation Rapide

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./tsumiki.sh -setup
./tsumiki.sh -start
```

Le drapeau `-setup` installe tous les paquets système nécessaires et les dépendances Python. Votre mot de passe peut vous être demandé pendant la configuration.

Pour d'autres méthodes d'installation (script bootstrap, configuration manuelle), consultez le [guide d'installation complet](/fr/getting-started/installation).

## Démarrage Automatique

Ajoutez cette ligne à `~/.config/hypr/hyprland.conf` :

```sh
exec-once = sleep 5; ~/.config/tsumiki/tsumiki.sh -start
```

## Configuration Minimale

Voici un `config.toml` minimal pour commencer :

```toml
"$schema" = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

Après avoir enregistré, redémarrez la barre :

```sh
pkill tsumiki
./tsumiki.sh -start
```

## Prochaines Étapes

<CardGrid stagger>
  <Card title="Premiers Pas" icon="rocket">
    Configurez votre disposition, testez les widgets et personnalisez.
    <br />
    <a href="/fr/getting-started/first-steps">Lire le guide →</a>
  </Card>
  <Card title="Configuration" icon="setting">
    Apprenez tout sur les widgets, modules et options.
    <br />
    <a href="/fr/configuring/config">Lire la doc →</a>
  </Card>
  <Card title="Règles Post-Installation" icon="list">
    Ajoutez les règles de couche Hyprland pour les effets de flou et popup.
    <br />
    <a href="/fr/resources/post-install">Voir les règles →</a>
  </Card>
  <Card title="FAQ & Aide" icon="question">
    Problèmes courants et conseils de dépannage.
    <br />
    <a href="/fr/help/faq">Obtenir de l'aide →</a>
  </Card>
</CardGrid>
