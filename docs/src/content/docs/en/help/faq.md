---
title: FAQs & Tips
description: Frequently asked questions about Tsumiki
---

:::tip
For Hyprland-specific behavior, check the [Hyprland Wiki](https://wiki.hyprland.org).
:::

<details>
<summary id="system-tray">Cannot see system tray?</summary>
<div>

Another bar may still be running. Stop it first:

```sh
pkill bar-name
```

</div>
</details>

<details>
<summary id="notifications">Cannot see notifications?</summary>
<div>

Another notification daemon may be handling notifications. Stop common daemons:

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Cannot see bar?</summary>
<div>

Restart Tsumiki from the project root and inspect output:

```sh
pkill tsumiki
tsu -start
```

If you see `ModuleNotFoundError`, install dependencies:

```sh
pip install -r requirements.txt
```

If the issue continues, open an issue and include logs.

</div>
</details>

<details>
<summary id="sass-error">Sass compilation error or UI not rendering?</summary>
<div>

Your `theme.toml` may be outdated or invalid. Reset it from the example:

```sh
cp example/theme.toml theme.toml
```

This overwrites custom values.

</div>
</details>

<details>
<summary id="no-icons">No Icons?</summary>
<div>

Use an icon theme with broad coverage. `Tela Circle` is a common choice.

</div>
</details>

<details>
<summary id="import-error">ImportError: cannot import XX</summary>
<div>

This usually means a required dependency is missing.

Install runtime and Python dependencies:

```sh
tsu -setup
```

or:

```sh
pip install -r requirements.txt
```

</div>
</details>

<details>
<summary id="blur-effects">How to enable blur and effects?</summary>
<div>

Add these `layerrule` entries to `hyprland.conf`:

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

Pull the latest changes:

```sh
cd ~/.config/tsumiki
git pull
```

:::note
Keep a backup of `config.toml` and `theme.toml` before major updates.
:::

</div>
</details>
