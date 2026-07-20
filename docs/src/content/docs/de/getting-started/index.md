---
title: Schnellstart
description: Tsumiki in wenigen Minuten zum Laufen bringen
---

Tsumiki ist eine modulare Statusleiste für Hyprland, die auf dem Fabric-Widget-System basiert.

## Voraussetzungen

Stelle vor dem Start sicher, dass du Folgendes hast:

- **Hyprland** — eine funktionierende Hyprland-Installation
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` sollte 3.12 oder höher anzeigen

## Schnellinstallation

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

Das Flag `-setup` installiert alle erforderlichen Systempakete und Python-Abhängigkeiten. Während der Einrichtung wirst du möglicherweise nach deinem Passwort gefragt.

Für alternative Installationsmethoden (Bootstrap-Skript, manuelle Einrichtung) siehe die [vollständige Installationsanleitung](/de/getting-started/installation).

## Autostart

Füge diese Zeile zu `~/.config/hypr/hyprland.conf` hinzu:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Minimale Konfiguration

Hier ist eine minimale `config.toml` für den Start:

```toml
$schema = "./tsumiki.schema.json"

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

Nach dem Speichern die Leiste neu starten:

```sh
pkill tsumiki
./init.sh -start
```

## Nächste Schritte

<CardGrid stagger>
  <Card title="Erste Schritte" icon="rocket">
    Konfiguriere dein Layout, teste Widgets und mache es zu deinem.
    <br />
    <a href="/de/getting-started/first-steps">Anleitung lesen →</a>
  </Card>
  <Card title="Konfiguration" icon="setting">
    Erfahre alles über Widgets, Module und Optionen.
    <br />
    <a href="/de/configuring/config">Dokumentation lesen →</a>
  </Card>
  <Card title="Post-Installations-Regeln" icon="list">
    Füge Hyprland-Layer-Regeln für Unschärfe- und Popup-Effekte hinzu.
    <br />
    <a href="/de/resources/post-install">Regeln anzeigen →</a>
  </Card>
  <Card title="FAQ & Hilfe" icon="question">
    Häufige Probleme und Tipps zur Fehlerbehebung.
    <br />
    <a href="/de/help/faq">Hilfe erhalten →</a>
  </Card>
</CardGrid>
