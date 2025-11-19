---
title: HyprPanel
description: HyprPanel wallbash template
---

![241005_14h24m09s_screenshot](https://github.com/user-attachments/assets/355aa7f0-856b-47f6-8ced-58bc0c4a3481)
![241005_14h26m11s_screenshot](https://github.com/user-attachments/assets/e7551bec-573c-4d37-91b9-de9400176cac)
![241005_14h19m51s_screenshot](https://github.com/user-attachments/assets/11f40837-08fe-4979-b16e-b1d0a6fd4fcd)


### Wallbash Template for HyprPanel

This template is designed for use with HyprPanel. For more information, visit [HyprPanel](https://hyprpanel.com/).

> **NOTE:** This is not a standalone package. Ensure you have HyDe installed and a working HyprPanel setup.

## Usage

Add the file [/hyprpanel.dcol](https://github.com/HyDE-Project/HyprPanel/blob/3f20c8922d7c3547688a2b16eb74846170a9f224/hyprpanel.dcol) to either `~/.config/hyde/wallbash/Wall-Ways` or `~/.config/hyde/wallbash/Wall-Dcol`.

### Difference Between Wall-Ways and Wall-Dcol

- **Wall-Ways**: This file is always used regardless of the theme mode or wallbash mode.
- **Wall-Dcol**: This file attempts to find the theme template (if in theme mode) and falls back to using the dominant color of the wallpapers if no template is available.

### Using This Template for Themes

1. **Header Line**:
    ```sh
    ${cacheDir}/landing/hyprpanel_wallbash.json | ags -r "useTheme('${cacheDir}/landing/hyprpanel_wallbash.json')"
    ```
    This command sets the theme using the cached wallbash-generated `.json` file.
    `$cacheDir` is the path to `~/.cache/hyde/`.

2. **Wallbash Generation**:
    ```sh
    ${cacheDir}/landing/hyprpanel_wallbash.json
    ```
    This command generates the wallbash `.json` file.

3. **Optional Command**:
    ```sh
    ags -r "useTheme('${cacheDir}/landing/hyprpanel_wallbash.json')"
    ```
    This command uses the cached wallbash-generated `.json` file to set the theme.
