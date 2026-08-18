---
title: SCSS Customization
description: Advanced SCSS theming and variable customization in Tsumiki
sidebar:
  order: 3
---

Beyond theme colors, Tsumiki exposes SCSS variables for fine-grained control over widget appearance, spacing, and layout.

## How SCSS Works

Tsumiki compiles SCSS from `styles/main.scss` into CSS using `dart-sass`. The compilation chain is:

1. **Theme variables** — defined in `themes/*.toml`, compiled into `styles/_theme.scss`
2. **SCSS settings** — auto-generated from `config.toml` styling section into `styles/_settings.scss`
3. **Widget styles** — individual `_widgetname.scss` files import variables and compose styles
4. **Output** — `dist/main.css` is loaded by the application

## Configuration-Based Variables

Some SCSS variables can be set directly from `config.toml` under `[styling]`:

```toml
[styling]
theme_name = "catpuccin-mocha"

[styling.bar]
background = "#1e1e2e"
border-color = "#313244"
border-radius = 16
border-enabled = true
border-width = 2
padding = "4px 12px"
margin = "0 8px"

[styling.bar.widgets]
gap = 2

[styling.bar.widgets.workspaces]
spacing = 4
icon_size = 14
border-radius = 16
border-enabled = false
border-width = 1
pill-active_width = "1em"
pill-height = "2px"
pill-width = "0.5em"
pill-border-enabled = false
pill-border-radius = 16
pill-border-width = 2

[styling.bar.widgets.workspaces.border]
color = "#cba6f7"
```

## SCSS Variable Reference

Variables are defined in `styles/_variable.scss` and `styles/_settings.scss`.

### Bar Variables

| Variable              | Default     | Description                                    |
| --------------------- | ----------- | ---------------------------------------------- |
| `$bar-background`     | theme color | Bar background color                           |
| `$bar-border-color`   | theme color | Bar border color                               |
| `$bar-border-radius`  | `16px`      | Bar corner radius                              |
| `$bar-border-enabled` | `false`     | Enable bar border                              |
| `$bar-border-width`   | `1px`       | Bar border thickness                           |
| `$bar-padding`        | `4px 12px`  | Bar internal padding                           |
| `$bar-margin`         | `0 8px`     | Bar external margin                            |
| `$bar-widgets-gap`    | `2px`       | Gap between bar widgets (applied on each side) |

### Workspace Variables

| Variable                                      | Default   | Description                        |
| --------------------------------------------- | --------- | ---------------------------------- |
| `$bar-widgets-workspaces-spacing`             | `0.125em` | Spacing between workspace buttons  |
| `$bar-widgets-workspaces-icon_size`           | `12px`    | Icon size within workspace buttons |
| `$bar-widgets-workspaces-border-radius`       | `16px`    | Workspace widget border radius     |
| `$bar-widgets-workspaces-border-enabled`      | `false`   | Enable workspace widget border     |
| `$bar-widgets-workspaces-border-width`        | `1px`     | Workspace widget border thickness  |
| `$bar-widgets-workspaces-pill-height`         | `1px`     | Pill indicator height              |
| `$bar-widgets-workspaces-pill-width`          | `0.5em`   | Pill indicator width               |
| `$bar-widgets-workspaces-pill-active_width`   | `1em`     | Active pill expanded width         |
| `$bar-widgets-workspaces-pill-border-enabled` | `false`   | Enable pill border                 |
| `$bar-widgets-workspaces-pill-border-radius`  | `16px`    | Pill border radius                 |
| `$bar-widgets-workspaces-pill-border-width`   | `2px`     | Pill border thickness              |

### Common Widget Variables

Each widget that displays an icon has size and spacing variables following this pattern:

```
$bar-widgets-<name>-icon_size
$bar-widgets-<name>-spacing
```

Common examples:

| Variable                           | Default | Widgets              |
| ---------------------------------- | ------- | -------------------- |
| `$bar-widgets-cpu-icon_size`       | `12px`  | CPU, Memory, Storage |
| `$bar-widgets-battery-icon_size`   | `14px`  | Battery              |
| `$bar-widgets-volume-icon_size`    | `14px`  | Volume               |
| `$bar-widgets-bluetooth-icon_size` | `14px`  | Bluetooth            |
| `$bar-widgets-weather-icon_size`   | `14px`  | Weather              |

### Layout Variables

| Variable               | Default       | Description                         |
| ---------------------- | ------------- | ----------------------------------- |
| `$quicksettings-width` | `370px`       | Quick settings panel width          |
| `$radius-large`        | `9999px`      | Large border radius (fully rounded) |
| `$radius`              | from config   | Default border radius               |
| `$border-color`        | theme color   | Default border color                |
| `$border`              | from settings | Border shorthand                    |

## Overriding SCSS

To permanently override a variable:

1. Copy the relevant `_settings.scss` variable into your custom theme.
2. Or set the value under `[styling]` in `config.toml` (for supported variables).
3. Recompile with `./init.sh -recompile`.

## Per-Widget Style Classes

Widget groups and individual widgets can use custom style classes:

```toml
[[widget_groups]]
widgets = ["workspaces", "window_title"]
spacing = 2
style_classes = ["compact"]     # Tighter spacing variant
```

Available built-in style classes:

| Class      | Effect                         |
| ---------- | ------------------------------ |
| `compact`  | Reduced padding and spacing    |
| `bordered` | Adds a border around the group |
| `pill`     | Pill-shaped container          |

## Adding Custom CSS

You can add custom CSS rules directly:

1. Create `styles/custom.scss`
2. Import it in `styles/main.scss`:
   ```scss
   @use "custom.scss";
   ```
3. Recompile: `./init.sh -recompile`

## Transition Animations

Workspace buttons use a shared transition variable:

```scss
$workspace-transition:
  padding 0.3s cubic-bezier(0.4, 0, 0.2, 1),
  background-color 0.4s cubic-bezier(0.4, 0, 0.2, 1);
```

You can override this in your custom SCSS for different animation curves.
