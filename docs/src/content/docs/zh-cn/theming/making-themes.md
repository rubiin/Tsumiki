---
title: 创建主题
description: 如何为 Tsumiki 创建主题
---

在 `themes/` 目录中创建您的主题文件，扩展名为 `.toml`。

```bash
touch themes/my-theme.toml
```

## 最小主题

```toml
[dark.background]
main = "#121212"
alt = "#1a1a1a"

[dark.text]
main = "#e0e0e0"
secondary = "#c5c5c5"

[dark.accent]
blue = "#00d0ff"
green = "#00ff00"

[light.background]
main = "#ededed"

[light.text]
main = "#1f1f1f"
```

## 启用主题

```toml
[styling]
theme_name = "my-theme"
```
