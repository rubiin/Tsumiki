---
title: Overzicht
description: Wat Tsumiki is, vereisten en kernconcepten
sidebar:
  order: 1
---

## Wat is Tsumiki?

Tsumiki (voorheen Hydepanel) is een modulaire statusbalk voor de [Hyprland](https://hyprland.org) Wayland-compositor. Gebouwd op het [Fabric](https://github.com/Fabric-Development/fabric) widgetsysteem, biedt het een flexibele architectuur voor het bouwen van aangepaste desktop-panelen via samengestelde widgets.

De naam **Tsumiki** (積み木) is Japans voor "bouwstenen" — wat het modulaire, stapelbare ontwerp van het project weerspiegelt.

## Vereisten

Zorg ervoor dat je systeem aan deze vereisten voldoet voordat je Tsumiki installeert:

| Vereiste | Opmerkingen |
|---|---|
| [Hyprland](https://hyprland.org) | Een werkende Hyprland-installatie is vereist |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Vereist voor weergave van pictogrammen en glyphs |
| **Python 3.12+** | Tsumiki vereist Python 3.12 |
| **uv** | Python-pakketbeheerder die wordt gebruikt om afhankelijkheden te installeren (`uv sync`) |
| **Arch Linux** (aanbevolen) | Pakketten geoptimaliseerd voor Arch; andere distro's hebben mogelijk handmatige installatie nodig |
| **NetworkManager** | Vereist voor netwerkgerelateerde widgets en services |
| **PipeWire** | Vereist voor audiogerelateerde widgets en OSD |

## Kernconcepten

### Widgets

Widgets zijn de individuele bouwstenen die in de balk verschijnen. Er zijn meer dan 45 ingebouwde widgets die betrekking hebben op:

- **Systeeminformatie** — CPU, geheugen, GPU, opslag, netwerkgebruik
- **Hardwarebediening** — Volume, helderheid, microfoon, batterij
- **Desktopbeheer** — Werkruimten, venstertitel, taakbalk
- **Hulpprogramma's** — Schermafbeelding, OCR, klembord, schermopname
- **Productiviteit** — Pomodoro-timer, Kanban-bord, stopwatch, emoji-picker
- **Integratie** — Weer, mediaregeling, Git-companion, DNS-schakelaar

Elke widget wordt geconfigureerd onder `[widgets.<naam>]` in `config.toml`. Zie de [Widgets-referentie](/nl/features/widgets) voor de volledige lijst.

### Modules

Modules zijn grotere UI-oppervlakken die verder gaan dan de balk — ze zijn zelfstandige vensters of overlays:

- **Balk** — Het hoofdscherm zelf
- **Notificatiesysteem** — Desktopmeldingenweergave
- **Dock** — Toepassingsdock met intellihide
- **Overzicht** — Volledig scherm werkruimte-exposé
- **App-launcher** — Toetsenbordgestuurd toepassingen zoeken
- **OSD** — Schermweergaven voor volume, helderheid, etc.
- **Desktopklok** - Decoratieve klokoverlay
- **Desktopcitaten** - Inspirerende citatenweergave

Modules worden geconfigureerd onder `[modules.<naam>]` in `config.toml`. Zie de [Modules-referentie](/nl/features/modules) voor details.

### Lay-out

De plaatsing van widgets in de balk wordt bepaald door de sectie `[layout]` van `config.toml`:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Widgets kunnen ook worden gegroepeerd of in samenvouwbare groepen worden geplaatst. Zie [Configuratie](/nl/configuring/config) voor details.

### Services

Services zijn achtergrondprocessen die gegevens aan widgets leveren — ze bewaken batterijniveaus, netwerkstatus, mediaspelers, weer en meer. Widgets maken via GTK-signalen verbinding met services, waardoor updates efficiënt blijven.

## Architectuur

De architectuur van Tsumiki volgt een gelaagd ontwerp:

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

- **Services** draaien op de achtergrond en zenden GTK-signalen uit bij statuswijzigingen
- **Widgets** zijn paneelknoppen die zich abonneren op servicesignalen
- **Modules** zijn zelfstandige GTK-vensters voor overlays en pop-ups

Zie de [Architectuur](/nl/resources/architecture) pagina voor een diepere blik.

## Aanbevolen Pad

1. **[Tsumiki installeren](/nl/getting-started/installation)** — Clonen, afhankelijkheden installeren, omgeving instellen.
2. **Volg [Eerste Stappen](/nl/getting-started/first-steps)** — Start de balk, configureer je lay-out, pas post-installatieregels toe.
3. **Leer [Configuratie](/nl/configuring/config)** — Begrijp de TOML-configuratiestructuur en beschikbare opties.
4. **Kies je thema** — Begin met een ingebouwd thema of maak je eigen met [Thema's maken](/nl/theming/making-themes).
5. **Verken** — Voeg widgets toe, schakel modules in, pas gedrag aan.

## Hulp Nodig?

- Raadpleeg de [FAQ](/nl/help/faq) voor veelvoorkomende problemen.
- Bezoek [Probleemoplossing](/nl/help/troubleshooting) voor hulp bij debuggen.
- Word lid van de [Discord](https://discord.gg/8nWbDC4SnP) voor community-ondersteuning.
