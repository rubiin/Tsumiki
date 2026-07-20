---
title: Referência de Módulos
description: Documentação completa de todos os módulos do Tsumiki
sidebar:
  order: 2
---

## Barra

```toml
[modules.bar]
layer = "top"
auto_hide = false
location = "top"
```

## Sistema de Notificações

```toml
[modules.notification]
enabled = true
anchor = "top-right"
auto_dismiss = true
```

## Dock

```toml
[modules.dock]
enabled = false
icon_size = 40
behavior = "intellihide"
preview_apps = true
```

## Visão Geral

```toml
[modules.overview]
enabled = false
layer = "top"
anchor = "center"
```

## Lançador de Aplicativos

```toml
[modules.app_launcher]
enabled = false
layout = "grid"
grid_columns = 3
```

## OSD

```toml
[modules.osd]
enabled = false
timeout = 3000
osds = ["brightness", "volume"]
```

## Relógio da Área de Trabalho

```toml
[modules.desktop_clock]
enabled = false
type = "cookie"
layer = "bottom"
```

## Citações da Área de Trabalho

```toml
[modules.desktop_quotes]
enabled = false
interval = 600
```
