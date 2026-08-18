---
title: 概述
description: Tsumiki 是什么、前提条件及核心概念
sidebar:
  order: 1
---

## 什么是 Tsumiki？

Tsumiki（原名 Hydepanel）是 [Hyprland](https://hyprland.org) Wayland 合成器的模块化状态栏。它基于 [Fabric](https://github.com/Fabric-Development/fabric) 组件系统构建，通过可组合的组件提供灵活的架构来构建自定义桌面面板。

**Tsumiki**（積み木）在日语中意为"积木"——反映了该项目模块化、可堆叠的设计理念。

## 前提条件

在安装 Tsumiki 之前，请确保您的系统满足以下要求：

| 要求                                             | 说明                                             |
| ------------------------------------------------ | ------------------------------------------------ |
| [Hyprland](https://hyprland.org)                 | 需要可正常运行的 Hyprland 安装                   |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | 图标和字形渲染所需                               |
| **Python 3.12+**                                 | Tsumiki 需要 Python 3.12                         |
| **uv**                                           | 用于安装依赖项的 Python 包管理器（`uv sync`）    |
| **Arch Linux**（推荐）                           | 为 Arch 优化的软件包；其他发行版可能需要手动设置 |
| **NetworkManager**                               | 网络相关组件和服务所需                           |
| **PipeWire**                                     | 音频相关组件和 OSD 所需                          |

## 核心概念

### 组件（Widgets）

组件是出现在状态栏中的独立构建块。有超过 45 个内置组件，涵盖：

- **系统信息** — CPU、内存、GPU、存储、网络使用
- **硬件控制** — 音量、亮度、麦克风、电池
- **桌面管理** — 工作区、窗口标题、任务栏
- **实用工具** — 截图、OCR、剪贴板、屏幕录制
- **生产力** — 番茄钟、看板、秒表、表情选择器
- **集成** — 天气、媒体控制、Git 助手、DNS 切换器

每个组件在 `config.toml` 的 `[widgets.<名称>]` 下配置。有关完整列表，请参阅[组件参考](/zh-cn/features/widgets)。

### 模块（Modules）

模块是超越状态栏的更大 UI 界面——它们是独立的窗口或覆盖层：

- **状态栏** — 主面板本身
- **通知系统** — 桌面通知显示
- **Dock** — 带智能隐藏的应用程序 Dock
- **概览** — 全屏工作区展示
- **应用启动器** — 键盘驱动的应用搜索
- **OSD** — 用于音量、亮度等的屏幕显示
- **桌面时钟** — 装饰性时钟覆盖
- **桌面语录** — 励志语录显示

模块在 `config.toml` 的 `[modules.<名称>]` 下配置。详情请参阅[模块参考](/zh-cn/features/modules)。

### 布局

状态栏中组件的放置由 `config.toml` 的 `[layout]` 部分控制：

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

组件也可以分组或放置在可折叠组中。详情请参阅[配置](/zh-cn/configuring/config)。

### 服务

服务是为组件提供数据的后台进程——它们监控电池电量、网络状态、媒体播放器、天气等。组件通过 GTK 信号连接到服务，保持更新的高效性。

## 架构

Tsumiki 的架构遵循分层设计：

```text
┌──────────────────────────────────────────────┐
│                  main.py                       │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│   │ Config    │  │ CSS      │  │ Module     │  │
│   │ Loader   │  │ Compiler │  │ Init       │  │
│   └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────┬────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Services │  │ Widgets  │  │ Modules  │
  │ (DBus,   │──▶│ (Panel   │──▶│ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **服务** 在后台运行，在状态变化时发出 GTK 信号
- **组件** 是订阅服务信号的面板按钮
- **模块** 是用于覆盖层和弹出窗口的独立 GTK 窗口

详情请参阅[架构](/zh-cn/resources/architecture)页面。

## 推荐路径

1. **[安装 Tsumiki](/zh-cn/getting-started/installation)** — 克隆、安装依赖、设置环境。
2. **遵循[第一步](/zh-cn/getting-started/first-steps)** — 启动状态栏、配置布局、应用安装后规则。
3. **学习[配置](/zh-cn/configuring/config)** — 了解 TOML 配置结构和可用选项。
4. **选择主题** — 从内置主题开始，或使用[创建主题](/zh-cn/theming/making-themes)创建自己的主题。
5. **探索** — 添加组件、启用模块、自定义行为。

## 需要帮助？

- 查阅[常见问题](/zh-cn/help/faq)了解常见问题。
- 访问[故障排除](/zh-cn/help/troubleshooting)获取调试指导。
- 加入 [Discord](https://discord.gg/8nWbDC4SnP) 获取社区支持。
