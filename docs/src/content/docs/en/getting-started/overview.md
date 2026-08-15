---
title: Overview
description: What Tsumiki is, prerequisites, and key concepts
sidebar:
  order: 1
---

## What is Tsumiki?

Tsumiki (formerly Hydepanel) is a modular status bar for the [Hyprland](https://hyprland.org) Wayland compositor. Built on the [Fabric](https://github.com/Fabric-Development/fabric) widget system, it provides a flexible architecture for building custom desktop panels through composable widgets.

The name **Tsumiki** (積み木) is Japanese for "building blocks" — reflecting the project's modular, stackable design.

## Prerequisites

Before installing Tsumiki, ensure your system meets these requirements:

| Requirement | Notes |
|---|---|
| [Hyprland](https://hyprland.org) | A functioning Hyprland installation is required |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Required for icon and glyph rendering |
| **Python 3.12+** | Tsumiki targets Python 3.12 |
| **uv** | Python package manager used to install dependencies (`uv sync`) |
| **Arch Linux** (recommended) | Packages optimized for Arch; other distros may need manual setup |
| **NetworkManager** | Required for network-related widgets and services |
| **PipeWire** | Required for audio-related widgets and OSD |

## Key Concepts

### Widgets

Widgets are the individual building blocks that appear in the bar. There are 45+ built-in widgets covering:

- **System info** — CPU, memory, GPU, storage, network usage
- **Hardware control** — Volume, brightness, microphone, battery
- **Desktop management** — Workspaces, window title, taskbar
- **Utilities** — Screenshot, OCR, clipboard, screen recording
- **Productivity** — Pomodoro timer, Kanban board, stopwatch, emoji picker
- **Integration** — Weather, media controls, Git companion, DNS switcher

Each widget is configured under `[widgets.<name>]` in `config.toml`. See the [Widgets Reference](/en/features/widgets) for the complete list.

### Modules

Modules are larger UI surfaces that go beyond the bar — they are standalone windows or overlays:

- **Bar** — The main panel itself
- **Notification System** — Desktop notification display
- **Dock** — Application dock with intellihide
- **Overview** — Full-screen workspace exposé
- **Launcher** — Keyboard-driven application search
- **OSD** — On-screen displays for volume, brightness, etc.
- **Desktop Clock** — Decorative clock overlay
- **Desktop Quotes** — Inspirational quote display

Modules are configured under `[modules.<name>]` in `config.toml`. See the [Modules Reference](/en/features/modules) for details.

### Layout

Widget placement in the bar is controlled by the `[layout]` section of `config.toml`:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Widgets can also be grouped together or placed in collapsible groups. See [Configuration](/en/configuring/config) for details.

### Services

Services are background processes that supply data to widgets — they monitor battery levels, network state, media players, weather, and more. Widgets connect to services via GTK signals, keeping updates efficient.

## Architecture

Tsumiki's architecture follows a layered design:

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
  │ (DBus    │  │ (Panel   │  │ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **Services** run in the background and emit GTK signals on state changes
- **Widgets** are panel buttons that subscribe to service signals
- **Modules** are standalone GTK windows for overlays and popups

See the [Architecture](/en/resources/architecture) page for a deeper look.

## Recommended Path

1. **[Install Tsumiki](/en/getting-started/installation)** — Clone, install dependencies, set up the environment.
2. **Follow [First Steps](/en/getting-started/first-steps)** — Start the bar, configure your layout, apply post-installation rules.
3. **Learn [Configuration](/en/configuring/config)** — Understand the TOML config structure and available options.
4. **Choose your theme** — Start with a built-in theme or create your own with [Making Themes](/en/theming/making-themes).
5. **Explore** — Add widgets, enable modules, customize behavior.

## Need Help?

- Check the [FAQ](/en/help/faq) for common issues.
- Visit [Troubleshooting](/en/help/troubleshooting) for debugging guidance.
- Join the [Discord](https://discord.gg/8nWbDC4SnP) for community support.
