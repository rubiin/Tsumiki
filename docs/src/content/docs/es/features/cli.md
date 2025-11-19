---
title: HyDE CLI
description: Installation guide for HyDE-cli
---

<div align="center">
  <br>

![hyde_cli_banner](../../../../assets/hyde-cli.png)

<style type="text/css">
    img {
        width: 200px;
    }
</style>

<br/>

HyDE-cli is a CLI tool for [HyDE](https://github.com/prasanthrangan/hyprdots).
This repository contains scripts that, while may not be perfect, could provide a better way to manage your HyDE installation.
For example, we have a functional TUI restore tool that follows `restore_cfg.lst`, power-saving options that could be useful for laptops, and much more!

</div>

> 🚨 While HyDE-cli is stable, it is important to note that these scripts do alter and _could_ potentially mess up your system configuration.
> We ask that you use this tool carefully and report any bugs you find.

## Installation

To install, execute the following command:

```sh
curl -sL https://raw.githubusercontent.com/HyDE-Project/Hyde-cli/master/install.sh | bash
```

> 📢 For User who do not have root access:
> `export HYDE_LOCAL=1` to install this package locally

For other working install solutions, see the following below.

### Arch Linux

Use your preferred AUR helper `paru` or `yay`:

```sh
paru -Sy hyde-cli-git
```

```sh
yay -Sy hyde-cli-git
```

Use makepkg:

```sh
git clone https://aur.archlinux.org/hyde-cli-git.git
cd ./hyde-cli
makepkg -si
```

### Make

Install required dependencies: `git make fzf tree ttf-jetbrains-mono-nerd`.

Clone:

```sh
git clone https://github.com/HyDE-Project/Hyde-cli
cd ./Hyde-cli
```

To install:

```sh
make
```

To uninstall:

```sh
make uninstall
```

To update:

```sh
make update clean install
```

> 📢 User who do not have root access should provide this flag for `make`; `make LOCAL=1`

> ⚠️ If you have previously installed HyDE without using the CLI, you can still use the CLI to manage your installation.
> To do this, combine the --dir and --link flags where the local cloned repository is located.
>
> For example:
>
> ```sh
> Hyde-install --dir /path/to/cloned/hyde --link
> ```

#### Installation Instructions for HyDE with Hyde-install

> 📢 To achieve the best experience, it is encouraged you perform a fresh install of HyDE.

1. **Basic Installation**

- To install HyDE with the defaults, simply run the following command:

  ```sh
  Hyde-install
  ```

> ⚠️ _Already have HyDE before you discover this CLI?_
> Simply run this command
> `Hyde-install --link --dir ~/HyDE`
> Note that the `~/HydE` is the path to the clone directory.
> See **Advanced Installation** below for more info.

2. **Advanced Installation**

- For more control over the installation process, you can use the following options:

  - **Specify Local Directory**: To clone HyDE into a specific local directory and run the installation, use the `-d` or `--dir` flag followed by the path of the directory.

    ```sh
    Hyde-install --dir /path/to/directory
    ```

  - **Specify Remote Git Repository**: To clone HyDE from a specific remote git repository, use the `-g` or `--git` flag followed by the URL of the repository.

    ```sh
    Hyde-install --git https://host/owner/repository
    ```

  - **Link Local Git Repository**: To link a local git repository, use the `-l` or `--link` flag.

    ```sh
    Hyde-install --link
    ```

3. **Sync changes**

- If you want to get the latest changes from the `hyprdots/HyDE` repo and apply to your local install
  ```sh
  Hyde update
  Hyde restore Config
  ```

> ⚠️ If you have previously installed HyDE without using the CLI, you can still use the CLI to manage your installation.
> To do this, combine the --dir and --link flags where the local cloned repository is located.
>
> For example:
>
> ```sh
> Hyde-install --dir /path/to/cloned/hyde --link
> ```
