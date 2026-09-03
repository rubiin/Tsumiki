---
title: Übersicht
description: Was Tsumiki ist, Voraussetzungen und Schlüsselkonzepte
sidebar:
  order: 1
---

## Was ist Tsumiki?

Tsumiki (ehemals Hydepanel) ist eine modulare Statusleiste für den [Hyprland](https://hyprland.org) Wayland-Compositor. Es basiert auf dem [Fabric](https://github.com/Fabric-Development/fabric) Widget-System und bietet eine flexible Architektur für den Bau benutzerdefinierter Desktop-Panels durch zusammensetzbare Widgets.

Der Name **Tsumiki** (積み木) ist Japanisch für "Bausteine" — was das modulare, stapelbare Design des Projekts widerspiegelt.

## Voraussetzungen

Stelle vor der Installation von Tsumiki sicher, dass dein System diese Anforderungen erfüllt:

| Anforderung                                      | Hinweise                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| [Hyprland](https://hyprland.org)                 | Eine funktionierende Hyprland-Installation ist erforderlich                           |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Für die Darstellung von Symbolen und Glyphen erforderlich                             |
| **Python 3.12+**                                 | Tsumiki benötigt Python 3.12                                                          |
| **uv**                                           | Python-Paketmanager zum Installieren der Abhängigkeiten (`uv sync`)                   |
| **Arch Linux** (empfohlen)                       | Für Arch optimierte Pakete; andere Distributionen benötigen ggf. manuelle Einrichtung |
| **NetworkManager**                               | Für Netzwerk-Widgets und -Dienste erforderlich                                        |
| **PipeWire**                                     | Für Audio-Widgets und OSD erforderlich                                                |

## Schlüsselkonzepte

### Widgets

Widgets sind die einzelnen Bausteine, die in der Leiste erscheinen. Es gibt über 45 integrierte Widgets für:

- **Systeminfo** — CPU, RAM, GPU, Speicher, Netzwerkauslastung
- **Hardware-Steuerung** — Lautstärke, Helligkeit, Mikrofon, Akku
- **Desktop-Verwaltung** — Arbeitsbereiche, Fenstertitel, Taskleiste
- **Dienstprogramme** — Screenshot, OCR, Zwischenablage, Bildschirmaufnahme
- **Produktivität** — Pomodoro-Timer, Kanban-Board, Stoppuhr, Emoji-Auswahl
- **Integration** — Wetter, Mediensteuerung, GitHub Tray, DNS-Umschalter

Jedes Widget wird unter `[widgets.<name>]` in `config.toml` konfiguriert. Siehe die [Widgets-Referenz](/de/features/widgets) für die vollständige Liste.

### Module

Module sind größere UI-Oberflächen, die über die Leiste hinausgehen — eigenständige Fenster oder Overlays:

- **Leiste** — Das Hauptpanel selbst
- **Benachrichtigungssystem** — Desktop-Benachrichtigungsanzeige
- **Dock** — Anwendungs-Dock mit Intellihide
- **Übersicht** — Vollbild-Arbeitsbereichs-Exposé
- **Launcher** — Tastaturgesteuerte Anwendungssuche
- **OSD** — Bildschirmanzeigen für Lautstärke, Helligkeit usw.
- **Desktop-Uhr** — Dekorative Uhren-Überlagerung
- **Desktop-Zitate** — Inspirierende Zitate-Anzeige

Module werden unter `[modules.<name>]` in `config.toml` konfiguriert. Siehe die [Module-Referenz](/de/features/modules) für Details.

### Layout

Die Widget-Platzierung in der Leiste wird durch den Abschnitt `[layout]` in `config.toml` gesteuert:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Widgets können auch gruppiert oder in einklappbaren Gruppen platziert werden. Siehe [Konfiguration](/de/configuring/config) für Details.

### Dienste

Dienste sind Hintergrundprozesse, die Daten an Widgets liefern — sie überwachen Akkustand, Netzwerkstatus, Mediaplayer, Wetter und mehr. Widgets verbinden sich über GTK-Signale mit Diensten, was Aktualisierungen effizient hält.

## Architektur

Die Architektur von Tsumiki folgt einem geschichteten Design:

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

- **Dienste** laufen im Hintergrund und senden GTK-Signale bei Zustandsänderungen
- **Widgets** sind Panel-Buttons, die Dienstsignale abonnieren
- **Module** sind eigenständige GTK-Fenster für Overlays und Popups

Siehe die Seite [Architektur](/de/resources/architecture) für einen tieferen Einblick.

## Empfohlener Weg

1. **[Tsumiki installieren](/de/getting-started/installation)** — Klonen, Abhängigkeiten installieren, Umgebung einrichten.
2. **[Erste Schritte](/de/getting-started/first-steps)** — Leiste starten, Layout konfigurieren, Post-Installationsregeln anwenden.
3. **[Konfiguration](/de/configuring/config)** — Die TOML-Konfigurationsstruktur und verfügbare Optionen verstehen.
4. **Theme wählen** — Mit einem integrierten Theme starten oder ein eigenes erstellen mit [Themes erstellen](/de/theming/making-themes).
5. **Erkunden** — Widgets hinzufügen, Module aktivieren, Verhalten anpassen.

## Hilfe benötigt?

- Prüfe die [FAQ](/de/help/faq) für häufige Probleme.
- Besuche [Fehlerbehebung](/de/help/troubleshooting) für Debugging-Hilfe.
- Tritt dem [Discord](https://discord.gg/8nWbDC4SnP) bei für Community-Support.
