---
title: Making Themes
description: How to make themes for Tsumiki
---

This guide walks through creating a custom Tsumiki theme from scratch.

## Where Themes Live

Create your theme file in `themes/` with a `.toml` extension.

Example:

```bash
touch themes/my-theme.toml
```

## Minimum Theme Template

Copy this starter and adjust values:

```toml
[dark.background]
main =  "#121212"  # Main background (dark, almost black with a slight grayish tint)
alt =  "#1a1a1a"  # Secondary background (dark, industrial gray)
dark =  "#0a0a0a"  # Darkest background (deep black, ultra-dark)


[dark.text]
main =  "#e0e0e0"  # Primary text color (light, almost white gray)
secondary =  "#c5c5c5"  # Secondary text color (soft light gray)
muted =  "#8e8e8e"  # Tertiary text, muted (dark gray)
disabled =  "#666666"  # Disabled text (muted gray)
muted-light =  "#999999"  # Light-muted text for hints (light gray)
muted-dark =  "#444444"  # Dark-muted text (gray with a slight purplish tint)


[dark.surface]
disabled =  "#444444"  # Disabled items (dark gray)
neutral =  "#333333"  # Neutral surface for cards, panels (dark gray with slight blue undertones)
highlight =  "#00f0f0"  # Selection and highlights (neon cyan)


[dark.accent]
light =  "#ff007f"  # Light accent (neon pink)
pink =  "#ff007f"  # Pink accent (neon pink)
purple =  "#9c00ff"  # Purple accent (electric purple)
red =  "#ff1744"  # Red for errors and warnings (bright neon red)
orange =  "#ff6d00"  # Orange for alerts (vibrant neon orange)
yellow =  "#ffea00"  # Yellow for highlights (electric yellow)
green =  "#00ff00"  # Green for success (neon green)
teal =  "#00b3b3"  # Teal for information (bright cyan)
blue =  "#00d0ff"  # Blue for links and actions (electric blue)
light-blue =  "#00d0ff"  # Sky blue accent (electric blue)
lavender =  "#b084ff"  # Lavender for subtle highlights (neon lavender)


[dark.general]
bar-background =  "rgba(18, 18, 18, 0.8)"  # Panel background (semi-transparent dark background)
shadow-color =  "rgba(0, 0, 0, 0.6)"  # Shadow color (deep shadows with high contrast)


[light.background]
main =  "#ededed"  # Main background (dark, almost black with a slight grayish tint)
alt =  "#e5e5e5"  # Secondary background (dark, industrial gray)
dark =  "#f5f5f5"  # Darkest background (deep black, ultra-dark)


[light.text]
main =  "#1f1f1f"  # Primary text color (light, almost white gray)
secondary =  "#3a3a3a"  # Secondary text color (soft light gray)
muted =  "#717171"  # Tertiary text, muted (dark gray)
disabled =  "#999999"  # Disabled text (muted gray)
muted-light =  "#666666"  # Light-muted text for hints (light gray)
muted-dark =  "#bbbbbb"  # Dark-muted text (gray with a slight purplish tint)


[light.surface]
disabled =  "#bbbbbb"  # Disabled items (dark gray)
neutral =  "#cccccc"  # Neutral surface for cards, panels (dark gray with slight blue undertones)
highlight =  "#ff0f0f"  # Selection and highlights (neon cyan)


[light.accent]
light =  "#00ff80"  # Light accent (neon pink)
pink =  "#00ff80"  # Pink accent (neon pink)
purple =  "#63ff00"  # Purple accent (electric purple)
red =  "#00e8bb"  # Red for errors and warnings (bright neon red)
orange =  "#0092ff"  # Orange for alerts (vibrant neon orange)
yellow =  "#0015ff"  # Yellow for highlights (electric yellow)
green =  "#ff00ff"  # Green for success (neon green)
teal =  "#ff4c4c"  # Teal for information (bright cyan)
blue =  "#ff2f00"  # Blue for links and actions (electric blue)
light-blue =  "#ff2f00"  # Sky blue accent (electric blue)
lavender =  "#4f7b00"  # Lavender for subtle highlights (neon lavender)


[light.general]
bar-background =  "rgba(237, 237, 237, 0.8)"  # Panel background (semi-transparent dark background)
shadow-color =  "rgba(255, 255, 255, 0.6)"  # Shadow color (deep shadows with high contrast)

```

## Enable Your Theme

Set the theme name in `config.toml` under styling:

```toml
[styling]
theme_name = "my-theme"
```

Then restart Tsumiki or reload your setup.

## Variable Groups

Use these groups as your mental model while editing:

- `background*`: panel and popup backgrounds.
- `text*`: content readability and emphasis.
- `surface*`: cards, buttons, and hover states.
- `accent*`: semantic colors for actions and status.
- `bar-background`, `shadow-color`, `ws-*`: bar-specific polish.

## Good Theme Practices

1. Keep text contrast high against background colors.
2. Reserve strong accent colors for important states.
3. Keep similar saturation across related colors.
4. Test common surfaces: bar, quick settings, notifications, popups.

## Example: Ocean Theme

```toml
[dark.background]
main =  "#1e1e2e"  # Main background
alt =  "#181825"  # Secondary background
dark =  "#11111b"  # Darkest background


[dark.text]
main =  "#cdd6f4"  # Primary text color
secondary =  "#bac2de"  # Secondary text color
muted =  "#a6adc8"  # Tertiary text, muted
disabled =  "#6c7086"  # Text for disabled elements
muted-light =  "#7f849c"  # Light-muted text for hints
muted-dark =  "#9399b2"  # Dark-muted text


[dark.surface]
disabled =  "#313244"  # Background for disabled items
neutral =  "#45475a"  # Neutral surface for cards, panels
highlight =  "#585b70"  # Selection and highlights


[dark.accent]
light =  "#f5e0dc"  # Lightest accent (Rosewater)
pink =  "#f5c2e7"  # Pink accent
purple =  "#cba6f7"  # Mauve accent
red =  "#f38ba8"  # Red for errors and warnings
orange =  "#fab387"  # Orange for warnings and alerts
yellow =  "#f9e2af"  # Yellow for highlights
green =  "#a6e3a1"  # Green for success
teal =  "#94e2d5"  # Teal for information
blue =  "#89b4fa"  # Blue for links and actions
light-blue =  "#89dceb"  # Sky blue accent
lavender =  "#b4befe"  # Lavender for subtle highlights


[dark.general]
bar-background =  "rgb(36, 35, 35)"
shadow-color =  "rgba(0, 0, 0, 0.6)"


[light.background]
main =  "#e1e1d1"  # Main background
alt =  "#e7e7da"  # Secondary background
dark =  "#eeeee4"  # Darkest background


[light.text]
main =  "#32290b"  # Primary text color
secondary =  "#453d21"  # Secondary text color
muted =  "#595237"  # Tertiary text, muted
disabled =  "#938f79"  # Text for disabled elements
muted-light =  "#807b63"  # Light-muted text for hints
muted-dark =  "#6c664d"  # Dark-muted text


[light.surface]
disabled =  "#cecdbb"  # Background for disabled items
neutral =  "#bab8a5"  # Neutral surface for cards, panels
highlight =  "#a7a48f"  # Selection and highlights


[light.accent]
light =  "#0a1f23"  # Lightest accent (Rosewater)
pink =  "#0a3d18"  # Pink accent
purple =  "#345908"  # Mauve accent
red =  "#0c7457"  # Red for errors and warnings
orange =  "#054c78"  # Orange for warnings and alerts
yellow =  "#061d50"  # Yellow for highlights
green =  "#591c5e"  # Green for success
teal =  "#6b1d2a"  # Teal for information
blue =  "#764b05"  # Blue for links and actions
light-blue =  "#762314"  # Sky blue accent
lavender =  "#4b4101"  # Lavender for subtle highlights


[light.general]
bar-background =  "rgb(36, 35, 35)"
shadow-color =  "rgba(0, 0, 0, 0.6)"


```

## Learn from Existing Themes

Browse `styles/themes/` for references such as `nord.scss`, `dracula.scss`, and `gruvbox.scss`.
