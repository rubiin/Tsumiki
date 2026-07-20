---
title: Na Installatie
description: Wat te doen na het installeren van Tsumiki
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

1. Herstart Hyprland of herlaad uw configuratie.
2. Start Tsumiki met `tsu -start`.
3. Raadpleeg de [FAQ](/nl/help/faq) indien nodig.
