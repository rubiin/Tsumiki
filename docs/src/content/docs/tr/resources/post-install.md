---
title: Kurulum Sonrası
description: Tsumiki'yi kurduktan sonra yapılacaklar
---

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

1. Hyprland'i yeniden başlatın veya yapılandırmanızı yeniden yükleyin.
2. Tsumiki'yi `tsu -start` ile başlatın.
3. Gerekirse [SSS](/tr/help/faq) bölümüne bakın.
