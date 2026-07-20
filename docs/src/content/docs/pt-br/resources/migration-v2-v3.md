---
title: Migração v2 para v3
description: Guia para atualizar sua configuração do Tsumiki
sidebar:
  order: 2
---

| Mudança | Detalhe |
|---|---|
| Formato | JSON5 → TOML |
| Dock | Em `[modules.dock]` |
| Auto-ocultar | Em `[modules.bar]` |
| Grupos | `[[widget_groups]]` e `[[collapsible_groups]]` |

```sh
cp ~/.config/tsumiki/example/config.toml ~/.config/tsumiki/config.toml
```

```toml
[modules.dock]
icon_size = 28
behavior = "intellihide"

[modules.bar]
auto_hide = true
auto_hide_timeout = 3000

[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4

[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
```
