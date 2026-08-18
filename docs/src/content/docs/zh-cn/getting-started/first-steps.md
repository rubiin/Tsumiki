---
title: 第一步
description: 安装 Tsumiki 后要做的第一件事
sidebar:
  order: 3
---

您已经安装了 Tsumiki 并应用了[安装后](/zh-cn/resources/post-install)步骤。以下是如何快速获得一个可以工作的面板。

## 1. 启动面板

从 Tsumiki 项目目录运行：

```sh
./tsumiki.sh -start
```

如果 Hyprland 正在运行，状态栏应出现在屏幕顶部。如果状态栏未出现，请检查终端中的错误输出并参阅[故障排除](/zh-cn/help/troubleshooting)。

:::tip
您可以随时停止 Tsumiki：

```sh
pkill tsumiki
```

:::

## 2. 设置自动启动

将 Tsumiki 添加到您的 Hyprland 配置中，以便在登录时自动启动：

打开 `~/.config/hypr/hyprland.conf` 并添加：

```sh
exec-once = sleep 5; ~/.config/tsumiki/tsumiki.sh -start
```

`sleep 5` 的延迟让 Hyprland 有足够的时间完全初始化。如果您将 Tsumiki 克隆到其他目录，请调整路径。

## 3. 复制示例配置

Tsumiki 附带一个完整的示例配置。复制它以获得一个有效的起点：

```sh
cp example/config.toml config.toml
```

:::tip
在文本编辑器中打开 `example/config.toml` 查看所有可用选项及文档。
:::

## 4. 自定义布局

编辑 `config.toml` 并调整 `[layout]` 部分。每个部分（`left_section`、`middle_section`、`right_section`）是一个组件名称数组：

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

这将创建一个具有以下布局的状态栏：

| 区域     | 组件                                   |
| -------- | -------------------------------------- |
| **左侧** | 工作区切换器、活动窗口标题             |
| **中间** | 当前日期和时间                         |
| **右侧** | 音量控制、电池状态、系统托盘、电源菜单 |

## 5. 重新加载以应用更改

保存编辑后，重启 Tsumiki：

```sh
pkill tsumiki
./tsumiki.sh -start
```

如果配置有效，状态栏将以新布局重新出现。

## 6. 测试常用组件

尝试与您的组件交互：

- **工作区** — 点击切换，滚动浏览桌面。
- **音量** — 点击静音/取消静音，滚动调整。
- **电池** — 悬停查看剩余时间和充电状态。
- **日期/时间** — 点击打开日历和通知面板。
- **系统托盘** — 现有的托盘图标应自动出现。

## 7. 打造您的风格

- **更改颜色** — 参阅[创建主题](/zh-cn/theming/making-themes)了解 SCSS 自定义，或参阅 [Matugen](/zh-cn/theming/matugen) 了解基于壁纸的自动主题。
- **添加更多组件** — 浏览[组件参考](/zh-cn/features/widgets)了解所有 45+ 可用组件。
- **启用模块** — 尝试 [Dock](/zh-cn/features/modules#dock)、[应用启动器](/zh-cn/features/modules#应用启动器)或 [OSD](/zh-cn/features/modules#osd-屏幕显示)。
- **配置行为** — 查看完整的[配置](/zh-cn/configuring/config)参考了解每个选项。

## 故障排除

如果出现问题：

- **状态栏不显示** — 检查您是否正在运行 Hyprland，以及是否有其他状态栏在运行（`pkill waybar`）。
- **没有图标** — 验证 [JetBrains Nerd Font](https://www.nerdfonts.com) 已安装并配置为终端/UI 字体。
- **缺少功能** — 某些组件需要外部工具（例如，媒体需要 `playerctl`，亮度需要 `brightnessctl`）。运行 `./tsumiki.sh -setup` 以确保所有依赖项都已安装（Python 依赖项通过 `uv sync` 安装）。
- **SASS 错误** — 您的 `config.toml` 可能无效。与 `example/config.toml` 进行比较。

如需更多帮助，请参阅[常见问题](/zh-cn/help/faq)或[故障排除](/zh-cn/help/troubleshooting)页面。
