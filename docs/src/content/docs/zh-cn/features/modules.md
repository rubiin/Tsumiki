---
title: 模块参考
description: 所有 Tsumiki 模块的完整文档
sidebar:
  order: 2
---

## 状态栏

```toml
[modules.bar]
layer = "top"
auto_hide = false
location = "top"
```

## 通知系统

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

## 概览

```toml
[modules.overview]
enabled = false
layer = "top"
anchor = "center"
```

## 应用启动器

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

## 桌面时钟

```toml
[modules.desktop_clock]
enabled = false
type = "cookie"
layer = "bottom"
```

## 桌面语录

```toml
[modules.desktop_quotes]
enabled = false
interval = 600
```
