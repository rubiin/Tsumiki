---
title: 安装后
description: 安装 Tsumiki 后要做的事
---

添加这些 Hyprland 层规则以使模糊和弹出效果正确呈现。

```lua
layerrule {
  name = tsumiki-notifications
  match:namespace = tsumiki-notifications
  blur = on
  xray = on
  blur_popups = on
  ignore_alpha = 0
  no_anim = on
}

layerrule {
  name = tsumiki-layer
  match:namespace = tsumiki
  blur = on
  xray = on
  blur_popups = on
  ignore_alpha = 0
}

layerrule {
  name = gtk-layer-shell
  match:namespace = gtk-layer-shell
  blur = on
  ignore_alpha = 0
}
```

1. 重启 Hyprland 或重新加载配置。
2. 使用 `tsu -start` 启动 Tsumiki。
3. 如有需要，请查阅[常见问题](/zh-cn/help/faq)。
