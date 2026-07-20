---
title: Post Instalación
description: Cosas que deberías hacer después de instalar Tsumiki
---

Después de instalar Tsumiki, añade estas reglas de capa de Hyprland para que el desenfoque y los efectos de popup se rendericen correctamente.

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

## Siguientes Pasos

1. Reinicia Hyprland o recarga tu configuración.
2. Inicia Tsumiki con `tsu -start`.
3. Si los visuales aún se ven incorrectos, consulta las [Preguntas Frecuentes](/es/help/faq).
