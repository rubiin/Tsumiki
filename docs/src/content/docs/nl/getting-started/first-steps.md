---
title: Eerste Stappen
description: Wat te doen direct na het installeren van Tsumiki
sidebar:
  order: 3
---

Je hebt Tsumiki geïnstalleerd en de [Post-Installatie](/nl/resources/post-install) stappen toegepast. Hier lees je hoe je snel een werkend paneel krijgt.

## 1. Start het Paneel

Vanuit de Tsumiki-projectmap voer je uit:

```sh
./init.sh -start
```

Als Hyprland actief is, zou de balk boven aan je scherm moeten verschijnen. Als de balk niet verschijnt, controleer dan de foutuitvoer in de terminal en raadpleeg [Probleemoplossing](/nl/help/troubleshooting).

:::tip
Je kunt Tsumiki op elk moment stoppen met:

```sh
pkill tsumiki
```
:::

## 2. Stel Automatisch Starten In

Voeg Tsumiki toe aan je Hyprland-configuratie zodat het automatisch start bij inloggen:

Open `~/.config/hypr/hyprland.conf` en voeg toe:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

De `sleep 5` vertraging geeft Hyprland de tijd om volledig te initialiseren. Pas het pad aan als je Tsumiki in een andere map hebt gekloond.

## 3. Kopieer de Voorbeeldconfiguratie

Tsumiki wordt geleverd met een volledige voorbeeldconfiguratie. Kopieer deze om een geldig startpunt te krijgen:

```sh
cp example/config.toml config.toml
```

:::tip
Open `example/config.toml` in een teksteditor om alle beschikbare opties met documentatie te bekijken.
:::

## 4. Pas je Lay-out Aan

Bewerk `config.toml` en pas de sectie `[layout]` aan. Elke sectie (`left_section`, `middle_section`, `right_section`) is een array van widget-namen:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Dit maakt een balk met:

| Sectie | Widgets |
|---|---|
| **Links** | Werkruimteschakelaar, actieve venstertitel |
| **Midden** | Huidige datum en tijd |
| **Rechts** | Volumeregeling, batterijstatus, systeemvak, energiemenu |

## 5. Herlaad om Wijzigingen Toe te Passen

Na het opslaan van je bewerkingen herstart je Tsumiki:

```sh
pkill tsumiki
./init.sh -start
```

Als de configuratie geldig is, zou de balk opnieuw moeten verschijnen met je nieuwe lay-out.

## 6. Test Veelvoorkomende Widgets

Probeer interactie met je widgets:

- **Werkruimtes** — Klik om te wisselen, scroll om door desktops te bladeren.
- **Volume** — Klik om te dempen/activeren, scroll om aan te passen.
- **Batterij** — Hover om resterende tijd en laadstatus te zien.
- **Datum/Tijd** — Klik om de kalender en het meldingenpaneel te openen.
- **Systeemvak** — Aanwezige pictogrammen zouden automatisch moeten verschijnen.

## 7. Maak het Je Eigen

- **Verander kleuren** — Zie [Thema's maken](/nl/theming/making-themes) voor SCSS-aanpassing of [Matugen](/nl/theming/matugen) voor automatische theming op basis van achtergrond.
- **Voeg meer widgets toe** — Blader door de [Widgets-referentie](/nl/features/widgets) voor alle 45+ beschikbare widgets.
- **Schakel modules in** — Probeer de [Dock](/nl/features/modules#dock), [App Launcher](/nl/features/modules#app-launcher) of [OSD](/nl/features/modules#osd-schermweergave).
- **Configureer gedrag** — Zie de volledige [Configuratie](/nl/configuring/config) referentie voor elke optie.

## Probleemoplossing

Als er iets niet klopt:

- **Balk verschijnt niet** — Controleer of Hyprland draait en of er geen andere balken actief zijn (`pkill waybar`).
- **Geen pictogrammen** — Controleer of [JetBrains Nerd Font](https://www.nerdfonts.com) is geïnstalleerd en geconfigureerd als je terminal/UI-lettertype.
- **Ontbrekende functionaliteit** — Sommige widgets vereisen externe tools (bijv. `playerctl` voor media, `brightnessctl` voor helderheid). Voer `./init.sh -setup` uit om ervoor te zorgen dat alle afhankelijkheden zijn geïnstalleerd.
- **SASS-fouten** — Je `config.toml` is mogelijk ongeldig. Vergelijk het met `example/config.toml`.

Voor meer hulp, raadpleeg de [FAQ](/nl/help/faq) of [Probleemoplossing](/nl/help/troubleshooting) pagina's.
