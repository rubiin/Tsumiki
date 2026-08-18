---
title: Fehlerbehebung
description: Häufige Tsumiki-Probleme diagnostizieren und beheben
---

Diese Seite behandelt Probleme, die über die [FAQ](/de/help/faq) hinausgehen.

## Panel erscheint nicht

1. Stellen Sie sicher, dass Hyprland läuft und die Layer-Regeln aus [Nach der Installation](/de/resources/post-install) angewendet wurden.
2. Beenden Sie konkurrierende Leisten: `pkill leistenname`.
3. Starten Sie Tsumiki: `tsu -start` und beobachten Sie die Log-Ausgabe.

## Widget fehlt

- Prüfen Sie, ob das Widget in `config.toml` unter `[widgets.<name>]` aktiviert ist.
- Stellen Sie sicher, dass das Widget in einem `layout`-Abschnitt gelistet ist.
- Prüfen Sie auf `ModuleNotFoundError` und installieren Sie Abhängigkeiten mit `tsu -setup`.

## Theme wird nicht angewendet

- Prüfen Sie, ob `theme_name` in `config.toml` mit einer Datei in `themes/` übereinstimmt.
- Stile neu kompilieren: `./tsumiki.sh -recompile`.
- Für Matugen, siehe [Theming mit Matugen](/de/theming/matugen).

## Hohe CPU- oder Speicherauslastung

- Reduzieren Sie Abfrageintervalle in der Widget-Konfiguration.
- Deaktivieren Sie ungenutzte Widgets und Module.
- Aktivieren Sie `auto_hide`, um Neuladevorgänge zu reduzieren.

## Immer noch Probleme?

Eröffnen Sie ein Issue mit Ihrer `config.toml` und den Logs von `tsu -start`.
