# HyDePanel

<p align="center">
 <a href="https://github.com/rubiin/HyDePanel/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/rubiin/HyDePanel"></a>
  <a href='http://makeapullrequest.com'><img alt='PRs Welcome' src='https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields'/></a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/rubiin/HyDePanel"/>
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/rubiin/HyDePanel"/>
  <img alt="discord" src="https://img.shields.io/discord/1200448076620501063" />

</p>

A semi-customizable bar written using the [Fabric Widget System](https://github.com/Fabric-Development/fabric) taking inpirations from hyprpanel and waybar for some widgets
More on [Fabric's Wiki](https://wiki.ffpy.org)

The panel focuses on providing an all-in-one, fully integrated panel experience, where users don’t have to rely on separate, theme-less third-party tools to manage niche functions like buetooth, notifications,on screen display.
Many aspects of the bar including the look and functionalities are inspired from [waybar](https://github.com/Alexays/Waybar), [hyprpanel](https://hyprpanel.com) and [swayosd](https://github.com/ErikReider/SwayOSD).

---

## Prerequisites

- [JetBrains Nerd Font](https://www.nerdfonts.com)
- [python 3+](https://www.python.org/downloads/)

---

## **Installation**

### Required

Most of these are already installed on existing working machines

```sh
networkmanager

pipewire


## Bluetooth menu utilities
gnome-bluetooth
bluez
bluez-utils

## Copy/Paste utilities
wl-clipboard

## Compiler for sass/scss
dart-sass

## Brightness module for OSD
brightnessctl
```

### Optional

```sh

## To check for pacman updates in the default script used in the updates module
pacman-contrib

## To record screen through the dashboard record shortcut
wf-recorder

## To enable the eyedropper color picker with the default snapshot shortcut in the dashboard
hyprpicker

## To enable hyprland's very own blue light filter
hyprsunset

## To enable hyprland's very own idle inhibitor
hypridle

```

- Clone this repository:

```sh
git clone https://github.com/rubiin/HyDePanel.git bar
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
sudo pacman -S pipewire playerctl dart-sass networkmanager wl-clipboard brightnessctl python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-cairo python-loguru pkgconf wf-recorder kitty grimblast gnome-bluetooth
```

#### Step 2: Install AUR Packages with `yay`

Use `yay` to install the required AUR packages:

```sh
yay -S gray-git python-fabric
```

#### Step 3: Run the `init.sh -start` Script

Once the dependencies are installed, run the following command to start the bar or environment:

```sh
./init.sh -start
```

## **Usage**

### **For Hyprland:**

Add this to your `.config/hyprland.conf`

```sh
exec = `$HOME/bar/init.sh -start`

```

> **Note**: modify the path accordingly

### **For Other Window Managers:**

Use a similar configuration for your respective window manager's autostart setup.

## Updating

Updating to latest commit is fairly simple, just git pull the latest changes.

> **Note**: make sure to keep the config safe just in case

## Check wiki for configuring individual widgets

## **Available Modules**

<details>
<summary>Click to expand modules</summary>

- battery
- bluetooth
- brightness
- clickcounter
- cpu
- workspaces
- date_menu
- hypr_idle
- hypr_sunset
- keyboard
- language
- media
- volume
- power
- ram
- recorder
- storage
- system_tray
- taskbar
- weather
- window_title
- workspace
- updates

</details>

# Screenshots

![image](https://github.com/user-attachments/assets/4bd1fd6d-6c35-43e1-ae47-f0f76089f447)

## Notification

![image](https://github.com/user-attachments/assets/6c66b11c-6a21-4dcb-ab7f-7ed586abbf65)

## Calendar with notification panel

![image](https://github.com/user-attachments/assets/6e3ef49a-64b3-4dbd-8ccd-53430ff6ecff)

## OSD

![image](https://github.com/user-attachments/assets/25e171ff-f85e-4b62-9ed3-8e3479c2e4b4)

## Logout

![image](https://github.com/user-attachments/assets/18b5c851-4d3a-4801-b4c3-dbb555cfbae9)

> [!WARNING]
> This is still in early development and will include breaking changes

## Frequently Asked Questions (FAQ)

### 1. **Cannot see system tray?**

Be sure to kill any bars that you may be running. You can kill other bar with `pkill bar-name`

### 2. **Cannot see bar? **

Kill the app with `pkill hydepanel`. Cd to the folder , activate venv with `source .venv/bin/activate` and run `python main.py`.
This should show some logs. If it shows like `ModuleNotFoundError`, run `pip install -r requirements.txt`.
If this does not solve the issue, do report a bug.

# ⭐ Hit that Star Button!

Like what you see? Think this project is cooler than your morning coffee? ☕✨

Give it a star! It’s like giving a virtual high-five to the code—plus, and who doesn't love high-fives? ✋

Your star helps the project get noticed, and it makes us do a little happy dance. 💃

Just click the shiny "Star" button at the top right (it’s begging for your attention). 🥳

Thanks for making this project a little bit more awesome! 🚀
