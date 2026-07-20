---
title: Theming-Tipps
description: Praktische Tipps zur Theme-Erstellung für Tsumiki
---

## Kontrast hoch halten

Text muss auf allen Oberflächen lesbar bleiben: Leiste, Popups, Benachrichtigungen.

## Häufige Oberflächen testen

Prüfen Sie mindestens: Hauptleiste, Schnelleinstellungen, Benachrichtigungen, Launcher, Dock.

## Semantische Akzente verwenden

Sparen Sie starke `accent*`-Farben für wichtige Zustände (Fehler, Erfolg, aktiver Arbeitsbereich).

## Matugen-Workflow

1. `matugen.enabled = true` in `config.toml` setzen.
2. `wallpaper` auf Ihr Bild verweisen.
3. Tsumiki neu starten, um die Palette zu generieren.
4. Bei Bedarf neu kompilieren: `./init.sh -recompile`.
