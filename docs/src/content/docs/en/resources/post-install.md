---
title: Post Installation
description: Things you should do after installing Tsumiki
---

After installing Tsumiki, add these Hyprland layer rules so blur and popup effects render correctly.

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

layerrule {
  name = launcher-layer
  match:namespace = launcher
  blur = on
  xray = on
  blur_popups = on
  ignore_alpha = 0
  animation = popin
}


```

## Next Steps

1. Restart Hyprland or reload your config.
2. Start Tsumiki with `tsu -start`.
3. If visuals still look wrong, check [FAQ](/en/help/faq).
