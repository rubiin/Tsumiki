---
title: FAQs & Tips
description: Frequently asked questions about Tsumiki
---

:::tip
Hyprland related questions should be referenced to [Hyprland Wiki](https://wiki.hyprland.org)
:::

<details>
<summary id="system-tray">Cannot see system tray?</summary>
<div>

Be sure to kill any bars that you may be running. You can kill other bars with:

```sh
pkill bar-name
```

</div>
</details>

<details>
<summary id="notifications">Cannot see notifications?</summary>
<div>

Be sure to kill other notification daemons that you may be running. You can kill other daemons with:

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Cannot see bar?</summary>
<div>

Kill the app with `pkill tsumiki`. Run `init.sh -start`. This should show some logs.

If it shows `ModuleNotFoundError`, run:

```sh
pip install -r requirements.txt
```

If this does not solve the issue, report a bug with a screenshot of the log.

</div>
</details>

<details>
<summary id="sass-error">Sass compilation error or UI not rendering?</summary>
<div>

Your `theme.toml` may be incorrect or outdated. You can copy the latest `theme.toml` from the `example/` directory:

```sh
cp example/theme.toml theme.toml
```

Be aware that this will overwrite any custom changes you've made.

</div>
</details>

<details>
<summary id="no-icons">No Icons?</summary>
<div>

Make sure your icon theme has the required icons. One of the recommended icon themes is `Tela Circle`.

</div>
</details>

<details>
<summary id="import-error">ImportError: cannot import XX</summary>
<div>

This error usually occurs when the required module/package is not installed or cannot be found. Make sure you have all the necessary dependencies installed.

You can run:

```sh
./init.sh -install
```

to install all the required packages and dependencies. Additionally, you can also manually install the package. Follow the instructions in the Installation section of the README.

</div>
</details>

<details>
<summary id="blur-effects">How to enable blur and effects?</summary>
<div>

Add these rules to your `hyprland.conf` to make blur and other effects work properly:

```sh
layerrule = blur, ^tsumiki-notifications$
layerrule = xray 0, ^tsumiki-notifications$
layerrule = blurpopups, ^tsumiki-notifications$
layerrule = ignorezero, ^tsumiki-notifications$
layerrule = noanim , ^tsumiki-notifications$
layerrule = blur, ^fabric$
layerrule = ignorezero, ^fabric$
layerrule = xray 0, ^fabric$
layerrule = blurpopups, ^fabric$
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
layerrule = blur ,gtk-layer-shell
layerrule = ignorezero ,gtk-layer-shell
layerrule = blur, ^launcher$
layerrule = xray 0, ^launcher$
layerrule = blurpopups, ^launcher$
layerrule = ignorezero, ^launcher$
layerrule = animation popin, ^launcher$
```

</div>
</details>

<details>
<summary id="updating">How do I update Tsumiki?</summary>
<div>

Updating to the latest commit is fairly simple, just git pull the latest changes:

```sh
cd ~/.config/tsumiki
git pull
```

:::note
Make sure to keep your config safe just in case
:::

</div>
</details>
