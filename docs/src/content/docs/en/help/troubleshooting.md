---
title: Troubleshooting
description: Diagnose and fix common Tsumiki issues
---

This page covers issues beyond the [FAQ](/en/help/faq).

## Panel Does Not Appear

1. Ensure Hyprland is running and the layer rules from [Post Installation](/en/resources/post-install) are applied.
2. Kill any conflicting bar: `pkill bar-name`.
3. Start Tsumiki: `tsu -start` and watch the log output.

## Widget Missing

- Confirm the widget is enabled in `config.toml` under `[widgets.<name>]`.
- Verify the widget is listed in a `layout` section.
- Check for `ModuleNotFoundError` and install dependencies with `tsu -setup`.

## Theme Not Applying

- Confirm `theme_name` in `config.toml` matches a file in `themes/`.
- Recompile styles: `./tsumiki.sh -recompile`.
- For Matugen, see [Theming with Matugen](/en/theming/matugen).

## High CPU or Memory

- Reduce polling intervals in widget config.
- Disable unused widgets and modules.
- Enable `auto_hide` to reduce redraws.

## Still Stuck?

Open an issue with your `config.toml` and logs from `tsu -start`.
