---
title: Making Themes
description: How to make themes for Tsumiki
---

This guide walks through creating a custom Tsumiki theme from scratch.

## Where Themes Live

Create your theme file in `styles/themes/` with a `.scss` extension.

Example:

```bash
touch styles/themes/my-theme.scss
```

## Minimum Theme Template

Copy this starter and adjust values:

```scss
/* Base */
$background: #1e1e2e;
$background-alt: #181825;
$background-dark: #11111b;

/* Text */
$text-main: #cdd6f4;
$text-secondary: #bac2de;
$text-muted: #a6adc8;
$text-disabled: #6c7086;

/* Surface */
$surface-disabled: #313244;
$surface-neutral: #45475a;
$surface-highlight: #585b70;

/* Accent */
$accent-light: #f5e0dc;
$accent-pink: #f5c2e7;
$accent-purple: #cba6f7;
$accent-red: #f38ba8;
$accent-orange: #fab387;
$accent-yellow: #f9e2af;
$accent-green: #a6e3a1;
$accent-teal: #94e2d5;
$accent-blue: #89b4fa;
$accent-light-blue: #89dceb;
$accent-lavender: #b4befe;

/* Extras */
$bar-background: #242323;
$shadow-color: rgba(0, 0, 0, 0.6);
$ws-active: $text-muted;

```

## Enable Your Theme

Set the theme name in `theme.toml`:

```toml
[theme]
name = "my-theme"
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

```scss
$background: #0d1b2a;
$background-alt: #1b263b;
$background-dark: #0a1628;

$text-main: #e0e1dd;
$text-secondary: #b0b3ae;
$text-muted: #778da9;
$text-disabled: #415a77;

$surface-disabled: #1b263b;
$surface-neutral: #2b3a4d;
$surface-highlight: #3d5a80;

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

$bar-background: #0d1b2a;
$shadow-color: rgba(0, 0, 0, 0.5);
$ws-active: $text-muted;
$ws-hover: $accent-teal;
```

## Learn from Existing Themes

Browse `styles/themes/` for references such as `nord.scss`, `dracula.scss`, and `gruvbox.scss`.
