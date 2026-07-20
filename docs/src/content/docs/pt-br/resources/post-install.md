---
title: Pós-Instalação
description: Coisas a fazer após instalar o Tsumiki
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

1. Reinicie o Hyprland ou recarregue a configuração.
2. Inicie o Tsumiki com `tsu -start`.
3. Consulte a [FAQ](/pt-br/help/faq) se necessário.
