---
title: Making Themes
description: How to make themes for Tsumiki
---

Here we will walk you through the process of making themes for Tsumiki step by step.


## Theme File Location

All theme files are located in `styles/themes/` and use the `.scss` extension.

## Theme Structure

A theme file defines SCSS variables that control the appearance of the entire application. Copy the template below and customize the color values.

### Template

```scss
/* ---------------------------- */
/* Base Colors                  */
/* ---------------------------- */
$background: #1e1e2e; // Main background
$background-alt: #181825; // Secondary background (elevated surfaces)
$background-dark: #11111b; // Darkest background (popups, dropdowns)

/* Text Colors */
$text-main: #cdd6f4; // Primary text color
$text-secondary: #bac2de; // Secondary text color
$text-muted: #a6adc8; // Tertiary text, muted
$text-disabled: #6c7086; // Text for disabled elements

/* Surface Colors */
$surface-disabled: #313244; // Background for disabled items
$surface-neutral: #45475a; // Neutral surface for cards, panels
$surface-highlight: #585b70; // Selection and highlights

/* Accent Colors */
$accent-light: #f5e0dc; // Lightest accent
$accent-pink: #f5c2e7; // Pink accent
$accent-purple: #cba6f7; // Purple accent
$accent-red: #f38ba8; // Red for errors
$accent-orange: #fab387; // Orange for warnings
$accent-yellow: #f9e2af; // Yellow for highlights
$accent-green: #a6e3a1; // Green for success
$accent-teal: #94e2d5; // Teal for information
$accent-blue: #89b4fa; // Blue for links and actions
$accent-light-blue: #89dceb; // Sky blue accent
$accent-lavender: #b4befe; // Lavender for subtle highlights

/* Additional UI Elements */
$bar-background: rgb(36, 35, 35); // Status bar background
$shadow-color: rgba(0, 0, 0, 0.6); // Drop shadows
$ws-active: $text-muted; // Active workspace indicator
$ws-hover: $accent-pink; // Workspace hover state
```

## Variable Reference

### Background Colors

| Variable | Purpose | Usage |
|----------|---------|-------|
| `$background` | Main application background | Primary window/panel background |
| `$background-alt` | Elevated surfaces | Cards, secondary panels, menus |
| `$background-dark` | Darkest background | Popups, dropdowns, overlays |
| `$bar-background` | Status bar | Top/bottom bar background |

### Text Colors

| Variable | Purpose | Usage |
|----------|---------|-------|
| `$text-main` | Primary text | Headings, important content |
| `$text-secondary` | Secondary text | Descriptions, subtitles |
| `$text-muted` | Muted text | Placeholders, hints |
| `$text-disabled` | Disabled text | Inactive/disabled elements |

### Surface Colors

| Variable | Purpose | Usage |
|----------|---------|-------|
| `$surface-disabled` | Disabled backgrounds | Inactive buttons, disabled inputs |
| `$surface-neutral` | Neutral surfaces | Cards, panels, input backgrounds |
| `$surface-highlight` | Highlighted surfaces | Hover states, selections |

### Accent Colors

| Variable | Purpose | Semantic Meaning |
|----------|---------|------------------|
| `$accent-blue` | Primary accent | Links, primary actions, focus states |
| `$accent-light-blue` | Secondary blue | Alternative links, secondary info |
| `$accent-purple` | Tertiary accent | Tags, badges, decorative elements |
| `$accent-lavender` | Subtle accent | Soft highlights, borders |
| `$accent-pink` | Decorative | Playful elements, notifications |
| `$accent-light` | Lightest accent | Subtle backgrounds, borders |

### Semantic Colors

| Variable | Purpose | When to Use |
|----------|---------|-------------|
| `$accent-green` | Success | Confirmations, completed states, positive feedback |
| `$accent-teal` | Information | Info messages, neutral notifications |
| `$accent-yellow` | Warning | Caution states, pending actions |
| `$accent-orange` | Alert | Important warnings, attention required |
| `$accent-red` | Error/Danger | Errors, destructive actions, critical alerts |

### UI Element Colors

| Variable | Purpose |
|----------|---------|
| `$shadow-color` | Box shadows (use rgba for transparency) |
| `$ws-active` | Active workspace indicator color |
| `$ws-hover` | Workspace hover state color |

## Color Guidelines

### Contrast Requirements

1. **Text on backgrounds**: Ensure sufficient contrast between text colors and backgrounds
   - `$text-main` on `$background` should have high contrast
   - `$text-secondary` can have slightly lower contrast
   - `$text-muted` can be subtle but still readable

2. **Text on accents**: When placing text on accent-colored backgrounds, use `$background` or `$background-dark` for the text color

### Color Harmony

For a cohesive theme:

1. **Choose a base palette**: Start with 2-3 related hues
2. **Define variations**: Create light/dark/muted versions
3. **Accent sparingly**: Use bright accents for emphasis only
4. **Maintain consistency**: Keep similar saturation levels across accents

## Step-by-Step Creation

1. **Create the file**:
   ```bash
   touch styles/themes/my-theme.scss
   ```

2. **Copy the template** from above

3. **Define your color palette**:
   - Pick a background color family
   - Choose complementary accent colors
   - Ensure text colors have good contrast

4. **Test the theme**:
   - Update `theme.toml` with your theme name:
     ```toml
     [theme]
     name = "my-theme"
     ```
   - Restart Tsumiki or trigger a theme reload

5. **Iterate**: Adjust colors based on how they look in the actual UI

## Example: Creating a "Ocean" Theme

```scss
/* Ocean Theme - Cool blues and teals */

/* Base Colors */
$background: #0d1b2a;
$background-alt: #1b263b;
$background-dark: #0a1628;

/* Text Colors */
$text-main: #e0e1dd;
$text-secondary: #b0b3ae;
$text-muted: #778da9;
$text-disabled: #415a77;

/* Surface Colors */
$surface-disabled: #1b263b;
$surface-neutral: #2b3a4d;
$surface-highlight: #3d5a80;

/* Accent Colors */
$accent-light: #caf0f8;
$accent-pink: #f72585;
$accent-purple: #7209b7;
$accent-red: #ef476f;
$accent-orange: #f77f00;
$accent-yellow: #fcbf49;
$accent-green: #06d6a0;
$accent-teal: #48cae4;
$accent-blue: #00b4d8;
$accent-light-blue: #90e0ef;
$accent-lavender: #ade8f4;

/* UI Elements */
$bar-background: #0d1b2a;
$shadow-color: rgba(0, 0, 0, 0.5);
$ws-active: $text-muted;
$ws-hover: $accent-teal;
```

## Tips

- Use **hex colors** (`#rrggbb`) or **rgba** (`rgba(r, g, b, a)`) for transparency
- Reference other variables using `$variable-name` syntax
- Test in both light and dark environments
- Check all widgets: bar, notifications, menus, popups

## Available Themes

Browse existing themes in `styles/themes/` for inspiration:
- `catpuccin-mocha.scss` - Warm, cozy dark theme
- `nord.scss` - Cool, Arctic-inspired palette
- `dracula.scss` - Dark theme with vibrant accents
- `gruvbox.scss` - Retro, earthy tones
- `tokyonight.scss` - Modern, purple-blue dark theme
