---
title: First Steps
description: What to do right after installing Tsumiki
sidebar:
  order: 3
---

You installed Tsumiki and applied the Post Installation steps. Here is how to get a working panel quickly.

## 1. Start the Panel

```sh
tsu -start
```

If Hyprland is already running, the bar should appear at the top of your screen.

## 2. Open the Example Config

Copy the example configuration so you start from a valid base:

```sh
cp example/config.toml config.toml
```

## 3. Pick Your Widgets

Edit `config.toml` and adjust the `layout` sections. A minimal starting point:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

## 4. Reload

After saving, restart Tsumiki:

```sh
pkill tsumiki
tsu -start
```

## 5. Make It Yours

- Change colors in [Making Themes](/en/theming/making-themes).
- Add modules like the [Dock](/en/features/dock) or [Launcher](/en/features/launcher).
- Browse the [Configuration](/en/configuring/config) reference for every option.

If something looks wrong, check the [FAQ](/en/help/faq) or [Troubleshooting](/en/help/troubleshooting).
