---
title: إعدادات متقدمة
description: أنماط إعدادات متقدمة لتسوميكي
---

بمجرد أن تصبح مرتاحاً مع أساسيات [الإعدادات](/ar/configuring/config)، هذه الأنماط تساعدك في ضبط تسوميكي أكثر.

## مجموعات الأدوات

جمّع الأدوات مع مسافات وأنماط مشتركة:

```toml
[[widget_groups]]
widgets = ["updates", "battery"]
spacing = 4
style_classes = ["bordered"]
```

أشر إلى مجموعة في تخطيطك باستخدام `@group:N` (فهرس يبدأ من صفر):

```toml
[layout]
right_section = ["@group:0", "system_tray"]
```

## المجموعات القابلة للطي

أخفِ الأدوات الأقل استخداماً خلف مفتاح:

```toml
[[collapsible_groups]]
widgets = ["ocr", "screenshot", "recorder"]
spacing = 4
icon = "󰒓"
tooltip = "أدوات مساعدة"
style_classes = ["utility-tools"]
```

## شاشات متعددة

فعّل اللوحات لكل شاشة:

```toml
[general]
multi_monitor = true
```

## إخفاء تلقائي

```toml
[modules.bar]
auto_hide = true
auto_hide_timeout = 3000
```

## وحدات مخصصة

أضف وحدتك الخاصة تحت `modules` وأشر إليها من `layout`. حافظ على التغييرات صغيرة وأعد التشغيل باستخدام `./init.sh -start` للتحقق.
