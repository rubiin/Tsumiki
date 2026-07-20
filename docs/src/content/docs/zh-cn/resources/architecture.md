---
title: 架构
description: Tsumiki 架构概览
sidebar:
  order: 5
---

```
tsumiki/
├── main.py                  # 入口点
├── config.toml              # 配置
├── themes/                  # 主题 .toml 文件
├── styles/                  # SCSS
├── widgets/                 # 状态栏组件
├── modules/                 # 窗口和覆盖层
├── services/                # 后台服务
└── utils/                   # 工具程序
```

## 服务

| 服务 | 描述 |
|---|---|
| 电池 | UPower D-Bus |
| 网络 | NetworkManager |
| 天气 | Open-Meteo |
| MPRIS | Playerctl |
| Matugen | Material You 调色板 |
