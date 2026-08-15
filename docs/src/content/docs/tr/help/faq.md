---
title: SSS
description: Tsumiki hakkında sık sorulan sorular
---

<details>
<summary id="system-tray">Sistem tepsisi görünmüyor mu?</summary>
<div>

Başka bir çubuk çalışıyor olabilir. Önce onu durdurun:

```sh
pkill çubuk-adı
```

</div>
</details>

<details>
<summary id="notifications">Bildirimler görünmüyor mu?</summary>
<div>

Başka bir bildirim hizmeti aktif olabilir.

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Çubuk görünmüyor mu?</summary>
<div>

```sh
pkill tsumiki
tsu -start
```

`ModuleNotFoundError` görürseniz:

```sh
uv sync
```

</div>
</details>

<details>
<summary id="updating">Tsumiki'yi nasıl güncellerim?</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

</div>
</details>
