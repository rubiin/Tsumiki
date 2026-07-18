---
title: OSD
description: On-screen display module for Tsumiki
---

The OSD (On-Screen Display) module shows transient feedback for system actions such as volume and brightness changes.

## What It Does

- Displays a brief overlay when you change volume, brightness, or similar properties.
- Appears centered or near the relevant control, then fades automatically.
- Keeps you informed without cluttering the panel.

## Configuration

OSD is a module, configured under `modules.osd` (see [Configuration](/en/configuring/config)):

```toml
[modules.osd]
enabled = true
timeout = 1500
```

## Tips

- Pair with the [Volume](/en/configuring/config) widget for consistent audio feedback.
- If the OSD does not appear, ensure the Hyprland layer rules from [Post Installation](/en/resources/post-install) are applied.
- Restart Tsumiki after changing OSD behavior.
