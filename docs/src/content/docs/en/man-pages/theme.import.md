---
title: theme.import.py
description: theme import manual page
---

### Preview

![preview theme import](../../../../assets/man-pages/theme.import/image.png)

### NAME

theme.import.py - Imports themes from the HyDE gallery repository

### SYNOPSIS

`theme.import.py` [OPTIONS]

### DESCRIPTION

`theme.import.py` is a script to import and manage themes from the HyDE gallery repository. It allows users to clone the repository, fetch theme data, preview themes, and apply selected themes.

### OPTIONS

- `-j`, `--json`
  Fetch JSON data after cloning the repository.

- `-S`, `--select`
  Select themes using `fzf`.

- `-p`, `--preview` IMAGE_URL
  Get a preview of the specified theme.

- `-t`, `--preview-text` TEXT
  Preview text to display when using the `--preview` option.

- `--skip-clone`
  Skip cloning the repository.

- `-f`, `--fetch` THEME
  Fetch and update a specific theme by name. Use `all` to fetch all themes located in `xdg_config/hyde/themes`.

### ENVIRONMENT VARIABLES

- `LOG_LEVEL`
  Set the logging level (default: `INFO`).

- `XDG_CACHE_HOME`
  Directory for cache files (default: `~/.cache`).

- `XDG_CONFIG_HOME`
  Directory for configuration files (default: `~/.config`).

- `FULL_THEME_UPDATE`
  Overwrites the archived files (useful for updates and changes in archives).

### EXAMPLES

Opens fzf menu and select themes.

```shell
theme.import.py --select
```
