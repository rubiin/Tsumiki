---
title: Post Installation
description: Choses à faire après avoir installé Tsumiki
---

Après avoir installé Tsumiki, ajoutez ces règles de couche Hyprland pour que les effets de flou et de popup s'affichent correctement.

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

## Prochaines Étapes

1. Redémarrez Hyprland ou rechargez votre configuration.
2. Démarrez Tsumiki avec `tsu -start`.
3. Si les visuels sont toujours incorrects, consultez la [FAQ](/fr/help/faq).
