---
title: بداية سريعة
description: ابدأ مع تسوميكي في دقائق
---

تسوميكي هو شريط حالة معياري لهيبرلاند مبني على نظام Fabric للواجهات.

## المتطلبات الأساسية

قبل البدء، تأكد من أن لديك:

- **هيبرلاند** — تثبيت عامل لهيبرلاند
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — يجب أن يظهر `python --version` الإصدار 3.12 أو أعلى

## التثبيت السريع

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

العلامة `-setup` تثبت جميع حزم النظام المطلوبة وتبعيات Python. قد يُطلب منك كلمة المرور أثناء الإعداد.

لطرق التثبيت البديلة (سكريبت التمهيد، الإعداد اليدوي)، راجع [دليل التثبيت الكامل](/ar/getting-started/installation).

## التشغيل التلقائي

أضف هذا السطر إلى `~/.config/hypr/hyprland.conf`:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## إعدادات الحد الأدنى

إليك ملف `config.toml` بسيط للبدء:

```toml
"$schema" = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

بعد الحفظ، أعد تشغيل الشريط:

```sh
pkill tsumiki
./init.sh -start
```

## الخطوات التالية

<CardGrid stagger>
  <Card title="الخطوات الأولى" icon="rocket">
    هيئ تخطيطك، اختبر الأدوات، واجعلها خاصة بك.
    <br />
    <a href="/ar/getting-started/first-steps">اقرأ الدليل →</a>
  </Card>
  <Card title="الإعدادات" icon="setting">
    تعرف على كل أداة ووحدة وخيار.
    <br />
    <a href="/ar/configuring/config">اقرأ الوثائق →</a>
  </Card>
  <Card title="قواعد ما بعد التثبيت" icon="list">
    أضف قواعد طبقة هيبرلاند لتأثيرات التمويه والنوافذ المنبثقة.
    <br />
    <a href="/ar/resources/post-install">عرض القواعد →</a>
  </Card>
  <Card title="الأسئلة الشائعة والمساعدة" icon="question">
    المشاكل الشائعة ونصائح استكشاف الأخطاء.
    <br />
    <a href="/ar/help/faq">احصل على المساعدة →</a>
  </Card>
</CardGrid>
