---
title: Probleemoplossing
description: Veelvoorkomende Tsumiki-problemen diagnosticeren
---

## Paneel verschijnt niet

1. Controleer of Hyprland draait.
2. Stop andere balken: `pkill balknaam`.
3. Start Tsumiki: `tsu -start`.

## Widget ontbreekt

- Controleer of de widget is ingeschakeld in `config.toml`.
- Controleer of deze in een `layout`-sectie staat.

## Thema wordt niet toegepast

- Controleer `theme_name` in `config.toml`.
- Hercompileer: `./init.sh -recompile`.

## Hoog CPU-gebruik

- Verlaag polling-intervallen.
- Schakel ongebruikte widgets uit.
