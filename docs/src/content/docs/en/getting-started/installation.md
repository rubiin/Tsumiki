---
title: Installation
description: HyDE Installation guide
---

The installation script is designed for a minimal [Arch Linux](https://wiki.archlinux.org/title/Arch_Linux) install, but **may** work on some [Arch-based distros](https://wiki.archlinux.org/title/Arch-based_distributions).
While installing HyDE alongside another [DE](https://wiki.archlinux.org/title/Desktop_environment)/[WM](https://wiki.archlinux.org/title/Window_manager) should work, due to it being a heavily customized setup, it **will** conflict with your [GTK](https://wiki.archlinux.org/title/GTK)/[Qt](https://wiki.archlinux.org/title/Qt) theming, [Shell](https://wiki.archlinux.org/title/Command-line_shell), [SDDM](https://wiki.archlinux.org/title/SDDM), [GRUB](https://wiki.archlinux.org/title/GRUB), etc. and is at your own risk.

For Nixos support there is a separate project being maintained @ [Hydenix](https://github.com/richen604/hydenix/tree/main)

:::note

The install script will auto-detect an NVIDIA card and install nvidia-dkms drivers for your kernel.
Please ensure that your NVIDIA card supports dkms drivers in the list provided [here](https://wiki.archlinux.org/title/NVIDIA).
:::

:::danger

The script modifies your `grub` or `systemd-boot` config to enable NVIDIA DRM.

:::

<!-- ### Option 1 -->

### Automated installation script

```shell
pacman -S --needed git base-devel
git clone --depth 1 https://github.com/HyDE-Project/HyDE ~/HyDE
cd ~/HyDE/Scripts
./install.sh
```

:::tip
You can also add any other apps you wish to install alongside HyDE to `Scripts/pkg_user.lst` and pass the file as a parameter to install it like so:

```shell
./install.sh pkg_user.lst
```

:::

:::note
Refer your list from `Scripts/pkg_extra.lst`
or you can `cp  Scripts/pkg_extra.lst Scripts/pkg_user.lst` if you wish to install all extra packages.
:::

### Granular and Manual Installation

#### Clone

Clone the repo and change the directory to the script path. Then make sure the user has [w]rite and e[x]ecute permission to the clone directory

```shell
pacman -Sy git
git clone --depth 1 https://github.com/HyDE-Project/HyDE ~/HyDE
cd ~/HyDE/Scripts
```

:::caution
**NEVER** ever execute the script with sudo or as root user!
:::

#### Modes

The install script can be executed in different modes,

- for default full hyprland installation with all configs

```shell
./install.sh
```

- for full or minimal hyprland installation + your favorite packages (ex.`pkg_user.lst`)

```shell
./install.sh pkg_user.lst # full install pkg_core.lst + pkg_user.lst with configs
./install.sh -i pkg_user.lst # minimal install pkg_core.lst + pkg_user.lst without configs
```

- each [section](#process) can also be independently executed as,

```shell
./install.sh -i # minimal install hyprland without any configs
./install.sh -d # minimal install hyprland without any configs, but with (--noconfirm) install
./install.sh -r # just restores the config files
./install.sh -s # start and enable system services
./install.sh -t # test run without executing (-irst to dry run all)
./install.sh -m # skips the theme installation
./install.sh -n # skips nvidia installation
./install.sh -irst # to do a test run for all
```

<!-- ### Option 2

:::caution

HyDE-CLI author here.
The CLI's dots management (Hyde {restore,backup,control,override}) is not yet and might not be 100% compatible of the current hyprdots.
This is due to incompatibility of the meta files
and the above commands need manual intervention
Rest assured that other commands are working perfectly
and will be ported to its own `hydectl` command line interface

:::

As a second install option, you can also use `Hyde-install`, which might be easier for some.
View installation instructions for HyDE in [Hyde-cli - Usage](https://github.com/kRHYME7/Hyde-cli?tab=readme-ov-file#usage).

### Option 3

...Soon
A declarative way to manage importing and exporting dotfiles from other users. This is not for boot strapping but for sharing dotfiles.

---

---

---

:::note

> Please reboot after the install script completes and takes you to the SDDM login screen (or black screen) for the first time.
> ::: -->
