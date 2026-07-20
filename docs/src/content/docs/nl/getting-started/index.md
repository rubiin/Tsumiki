---
title: Snelstartgids
description: Zet Tsumiki binnen enkele minuten aan de praat
---

Tsumiki is een modulaire statusbalk voor Hyprland, gebouwd op het Fabric-widgetsysteem.

## Vereisten

Zorg ervoor dat je het volgende hebt voordat je begint:

- **Hyprland** — een werkende Hyprland-installatie
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` moet 3.12 of hoger tonen

## Snelle Installatie

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

De vlag `-setup` installeert alle benodigde systeempakketten en Python-afhankelijkheden. Tijdens de installatie kan naar je wachtwoord worden gevraagd.

Voor alternatieve installatiemethoden (bootstrap-script, handmatige installatie), zie de [volledige installatiehandleiding](/nl/getting-started/installation).

## Automatisch Starten

Voeg deze regel toe aan `~/.config/hypr/hyprland.conf`:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Minimale Configuratie

Hier is een minimale `config.toml` om te beginnen:

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

Na het opslaan, herstart de balk:

```sh
pkill tsumiki
./init.sh -start
```

## Volgende Stappen

<CardGrid stagger>
  <Card title="Eerste Stappen" icon="rocket">
    Configureer je lay-out, test widgets en maak het je eigen.
    <br />
    <a href="/nl/getting-started/first-steps">Handleiding lezen →</a>
  </Card>
  <Card title="Configuratie" icon="setting">
    Leer over elke widget, module en optie.
    <br />
    <a href="/nl/configuring/config">Documentatie lezen →</a>
  </Card>
  <Card title="Post-Installatieregels" icon="list">
    Voeg Hyprland-laagregels toe voor vervaging en pop-upeffecten.
    <br />
    <a href="/nl/resources/post-install">Regels bekijken →</a>
  </Card>
  <Card title="FAQ & Hulp" icon="question">
    Veelvoorkomende problemen en advies voor probleemoplossing.
    <br />
    <a href="/nl/help/faq">Hulp krijgen →</a>
  </Card>
</CardGrid>
