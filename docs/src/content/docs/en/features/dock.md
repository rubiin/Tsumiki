---
title: Dock
description: Dock module for Tsumiki
---

The Dock module provides a pinned-application launcher that integrates with Hyprland.

## What It Does

- Pins your favorite applications to a persistent dock.
- Supports intellihide and auto-show behaviors.
- Reflects open windows from Hyprland.

## Configuration

The dock is a module, configured under `modules.dock` (see [Configuration](/en/configuring/config)):

```toml
[modules.dock]
enabled = true
behavior = "intellihide"
show_when_no_windows = false
icon_size = 40
```

## Tips

- Pair with the [Launcher](/en/features/launcher) for a complete app experience.
- Restart Tsumiki after changing dock behavior.
