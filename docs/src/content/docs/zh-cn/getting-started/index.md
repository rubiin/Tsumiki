---
title: 快速开始
description: 在几分钟内让 Tsumiki 运行起来
---

Tsumiki 是基于 Fabric 组件系统构建的 Hyprland 模块化状态栏。

## 前提条件

开始之前，请确保您已具备：

- **Hyprland** — 一个可正常运行的 Hyprland 安装
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` 应显示 3.12 或更高版本
- **uv** — 用于安装依赖项的 Python 包管理器（`uv sync`）

## 快速安装

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

`-setup` 标志会安装所有必需的系统包和 Python 依赖。安装过程中可能会提示您输入密码。

如需其他安装方法（引导脚本、手动设置），请参阅[完整安装指南](/zh-cn/getting-started/installation)。

## 自动启动

将这一行添加到 `~/.config/hypr/hyprland.conf`：

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## 最小配置

以下是一个可以快速上手的极简 `config.toml`：

```toml
"$schema" = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

保存后，重启状态栏：

```sh
pkill tsumiki
./init.sh -start
```

## 下一步

<CardGrid stagger>
  <Card title="第一步" icon="rocket">
    配置布局、测试组件并打造属于您的风格。
    <br />
    <a href="/zh-cn/getting-started/first-steps">阅读指南 →</a>
  </Card>
  <Card title="配置" icon="setting">
    了解每个组件、模块和选项。
    <br />
    <a href="/zh-cn/configuring/config">阅读文档 →</a>
  </Card>
  <Card title="安装后规则" icon="list">
    添加 Hyprland 层规则以实现模糊和弹出效果。
    <br />
    <a href="/zh-cn/resources/post-install">查看规则 →</a>
  </Card>
  <Card title="常见问题与帮助" icon="question">
    常见问题和故障排除建议。
    <br />
    <a href="/zh-cn/help/faq">获取帮助 →</a>
  </Card>
</CardGrid>
