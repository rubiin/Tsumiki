---
title: Theming Tips
description: Practical theming advice for Tsumiki
---

A few tips to get the most out of [Making Themes](/en/theming/making-themes) and [Matugen](/en/theming/matugen).

## Keep Contrast High

Text must stay readable on every surface: bar, popups, notifications, quick settings. Use the `text*` and `background*` groups together and verify with a contrast check.

## Test Common Surfaces

At minimum, check these after editing a theme:

- Main bar
- Quick settings popup
- Notification toast
- Launcher and dock

## Use Semantic Accents

Reserve strong `accent*` colors for important states (errors, success, active workspace). Avoid using neon accents for static text.

## Matugen Workflow

1. Set `matugen.enabled = true` in `config.toml`.
2. Point `wallpaper` at your image.
3. Restart Tsumiki to generate the palette.
4. Recompile styles if colors look stale: `./tsumiki.sh -recompile`.

## Learn from Existing Themes

Browse `styles/themes/` for references such as `nord.scss`, `dracula.scss`, and `gruvbox.scss`. Copy a nearby theme and adjust gradually.
