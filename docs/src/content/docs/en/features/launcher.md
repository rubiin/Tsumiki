---
title: Launcher
description: Application launcher widget for Tsumiki
---

The Launcher widget gives you a fast, keyboard-driven way to find and open applications from the panel.

## What It Does

- Searches installed desktop entries by name or keyword.
- Launches applications without leaving the panel.
- Supports drag-to-pin and custom actions.

## Configuration

Launcher settings live under the `widgets.launcher` table in `config.toml`:

```toml
[widgets.launcher]
enabled = true
search_paths = ["/usr/share/applications", "~/.local/share/applications"]
max_results = 8
```

Add `launcher` to a bar section in the `layout` table to display it:

```toml
[layout]
left_section = ["launcher", "workspaces"]
```

## Related

- [Dock](/en/features/dock) for pinned applications.
- [Configuration](/en/configuring/config) for layout basics.
