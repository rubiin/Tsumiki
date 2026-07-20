---
title: 高级配置
description: Tsumiki 高级配置模式
---

## 组件组

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

## 可折叠组

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "工具"
```

## 多显示器

```toml
[general]
multi_monitor = true
```

## 自动隐藏

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```
