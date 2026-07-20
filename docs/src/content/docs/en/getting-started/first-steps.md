---
title: First Steps
description: What to do right after installing Tsumiki
sidebar:
  order: 3
---

You installed Tsumiki and applied the [Post Installation](/en/resources/post-install) steps. Here is how to get a working panel quickly.

## 1. Start the Panel

From the Tsumiki project directory, run:

```sh
./init.sh -start
```

If Hyprland is running, the bar should appear at the top of your screen. If the bar does not appear, check for error output in the terminal and see [Troubleshooting](/en/help/troubleshooting).

:::tip
You can stop Tsumiki at any time with:

```sh
pkill tsumiki
```
:::

## 2. Set Up Autostart

Add Tsumiki to your Hyprland configuration so it launches automatically on login:

Open `~/.config/hypr/hyprland.conf` and add:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

The `sleep 5` delay gives Hyprland time to fully initialize. Adjust the path if you cloned Tsumiki to a different directory.

## 3. Copy the Example Config

Tsumiki ships with a complete example configuration. Copy it to get a valid starting point:

```sh
cp example/config.toml config.toml
```

:::tip
Open `example/config.toml` in a text editor to see all available options with documentation.
:::

## 4. Customize Your Layout

Edit `config.toml` and adjust the `[layout]` section. Each section (`left_section`, `middle_section`, `right_section`) is an array of widget names:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

This creates a bar with:

| Section | Widgets |
|---|---|
| **Left** | Workspace switcher, active window title |
| **Middle** | Current date and time |
| **Right** | Volume control, battery status, system tray, power menu |

## 5. Reload to Apply Changes

After saving your edits, restart Tsumiki:

```sh
pkill tsumiki
./init.sh -start
```

If the configuration is valid, the bar should reappear with your new layout.

## 6. Test Common Widgets

Try interacting with your widgets:

- **Workspaces** — Click to switch, scroll to cycle through desktops.
- **Volume** — Click to mute/unmute, scroll to adjust.
- **Battery** — Hover to see remaining time and charge status.
- **Date/Time** — Click to open the calendar and notification panel.
- **System Tray** — Existing tray icons should appear automatically.

## 7. Make It Yours

- **Change colors** — See [Making Themes](/en/theming/making-themes) for SCSS customization or [Matugen](/en/theming/matugen) for automatic wallpaper-based theming.
- **Add more widgets** — Browse the [Widgets Reference](/en/features/widgets) for all 45+ available widgets.
- **Enable modules** — Try the [Dock](/en/features/modules#dock), [App Launcher](/en/features/modules#application-launcher), or [OSD](/en/features/modules#osd-on-screen-display).
- **Configure behavior** — See the full [Configuration](/en/configuring/config) reference for every option.

## Troubleshooting

If something looks wrong:

- **Bar doesn't appear** — Check that you're running Hyprland and that no other bars are running (`pkill waybar`).
- **No icons** — Verify [JetBrains Nerd Font](https://www.nerdfonts.com) is installed and configured as your terminal/UI font.
- **Missing functionality** — Some widgets require external tools (e.g., `playerctl` for media, `brightnessctl` for brightness). Run `./init.sh -setup` to ensure all dependencies are installed.
- **SASS errors** — Your `config.toml` may be invalid. Compare with `example/config.toml`.

For more help, see the [FAQ](/en/help/faq) or [Troubleshooting](/en/help/troubleshooting) pages.
