---
title: الأسئلة الشائعة
description: أسئلة متكررة عن تسوميكي
---

<details>
<summary id="system-tray">لا أرى علبة النظام؟</summary>
<div>

قد يكون شريط آخر قيد التشغيل. أوقفه أولاً:

```sh
pkill اسم-الشريط
```

</div>
</details>

<details>
<summary id="notifications">لا أرى الإشعارات؟</summary>
<div>

قد يكون هناك برنامج إشعارات آخر نشط.

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">لا أرى الشريط؟</summary>
<div>

```sh
pkill tsumiki
tsu -start
```

إذا رأيت `ModuleNotFoundError`:

```sh
pip install -r requirements.txt
```

</div>
</details>

<details>
<summary id="updating">كيف أحدث تسوميكي؟</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

</div>
</details>
