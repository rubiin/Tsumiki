---
title: Erste Schritte
description: Was Sie direkt nach der Installation von Tsumiki tun sollten
sidebar:
  order: 3
---

Sie haben Tsumiki installiert und die [Post-Installations](/de/resources/post-install)-Schritte angewendet. Hier erfahren Sie, wie Sie schnell ein funktionierendes Panel erhalten.

## 1. Panel starten

Führen Sie vom Tsumiki-Projektverzeichnis aus:

```sh
./tsumiki.sh -start
```

Wenn Hyprland läuft, sollte die Leiste oben auf Ihrem Bildschirm erscheinen. Wenn die Leiste nicht erscheint, überprüfen Sie die Fehlerausgabe im Terminal und siehe [Fehlerbehebung](/de/help/troubleshooting).

:::tip
Sie können Tsumiki jederzeit beenden mit:

```sh
pkill tsumiki
```

:::

## 2. Autostart einrichten

Fügen Sie Tsumiki zu Ihrer Hyprland-Konfiguration hinzu, damit es beim Einloggen automatisch startet:

Öffnen Sie `~/.config/hypr/hyprland.conf` und fügen Sie hinzu:

```sh
exec-once = sleep 5; ~/.config/tsumiki/tsumiki.sh -start
```

Die Verzögerung `sleep 5` gibt Hyprland Zeit, vollständig zu initialisieren. Passen Sie den Pfad an, wenn Sie Tsumiki in ein anderes Verzeichnis geklont haben.

## 3. Beispielkonfiguration kopieren

Tsumiki wird mit einer vollständigen Beispielkonfiguration ausgeliefert. Kopieren Sie sie, um einen gültigen Ausgangspunkt zu erhalten:

```sh
cp example/config.toml config.toml
```

:::tip
Öffnen Sie `example/config.toml` in einem Texteditor, um alle verfügbaren Optionen mit Dokumentation zu sehen.
:::

## 4. Layout anpassen

Bearbeiten Sie `config.toml` und passen Sie den Abschnitt `[layout]` an. Jeder Abschnitt (`left_section`, `middle_section`, `right_section`) ist ein Array von Widget-Namen:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Dies erzeugt eine Leiste mit:

| Bereich    | Widgets                                                |
| ---------- | ------------------------------------------------------ |
| **Links**  | Arbeitsbereich-Umschalter, aktiver Fenstertitel        |
| **Mitte**  | Aktuelles Datum und Uhrzeit                            |
| **Rechts** | Lautstärkeregler, Akkustatus, System Tray, Energiemenü |

## 5. Neu laden, um Änderungen zu übernehmen

Nach dem Speichern Ihrer Änderungen starten Sie Tsumiki neu:

```sh
pkill tsumiki
./tsumiki.sh -start
```

Wenn die Konfiguration gültig ist, sollte die Leiste mit Ihrem neuen Layout wieder erscheinen.

## 6. Allgemeine Widgets testen

Interagieren Sie mit Ihren Widgets:

- **Arbeitsbereiche** — Klicken zum Wechseln, scrollen zum Durchlaufen der Desktops.
- **Lautstärke** — Klicken zum Stummschalten, scrollen zum Anpassen.
- **Akku** — Darüberfahren, um Restzeit und Ladestatus zu sehen.
- **Datum/Uhrzeit** — Klicken, um Kalender und Benachrichtigungsfeld zu öffnen.
- **System Tray** — Vorhandene Tray-Symbole sollten automatisch erscheinen.

## 7. Machen Sie es zu Ihrem

- **Farben ändern** — Siehe [Themes erstellen](/de/theming/making-themes) für SCSS-Anpassung oder [Matugen](/de/theming/matugen) für automatische Hintergrundbild-basierte Theming.
- **Weitere Widgets hinzufügen** — Durchsuchen Sie die [Widgets-Referenz](/de/features/widgets) für alle über 45 verfügbaren Widgets.
- **Module aktivieren** — Probieren Sie das [Dock](/de/features/modules#dock), den [Launcher](/de/features/modules#launcher) oder das [OSD](/de/features/modules#osd-bildschirmanzeige) aus.
- **Verhalten konfigurieren** — Siehe die vollständige [Konfigurations](/de/configuring/config)-Referenz für jede Option.

## Fehlerbehebung

Wenn etwas nicht stimmt:

- **Leiste erscheint nicht** — Überprüfen Sie, ob Hyprland läuft und keine anderen Leisten aktiv sind (`pkill waybar`).
- **Keine Symbole** — Stellen Sie sicher, dass [JetBrains Nerd Font](https://www.nerdfonts.com) installiert und als Terminal-/UI-Schriftart konfiguriert ist.
- **Fehlende Funktionalität** — Einige Widgets erfordern externe Tools (z.B. `playerctl` für Medien, `brightnessctl` für Helligkeit). Führen Sie `./tsumiki.sh -setup` aus, um sicherzustellen, dass alle Abhängigkeiten installiert sind (Python-Abhängigkeiten werden mit `uv sync` installiert).
- **SASS-Fehler** — Ihre `config.toml` könnte ungültig sein. Vergleichen Sie sie mit `example/config.toml`.

Weitere Hilfe finden Sie auf den Seiten [FAQ](/de/help/faq) oder [Fehlerbehebung](/de/help/troubleshooting).
