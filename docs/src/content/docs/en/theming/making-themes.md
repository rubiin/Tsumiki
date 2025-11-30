---
title: Making Themes
description: How to make themes for HyDE
---

Here we will walk you through the process of making themes for HyDE step by step.
This tutorial will work for both hyprdots and HyDE.

### Quick Start Guide

Clone the hyde-theme-starter repo into your themes directory

:::tip
Rename `MyTheme` to your theme name, make sure it doesn't conflict in names in [HyDE-Gallery](https://github.com/HyDE-Project/hyde-gallery)
:::

```bash
git clone https://github.com/richen604/hyde-theme-starter ~/MyTheme
```

1. Required components - all must be in `tar.*` format:

   - A GTK theme (mandatory)
     - search [Gnome-Look Themes](https://www.gnome-look.org/browse?cat=135&ord=latest) for existing themes
     - or see [Generate GTK4](#generate-gtk4-from-wallbash) for generating GTK theme from wallpaper
   - Icon pack (optional) - defaults to Tela-circle
     - search [Gnome-Look Icons](https://www.gnome-look.org/browse?cat=132&ord=latest) for existing icon packs
   - Cursor theme (optional) - defaults to Bibata-Modern-Ice
     - search [Gnome-Look Cursors](https://www.gnome-look.org/browse?cat=107&ord=latest) for existing cursor themes
   - Font (optional)
     - search [fonts.google.com](https://fonts.google.com/) for web fonts
     - search [nerdfonts.com](https://www.nerdfonts.com/) for patched developer fonts

2. A collection of wallpapers that match your desired style/color scheme

   - [Wallhaven](https://wallhaven.cc/) - For wallpapers
   - [farbenfroh.io](https://farbenfroh.io/) - For color match wallpapers if you have a desired color scheme in mind
   - Don't add too many wallpapers, 8-10 is a good number

3. Install `just` for running helper scripts `yay -S just`

Go to your theme directory `cd ~/MyTheme` (replace `MyTheme` with your theme name)

:::tip
Rename `MyTheme` in the `justfile` to your theme name
:::

```bash
theme = "MyTheme"
```

Run `just init` to generate initial directory structure

Your theme should have the following structure:

```bash
~/MyTheme/
├── Config/                  # Part of your final theme - Configuration files
│   └── hyde/
│       └── themes/
│           └── MyTheme/     # main theme directory
│               └── wallpapers/
├── refs/                    # for reference files we generate
├── screenshots/             # for screenshots of your theme
├── Source/                  # Part of your final theme - Arcs ie. gtk, cursor, icon, font
│   └── arcs/
├── .gitignore
├── justfile                 # for running helper scripts
└── README.md                # links to this webpage
```

### Arcs

Arcs are the GTK theme, icon, cursor, and font components that make up parts of your theme.
Lets add these right away to the `Source/arcs` directory so they are ready for testing.

Your folder structure should look something like this:

```bash
~/MyTheme/
├── Source/
│   └── arcs/
│       ├── Gtk_<Your-GTK-Theme>.tar.*
│       ├── Cursor_<Your-Cursor-Theme>.tar.*
│       └── Icon_<Your-Icon-Theme>.tar.*
│       └── Font_<Your-Font-Name>.tar.*
```

**Make sure to use the correct prefix for each arc**. eg. `Gtk_<Your-GTK-Theme>.tar.*`

### Viewing your theme with Wallbash

Copy your wallpapers to your theme directory

```bash
cp -r ~/wallpapers ~/MyTheme/Config/.config/hyde/themes/MyTheme/wallpapers
```

cd into your theme directory

```bash
cd ~/MyTheme
```

install your theme

```bash
just install
```

### Testing your theme with wallbash

There are two ways to initialize your theme. from wallbash or from an existing theme.

We are going to use wallbash for this guide. as it gives you a good understanding of how wallbash generates the colors for your theme. You can learn more about wallbash [here](#understanding-wallbash).

Open Wallbash, setting auto, dark, or light (`Meta + Shift + R`). </br>
Set your chosen wallpaper as the current wallpaper (`Meta + Shift + W`)

Observe how wallbash adapts the colors to your wallpaper for the following applications:

- GTK (nwg-look)
  - to test your arc gtk theme, change from wallbash mode to theme mode (Meta + Shift + R)
  - then check `pavucontrol` to see if your gtk theme looks weird. if it does, follow the instructions in [Generate GTK4](#generate-gtk4-from-wallbash) to generate GTK4 theme files using wallbash
- Kitty (kitty)
- QT (qt5ct + qt6ct)
- Waybar (waybar)
- Spotify (spotify)
- VSCode (code) - needs wallbash enabled as color theme
- Cava (cava)

### Generate theme files

Make sure the wallpaper you picked is the best wallpaper that wallbash generates for your theme. </br>
Now run the following commands to generate the wallbash files.

```bash
just gen-all
just set-wall
```

You'll see a bunch of new files in your theme `refs` directory.

```bash
~/MyTheme/
├── refs/                   # for reference files we generate
│   ├── gtk-4.0/            # GTK4 theme files
│   │   ├── gtk.css         # Light theme
│   │   └── gtk-dark.css    # Dark theme
│   ├── kvantum/            # Kvantum theme files
│   │   ├── kvantum.theme   # Kvantum theme config
│   │   └── kvconfig.theme  # Kvantum config
│   ├── hypr.theme          # Hyprland theme
│   ├── kitty.theme         # Kitty terminal theme
│   ├── rofi.theme          # Rofi theme
│   ├── theme.dcol          # wallbash "theme" mode overrides
│   └── waybar.theme        # Waybar theme
│   └── wall.set            # First wallpaper theme uses
```

You can copy all the files to your `Config/.config/hyde/themes/MyTheme` directory.

```bash
cp -r ./refs/* ./Config/.config/hyde/themes/MyTheme
```

run install again to update your theme

```bash
just install
```

These files are used to set the "theme" mode for your theme. (`Meta + Shift + R`)

### Editing \*.theme files

These files are important for themes to work correctly.

You should reference a theme like [Bad Blood](https://github.com/HyDE-Project/hyde-gallery/blob/Bad-Blood/Configs/.config/hyde/themes/Bad%20Blood) along this guide.

Each \*.theme file contains configuration lines

The first line has the format: file_path | command_to_execute

- hypr.theme - `$HOME/.config/hypr/themes/theme.conf|> $HOME/.config/hypr/themes/colors.conf`
- kitty.theme - `$HOME/.config/kitty/theme.conf|killall -SIGUSR1 kitty`
- rofi.theme - `$HOME/.config/rofi/theme.rasi`
- waybar.theme - `$HOME/.config/waybar/theme.css|${scrDir}/wbarconfgen.sh`

the most important file is `hypr.theme`

```bash
$HOME/.config/hypr/themes/theme.conf|> $HOME/.config/hypr/themes/colors.conf
# ~/.config/hypr/theme/theme.conf is an auto-generated file. Do not edit.

$GTK_THEME=Bad-Blood # folder name inside `Source/arcs/Gtk_<Your-GTK-Theme>.tar.*`
$ICON_THEME=besgnulinux-mono-red # folder name inside `Source/arcs/Icon_<Your-Icon-Theme>.tar.*`
$COLOR_SCHEME=prefer-dark # prefer-dark, prefer-light, or auto
$CURSOR_THEME=Night-Diamond-Red # folder name inside `Source/arcs/Cursor_<Your-Cursor-Theme>.tar.*`
$CURSOR_SIZE=30 # cursor size in pixels
```

- Edit the variables for arcs, must match the name of the folder **inside** each arc in `Source/arcs` like above
- Set hyprland borders, colors, and other theme related settings
- You can use hypr.theme to set additional programs for your theme. such as SDDM or Vscode theme
- Becomes `$HOME/.config/hypr/themes/theme.conf`

Any updates to your theme in either `Config` or `Source` should be run with `just install` to update your theme.

### Editing theme.dcol

The `theme.dcol` file is used to override some generated wallbash colors for wallbash modes.
Check out [understanding wallbash](#understanding-wallbash) for more information.

This file is entirely optional

### Finalizing your theme

Your theme should now be ready to be added to the hyde-gallery!

A few more finishing touches:

- Add some screenshots to `~/screenshots`
- Add your theme to the Hyde-Gallery

### Adding Themes to Hyde-Gallery

In your theme directory, generate the readme using

```bash
python3 generate_readme.py
```

Initialize git

```bash
git init && git branch -M main && git add . && git commit -m "My first HyDE theme"
```

[create a github repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

Fork hyde-gallery <https://github.com/HyDE-Project/hyde-gallery> </br>
Add your theme to the list and `hyde-themes.json`

## More Information

### Generate GTK4 from wallbash

If your theme doesn't include GTK4 support, pavucontrol and other GTK4 applications may appear with a plain white theme.

Run the following command to generate the GTK4 theme files

```bash
just gen-gtk4
```

Copy the `refs/gtk-4.0` directory to your theme directory

```bash
mkdir -p ./Config/.config/hyde/themes/MyTheme/gtk-4.0
cp -r ./refs/gtk-4.0/* ./Config/.config/hyde/themes/MyTheme/gtk-4.0/
```

### Understanding wallbash

Wallbash generates 4 primary colors from your wallpaper, then creates color groups around each primary color with the following structure:

For each primary color (`wallbash_pry1` through `wallbash_pry4`):

- Text color (`wallbash_txt1` through `wallbash_txt4`)
- 9 accent colors (`wallbash_1xa1` through `wallbash_1xa9` for group 1, etc.)

Each color has an RGBA variant with configurable opacity (e.g. `wallbash_pry1_rgba(0.95)`)

Total: 44 base colors (4 groups × 11 colors) plus RGBA variants

Use `just gen-dcol` to generate a `theme.dcol` with all the wallbash generated colors for your active wallpaper for reference
