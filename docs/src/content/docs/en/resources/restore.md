---
title: Restore Configuration
description: Restore script's logic
---

:::note

"restore" in further context is restoring the dotfiles from the repository to your $HOME, not the other way around.

```sh
./restore_cfg.sh </path/to/file.psv > <optional /path/to/hyde/clone>
```

:::

## Pipe Separated Values (PSV)

This is a pipe-separated value file. It contains the paths of the dotfiles and their respective package dependencies.

#### Note:

- Lines starting with `#` are comments.
- The only known variable is `${HOME}`.
- This is a 4-column file separated by `|`.
- Each column should use spaces to separate array elements.

#### Structure:

```shell
flag|path|target|dependency
```

#### Flags:

- **( P ) Populate/Preserved**

  - This flag ensures that the target is only copied if it does not already exist. It is useful for preserving the current state of the target, preventing any overwrites or modifications to existing files or directories.

- **( S ) Sync**

  - If the target file(s) exist, overwrite them.
  - If the target is a directory, only overwrite the files that are listed.
  - Preserve other files in the target directory that are not listed.
  - This behavior is similar to the `cp -r` command.

- **( O ) Overwrite**

  - This flag performs an aggressive sync operation. It ensures that the target is completely replaced by the source.
  - If the target is a directory, every file and subdirectory within it will be overwritten by the corresponding items from the source.
  - If the target is a file, it will be entirely overwritten by the source file.
  - This operation does not preserve any existing files or directories in the target location; everything is replaced.
  - Useful for updating core configurations and scripts.

- **( B ) Backup**
  - Backup the target.
  - All P, S, O flags will also backup the target file/directory.

<details>
<summary>Sample PSV file</summary>

```shell
 Hyde core files 
P|${HOME}/.config/hyde|config.toml|hyprland
P|${HOME}/.config/hypr|hyde.conf animations.conf windowrules.conf keybindings.conf userprefs.conf monitors.conf|hyprland
P|${HOME}/.config/hypr|nvidia.conf|hyprland nvidia-utils
P|${HOME}/.config/hypr/themes|theme.conf wallbash.conf colors.conf|hyprland
P|${HOME}/.local/state|hyde|hyprland

S|${HOME}/.config/hypr|hyprland.conf|hyprland
S|${HOME}/.local|bin|hyprland
S|${HOME}/.config|gtk-3.0|nwg-look
S|${HOME}/.config|nwg-look|nwg-look
S|${HOME}/.config|xsettingsd|nwg-look
S|${HOME}|.gtkrc-2.0|nwg-look
S|${HOME}/.config|Kvantum|kvantum
S|${HOME}/.config|qt5ct|qt5ct
S|${HOME}/.config|qt6ct|qt6ct
S|${HOME}/.config/hyde|wallbash|hyprland
S|${HOME}/.config/hypr|animations|hyprland

O|${HOME}/.local/share|hyde|hyprland
O|${HOME}/.local/lib|hyde|hyprland

 Editor 
P|${HOME}/.config/Code - OSS/User|settings.json|code
P|${HOME}/.config/Code/User|settings.json|visual-studio-code-bin
P|${HOME}/.config/VSCodium/User|settings.json|vscodium-bin

 Bar 
P|${HOME}/.config/waybar|config.ctl|waybar
S|${HOME}/.config/waybar|modules config.jsonc theme.css style.css|waybar

 Terminal 
P|${HOME}/.config|lsd|lsd
S|${HOME}/.config|fastfetch|fastfetch
S|${HOME}/.config/kitty|hyde.conf theme.conf|kitty
P|${HOME}/.config/kitty|kitty.conf|kitty

 Shell 
P|${HOME}/.config|fish|fish
P|${HOME}|.zshrc .hyde.zshrc .p10k.zsh|zsh zsh-theme-powerlevel10k pokego-bin
S|${HOME}|.zshenv|zsh zsh-theme-powerlevel10k

 File Explorer 
P|${HOME}/.local/state|dolphinstaterc|dolphin
P|${HOME}/.config|baloofilerc|dolphin
S|${HOME}/.config/menus|applications.menu|dolphin
S|${HOME}/.config|dolphinrc|dolphin
S|${HOME}/.config|kdeglobals|dolphin
S|${HOME}/.local/share/kio/servicemenus|hydewallpaper.desktop|dolphin
S|${HOME}/.local/share/kxmlgui5|dolphin|dolphin
S|${HOME}/.local/share|dolphin|dolphin

 Input 
P|${HOME}/.config|libinput-gestures.conf|libinput-gestures

 Wayland 
P|${HOME}/.config|spotify-flags.conf|spotify
P|${HOME}/.config|code-flags.conf|code
P|${HOME}/.config|code-flags.conf|visual-studio-code-bin
P|${HOME}/.config|vscodium-flags.conf|vscodium-bin
P|${HOME}/.config|electron-flags.conf|electron

 Notifications 
S|${HOME}/.config|dunst|dunst

 Gaming 
S|${HOME}/.config|MangoHud|mangohud

 Launcher 
S|${HOME}/.config|rofi|rofi
S|${HOME}/.config|wlogout|wlogout

 Lock Screen 
S|${HOME}/.config|swaylock|swaylock-effects
P|${HOME}/.config/hypr|hyprlock.conf|hyprlock
S|${HOME}/.config/hypr|hyprlock|hyprlock

 Idle daemon 
P|${HOME}/.config/hypr|hypridle.conf|hypridle
```

</details>

## TOML Configuration

🚧 🚧 WIP 🚧🚧

PSV configuration file is convenient for the script to read and write. However, it is very restrictive and not user-friendly.
For further customization, we can use TOML configuration files.

...
