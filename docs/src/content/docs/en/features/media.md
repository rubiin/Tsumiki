---
title: Media
description: Media controls widget for Tsumiki
---

The Media widget shows current playback and gives you transport controls for MPRIS-compatible players.

## What It Does

- Displays track title, artist, and album art (if available).
- Play/pause, next, and previous controls.
- Volume and seek integration with Playerctl.

## Configuration

Enable and tune the widget under `widgets.media`:

```toml
[widgets.media]
enabled = true
show_art = true
max_title_length = 24
```

## Notes

- Requires `playerctl` to be installed (see [Installation](/en/getting-started/installation)).
- If no player is running, the widget hides automatically.

## Related

- [Volume](/en/configuring/config) for system audio control.
- [FAQ](/en/help/faq) if media controls do not appear.
