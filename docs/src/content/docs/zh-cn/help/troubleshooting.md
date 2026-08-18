---
title: 故障排除
description: 诊断常见 Tsumiki 问题
---

## 面板不显示

1. 确保 Hyprland 正在运行。
2. 停止其他状态栏：`pkill bar-name`。
3. 启动 Tsumiki：`tsu -start`。

## 组件缺失

- 确认组件已在 `config.toml` 中启用。
- 检查它是否列在 `layout` 部分中。

## 主题未应用

- 检查 `config.toml` 中的 `theme_name`。
- 重新编译：`./tsumiki.sh -recompile`。

## CPU 使用率高

- 减少轮询间隔。
- 禁用未使用的组件。
