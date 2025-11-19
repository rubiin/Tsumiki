---
title: waybar.py
description: waybar.py manual page
---

## Name

`waybar.py` - HyDE Waybar configuration management script

## Synopsis

```
waybar.py [-h] [--set SET] [-n] [-p] [-u] [-g] [-i] [-b] [-G] 
          [-c CONFIG] [-s STYLE] [-w] [--json] [--select] [--kill] 
          [--hide [{0,1,toggle}]]
```

## Description

`waybar.py` is a comprehensive Waybar configuration management script that is part of the HyDE, your Development Environment.

The script manages Waybar configurations stored in `~/.config/waybar/layouts/` and their corresponding styles in `~/.config/waybar/styles/`. It automatically handles the generation of includes files, icon sizing, border radius updates, and provides seamless switching between different Waybar configurations.

## Options

### Layout Management

**`--set SET`**
: Set a specific layout by name. The layout file should exist in `~/.config/waybar/layouts/` with a `.jsonc` extension.

**`-n, --next`**
: Switch to the next available layout in alphabetical order. Cycles through all layouts in the layouts directory.

**`-p, --prev`**
: Switch to the previous available layout in alphabetical order. Cycles through all layouts in the layouts directory.

### Update Operations

**`-u, --update`**
: Perform a complete update of all Waybar components including:
  - Icon size configurations in JSON files
  - Border radius in CSS files  
  - Includes.json file generation
  - Configuration and style synchronization

**`-g, --update-global-css`**
: Update only the global.css file. This file contains dynamic font-size and font-family configurations that can be overridden by themes via `hypr.theme` >> `$BAR_FONT`.

**`-i, --update-icon-size`**
: Update icon size configurations in JSON files. This resolves icon sizing that cannot be handled directly by Waybar's CSS.

**`-b, --update-border-radius`**
: Update border radius configurations in CSS files. This creates dynamic border radius for groups that adapts to Hyprland's corner rounding settings.

**`-G, --generate-includes`**
: Generate the `includes.json` file. This file contains:
  - All modules from `~/.config/waybar/modules/`
  - Dynamic configurations that Waybar doesn't provide natively
  - Icon size resolutions for proper styling

### Configuration Paths

**`-c CONFIG, --config CONFIG`**
: Specify the path to a source `config.jsonc` file. This allows using configurations outside the standard layouts directory.

**`-s STYLE, --style STYLE`**
: Specify the path to a source `style.css` file. This allows using styles outside the standard styles directory.

### Process Management

**`-w, --watch`**
: Enable watch mode. Continuously monitor Waybar and automatically restart it if the process dies. Useful for maintaining a persistent Waybar instance.

**`--kill, -k`**
: Kill all running Waybar instances and any associated watcher scripts. This provides a clean way to terminate all Waybar processes.

**`--hide [{0,1,toggle}]`**
: Control Waybar visibility:
  - `--hide 0` or `--hide show`: Show Waybar
  - `--hide 1` or `--hide hide`: Hide Waybar  
  - `--hide` or `--hide toggle`: Toggle current visibility state

### Information and Listing

**`--json, -j`**
: List all available layouts in JSON format. Useful for scripting and integration with other tools.

**`--select, -S`**
: Open an interactive rofi menu to select and switch between available layouts. This provides a visual interface for browsing and selecting from all layout configurations in `~/.config/waybar/layouts/`.

**`-h, --help`**
: Display help message with all available options and exit.

## Files

**`~/.config/waybar/`**
: Main Waybar configuration directory for user customizations

**`~/.config/waybar/layouts/`**
: Directory containing Waybar layout configuration files (`.jsonc` format)

**`~/.config/waybar/styles/`**
: Directory containing CSS style files corresponding to layouts

**`~/.config/waybar/modules/`**
: Directory containing individual module configurations

**`~/.config/waybar/includes/`**
: Directory containing generated include files and dynamic configurations

**`~/.config/waybar/includes/includes.json`**
: Auto-generated file containing all module definitions and dynamic configurations

**`~/.config/waybar/config.jsonc`**
: Current active Waybar configuration (transient file, copy of selected layout)

**`~/.config/waybar/style.css`**
: Current active Waybar style (auto-generated, imports multiple CSS files)

**`~/.local/share/waybar/`**
: HyDE-provided Waybar configurations (read-only, do not edit)

## Examples

### Basic Layout Management

Select a layout interactively:
```bash
waybar.py --select       # Opens rofi layout selector
```

Switch to a specific layout:
```bash
waybar.py --set khing
```

Cycle through layouts:
```bash
waybar.py --next     # Next layout
waybar.py --prev     # Previous layout
```

### Configuration Updates

Update all configurations:
```bash
waybar.py --update
```

Update specific components:
```bash
waybar.py --update-icon-size        # Update icon sizes only
waybar.py --update-border-radius    # Update border radius only
waybar.py --generate-includes       # Regenerate includes.json
```

### Process Management

Start Waybar with watch mode:
```bash
waybar.py --watch
```

Control Waybar visibility:
```bash
waybar.py --hide 1       # Hide Waybar
waybar.py --hide 0       # Show Waybar  
waybar.py --hide toggle  # Toggle visibility
```

Kill all `waybar.py` processes which effectively kill `--watch` mode:

```bash
waybar.py --kill
```

### Information Gathering

Interactive layout selection:
```bash
waybar.py --select       # Opens rofi menu for layout selection
```

List available layouts:
```bash
waybar.py --json         # JSON format for scripting
```

### Custom Configuration Paths

Use custom configuration files:
```bash
waybar.py --config /path/to/custom-config.jsonc --style /path/to/custom-style.css
```

## Configuration Workflow

1. **Browse and select layouts**: Use `waybar.py --select` to open an interactive rofi menu and preview available layouts

2. **Create or copy a layout**: Start with an existing layout from `~/.local/share/waybar/layouts/` or create a new one in `~/.config/waybar/layouts/`

3. **Generate includes**: Run `waybar.py --generate-includes` to ensure all modules are available

4. **Set the layout**: Use `waybar.py --set <layout-name>` to activate your configuration, or use the interactive selector with `waybar.py --select`

5. **Update configurations**: Run `waybar.py --update` after making changes to ensure all components are synchronized

## Integration with HyDE

`waybar.py` is tightly integrated with the HyDE ecosystem:

- **Theme Integration**: Automatically adapts to current HyDE theme settings
- **Dynamic Styling**: Updates border radius based on Hyprland window rounding
- **Font Management**: Synchronizes fonts with HyDE theme configurations  
- **Module System**: Manages HyDE-specific Waybar modules and configurations


## Notes

- Always use `~/.config/waybar/` for custom configurations, never edit files in `~/.local/share/waybar/`
- The `includes.json` file is auto-generated and should not be manually edited
- Layout names correspond to filenames without the `.jsonc` extension
- Style files should match layout names for automatic pairing (e.g., `khing.jsonc` uses `khing.css`)



