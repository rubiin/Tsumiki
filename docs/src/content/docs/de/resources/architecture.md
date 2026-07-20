---
title: Architektur
description: Architektur-Überblick für Entwickler und Mitwirkende
sidebar:
  order: 5
---

## Projektstruktur

```
tsumiki/
├── main.py                  # Einstiegspunkt
├── config.toml              # Benutzerkonfiguration
├── themes/                  # Theme-.toml-Dateien
├── styles/                  # SCSS-Stylesheets
├── widgets/                 # Leisten-Widgets
├── modules/                 # Eigenständige Overlays & Fenster
├── services/                # Hintergrunddienste
├── shared/                  # Wiederverwendbare UI-Komponenten
├── utils/                   # Hilfsmodule
└── assets/                  # Statische Ressourcen
```

## Schlüsseldienste

| Dienst | Quelle | Beschreibung |
|---|---|---|
| Akku | UPower D-Bus | Ladestand, Ladezustand |
| Netzwerk | NetworkManager D-Bus | WiFi, Ethernet |
| Helligkeit | brightnessctl | Bildschirm-/Tastaturhelligkeit |
| Wetter | Open-Meteo | Wetterbedingungen |
| MPRIS | Playerctl | Medienwiedergabe |
| Matugen | matugen-Binary | Material-You-Palette |

## Neues Widget hinzufügen

1. `widgets/mein_widget.py` erstellen
2. Konfiguration in `utils/widget_settings.py` hinzufügen
3. Schemaeintrag in `tsumiki.schema.json` hinzufügen
4. In `modules/bar.py` registrieren
5. SCSS-Stile hinzufügen
6. Im Layout referenzieren
