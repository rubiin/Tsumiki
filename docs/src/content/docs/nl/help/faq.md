---
title: FAQ
description: Veelgestelde vragen over Tsumiki
---

<details>
<summary id="system-tray">Kan ik de systeemvak niet zien?</summary>
<div>

Er kan nog een andere balk actief zijn. Stop deze eerst:

```sh
pkill balknaam
```

</div>
</details>

<details>
<summary id="notifications">Kan ik meldingen niet zien?</summary>
<div>

Er kan een andere meldingendienst actief zijn.

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Kan ik de balk niet zien?</summary>
<div>

```sh
pkill tsumiki
tsu -start
```

Bij `ModuleNotFoundError`:

```sh
pip install -r requirements.txt
```

</div>
</details>

<details>
<summary id="updating">Hoe werk ik Tsumiki bij?</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

</div>
</details>
