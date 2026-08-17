---
title: Quick Start
description: Get Tsumiki running in minutes
---


Tsumiki is a modular status bar for Hyprland built on the Fabric widget system.

## Prerequisites

Before starting, ensure you have:

- **Hyprland** — a working Hyprland installation
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` should show 3.12 or higher
- **uv** — Python package manager used to install dependencies (`uv sync`)

## Quick Install

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

The `-setup` flag installs all required system packages and Python dependencies. You may be prompted for your password during setup.

For alternative install methods (bootstrap script, manual setup), see the [full installation guide](/en/getting-started/installation).

## Autostart

Add this line to `~/.config/hypr/hyprland.conf`:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Minimal Config

Here is a minimal `config.toml` to get started:

```toml
"$schema" = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

After saving, restart the bar:

```sh
pkill tsumiki
./init.sh -start
```

## Next Steps

<CardGrid stagger>
  <Card title="First Steps" icon="rocket">
    Configure your layout, test widgets, and make it yours.
    <br />
    <a href="/en/getting-started/first-steps">Read guide →</a>
  </Card>
  <Card title="Configuration" icon="setting">
    Learn about every widget, module, and option.
    <br />
    <a href="/en/configuring/config">Read docs →</a>
  </Card>
  <Card title="Post-Install Rules" icon="list">
    Add Hyprland layer rules for blur and popup effects.
    <br />
    <a href="/en/resources/post-install">View rules →</a>
  </Card>
  <Card title="FAQ & Help" icon="question">
    Common issues and troubleshooting advice.
    <br />
    <a href="/en/help/faq">Get help →</a>
  </Card>
</CardGrid>
