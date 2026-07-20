---
title: 从 v2 迁移到 v3
description: 升级 Tsumiki 配置的指南
sidebar:
  order: 2
---

| 变更 | 详情 |
|---|---|
| 格式 | JSON5 → TOML |
| Dock | 位于 `[modules.dock]` 下 |
| 自动隐藏 | 位于 `[modules.bar]` 下 |
| 分组 | 使用 `[[widget_groups]]` 和 `[[collapsible_groups]]` |

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
icon = "󰓒"
```
