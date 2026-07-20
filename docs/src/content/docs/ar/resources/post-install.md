---
title: ما بعد التثبيت
description: أشياء يجب فعلها بعد تثبيت تسوميكي
---

أضف قواعد طبقة هيبرلاند هذه لتأثيرات التمويه والنوافذ المنبثقة.

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

1. أعد تشغيل هيبرلاند أو حمّل إعداداتك.
2. ابدأ تسوميكي بـ `tsu -start`.
3. راجع [الأسئلة الشائعة](/ar/help/faq) إذا لزم الأمر.
