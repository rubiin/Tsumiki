---
title: 常见问题
description: 关于 Tsumiki 的常见问题
---

<details>
<summary id="system-tray">看不到系统托盘？</summary>
<div>

可能还有其他状态栏在运行。先停止它：

```sh
pkill bar-name
```

</div>
</details>

<details>
<summary id="notifications">看不到通知？</summary>
<div>

可能有其他通知守护程序处于活动状态。

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">看不到状态栏？</summary>
<div>

```sh
pkill tsumiki
tsu -start
```

如果看到 `ModuleNotFoundError`：

```sh
uv sync
```

</div>
</details>

<details>
<summary id="updating">如何更新 Tsumiki？</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

</div>
</details>
