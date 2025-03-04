<p align="center"><img src="./assets/hydepanel.png" align="centre" width="100" height="130"/></p>
<h1 align="center"><img src="https://raw.githubusercontent.com/JaKooLit/Telegram-Animated-Emojis/refs/heads/main/Activity/Sparkles.webp"/ height=50> HyDePanel</h1>
<p align="center">
 <a href="https://github.com/rubiin/HyDePanel/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/rubiin/HyDePanel"></a>
  <a href='http://makeapullrequest.com'><img alt='PRs Welcome' src='https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields'/></a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/rubiin/HyDePanel"/>
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/rubiin/HyDePanel"/>
  <img alt="discord" src="https://img.shields.io/discord/1200448076620501063" />
</p>

A semi-customizable bar written using the [Fabric Widget System](https://github.com/Fabric-Development/fabric).
The panel focuses on providing an all-in-one, fully integrated panel experience, where users don’t have to rely on separate, theme-less third-party tools to manage niche functions like bluetooth, notifications and notification panel,on screen display.

<h2><sub><img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Camera%20with%20Flash.png" alt="Camera with Flash" width="25" height="25" /></sub> Screenshots</h2>

<table align="center">
  <tr>
    <td colspan="4"><img src="assets/screenshots/main.png"></td>
  </tr>
    <tr>
    <td colspan="4"><img src="assets/screenshots/main2.png"></td>
  </tr>
  <tr>
    <td colspan="1"><img src="assets/screenshots/quick_settings.png"></td>
    <td colspan="1"><img src="assets/screenshots/noti.png"></td>
    <td colspan="1" align="center"><img src="assets/screenshots/logout.png"></td>
    <td colspan="1" align="center"><img src="assets/screenshots/weather.png"></td>
  </tr>
</table>

<table align="center">
  <tr>
    <td align="center"><sup>✨ sᴜᴘᴘᴏʀᴛ ᴛʜᴇ ᴘʀᴏᴊᴇᴄᴛ ✨</sup></td>
  </tr>
  <tr>
    <td align="center">
      <a href='https://ko-fi.com/rubiin' target='_blank'>
        <img style='border:0px;height:128px;'
             src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3N4NzlvZWs2Z2tsaGx4aHgwa3UzMWVpcmNwZTNraTM2NW84ZDlqbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/PaF9a1MpqDzovyqVKj/giphy.gif'
             border='0' alt='Support me on Ko-fi!' />
      </a>
    </td>
  </tr>
</table>

---

## Prerequisites

- [JetBrains Nerd Font](https://www.nerdfonts.com)
- [python 3+](https://www.python.org/downloads/)

---

## **Installation**

### Required

Most of these are already installed on existing working machines

```sh
## network
networkmanager

## Sound
pipewire

## Bluetooth menu utilities
gnome-bluetooth-3.0 # aur
bluez
bluez-utils

## Compiler for sass/scss
dart-sass

## Brightness module for OSD
brightnessctl
```

## To open and execute commands in a terminal ex: updates, cava

kitty

### Optional

```sh

## To check for updates using the default pacman script in the updates module
pacman-contrib

## To display cava audio visualizer
cava

## To switch between power profiles in the battery module
power-profiles-daemon

## To record screen through recorder module
wf-recorder & slurp

## To activate Hyprland’s native blue light filter
hyprsunset

## To activate Hyprland’s native idle inhibitor
hypridle

## To use media module on quick settings
playerctl

```

- Clone this repository:

```sh
git clone https://github.com/rubiin/HyDePanel.git ~/.config/hydepanel
cd bar
```

- Run the following command to install the required packages for particular os, few of them are already installed if you have a working system:

## Installation

You can choose one of two installation methods: **Automated Setup** or **Manual Setup**.

### Option 1: Automated Setup Using `init.sh -install`

1.  **Run the `init.sh -install` script** to automatically install all the required packages and dependencies (both `pacman` and AUR packages):

```sh
./init.sh -install
```

This script will:

- Install all required `pacman` and AUR packages.
- Set up the virtual environment and any required configurations.

1.  **Start the environment or bar** once the installation is complete:

```sh
./init.sh -start
```

This will launch the environment or bar as defined in your project.

### Option 2: Manual Setup (Install Dependencies First)

If you prefer to have more control over the installation process, you can install the required dependencies manually and then run the `init.sh -start` script.

#### Step 1: Install `pacman` Packages

Run the following command to install the required system packages:

```sh
	sudo pacman -S --noconfirm --needed pipewire playerctl dart-sass power-profiles-daemon networkmanager brightnessctl pkgconf wf-recorder kitty python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-dbus python-cairo python-loguru python-setproctitle
```

#### Step 2: Install AUR Packages

Using `yay` to install the required AUR packages:

```sh
yay -S --needed gray-git python-fabric gnome-bluetooth-3.0 python-rlottie-python slurp
```

If you have something else besides `yay`, install with the respective aur helper.

#### Step 3: Run the `init.sh -start` Script

Once the dependencies are installed, run the following command to start the bar or environment:

```sh
./init.sh -start
```

## **Usage**

Add this to your `.config/hyprland.conf`

```sh
exec = `~/.config/hydepanel/init.sh -start`

```

> **Note**: modify the path accordingly

Check FAQs for common things you are likely to encounter

## Updating

Updating to latest commit is fairly simple, just git pull the latest changes.

> **Note**: make sure to keep the config safe just in case

## Check wiki for configuring individual widgets

## **Available Modules**

| **Item**              | **Description**                                                                |
| --------------------- | ------------------------------------------------------------------------------ |
| **battery**           | Displays battery status and usage information.                                 |
| **bluetooth**         | Manages Bluetooth connections and settings.                                    |
| **brightness**        | Controls the screen brightness level.                                          |
| **cava**              | An audio visualizer.                                                           |
| **clickcounter**      | Tracks the number of mouse clicks.                                             |
| **cpu**               | Displays CPU usage and performance statistics.                                 |
| **date_menu**         | A menu displaying the current date and notifications.                          |
| **divider (utility)** | Separates sections in a user interface for better organization.                |
| **hypr_idle**         | Tracks idle time or status of the system.                                      |
| **hypr_sunset**       | A utility that adjusts screen settings based on the time of sunset.            |
| **keyboard**          | Displays and manages the keyboard layout or settings.                          |
| **language**          | Allows selection of the system's language or locale settings.                  |
| **media**             | Controls media playback, volume, or other media-related settings.              |
| **microphone**        | Manages microphone settings and input levels.                                  |
| **power**             | Controls power-related settings, including sleep and shutdown.                 |
| **ram**               | Displays information about system RAM usage and performance.                   |
| **recorder**          | A tool for recording audio or video on the system.                             |
| **spacer (utility)**  | A simple utility for adding space in UI layouts.                               |
| **storage**           | Displays storage usage and manages disk partitions or drives.                  |
| **submap**            | Displays active submap for hyprland.                                           |
| **network_usage**     | Displays the upload/download speeds.                                           |
| **stop_watch**        | A utility for tracking elapsed time, like a timer or stopwatch.                |
| **system_tray**       | Displays system tray icons and manages notifications.                          |
| **taskbar**           | A bar at the bottom of the screen for quick access to apps and notifications.  |
| **updates**           | Manages system updates, patches, and version upgrades.                         |
| **quicksettings**     | Displays panel for quickly accessing some settings like brightness, sound etc. |
| **volume**            | Controls the system’s audio volume.                                            |
| **weather**           | Displays current weather information or forecasts.                             |
| **window_title**      | Shows the title of the current window or application.                          |
| **workspaces**        | Refers to multiple virtual desktops or workspaces.                             |

> [!WARNING]
> This is still in early development and will include breaking changes

## Frequently Asked Questions (FAQ)

### 1. **Cannot see system tray?**

Be sure to kill any bars that you may be running. You can kill other bar with `pkill bar-name`

### 2. **Cannot see notifications?**

Be sure to kill other notifications daemon that you may be running. You can kill other daeemons with `pkill dunst; pkill mako;`

### 3. **Cannot see bar?**

Kill the app with `pkill hydepanel`. Run `init.sh -start`. This should show some logs. If it shows like `ModuleNotFoundError`, run `pip install -r requirements.txt`. If this does not solve the issue, do report a bug with screenshot of the log.

### 4. **No Blur?**

Add this to your `hyprland.conf`

```conf
layerrule = blur , fabric
layerrule = ignorezero, fabric
layerrule = blur ,gtk-layer-shell
layerrule = ignorezero ,gtk-layer-shell

```

## Contributing

We welcome all sorts of contributions, no matter how small, to this project! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

## Acknowledgements

- **Waybar** - A lot of the initial inspiration, and a pretty great bar.
  [Waybar GitHub Repository](https://github.com/Alexays/Waybar)

- **Hyprpanel** - Served as inspiration for some of the panel's features and design choices, with its focus on dynamic and customizable Hyprland panels.
  [Hyprpanel GitHub Repository](https://github.com/Jas-SinghFSU/HyprPanel)

## Special Thanks

A big thank you to the following people for their amazing help with code, bug fixes, and great ideas:

- [darsh](https://github.com/its-darsh): For creating fabric without which the project wouldn't have existed. Also, your quick feedbacks and problem-solving approach were a game-changer!
- [gummy bear album](https://github.com/muhchaudhary): For providing code snippets which served as a reference to start stuffs. Your creative ideas really pushed the project forward and made it better!
- [axenide](https://github.com/Axenide): For your fresh ideas and design references. Your code improvements and insights made a significant impact
- [sankalp](https://github.com/S4NKALP): For some bug fixes and recommendations,contributions in optimizing the code and identifying subtle bugs during the development period

# ⭐ Hit that Star Button!

Like what you see? Think this project is cooler than your morning coffee? ☕✨

Give it a star! It’s like giving a virtual high-five to the code—plus, and who doesn't love high-fives? ✋

Your star helps the project get noticed, and it makes us do a little happy dance. 💃

Just click the shiny "Star" button at the top right (it’s begging for your attention). 🥳

Thanks for making this project a little bit more awesome! 🚀

## Star History

<a href="https://star-history.com/#rubiin/HyDePanel&Timeline">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline" />
 </picture>
</a>
