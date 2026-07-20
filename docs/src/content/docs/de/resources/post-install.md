---
title: Nach der Installation
description: Was Sie nach der Installation von Tsumiki tun sollten
---

Fügen Sie diese Hyprland-Layer-Regeln hinzu, damit Unschärfe- und Popup-Effekte korrekt dargestellt werden.

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

## Nächste Schritte

1. Starten Sie Hyprland neu oder laden Sie Ihre Konfiguration neu.
2. Starten Sie Tsumiki mit `tsu -start`.
3. Bei Problemen, prüfen Sie die [FAQ](/de/help/faq).
