---
title: FAQ
description: Häufig gestellte Fragen zu Tsumiki
---

:::tip
Für Hyprland-spezifisches Verhalten, konsultieren Sie das [Hyprland-Wiki](https://wiki.hyprland.org).
:::

<details>
<summary id="system-tray">System Tray nicht sichtbar?</summary>
<div>

Möglicherweise läuft noch eine andere Leiste. Stoppen Sie sie zuerst:

```sh
pkill leistenname
```

</div>
</details>

<details>
<summary id="notifications">Benachrichtigungen nicht sichtbar?</summary>
<div>

Ein anderer Benachrichtigungsdienst könnte aktiv sein. Stoppen Sie gängige Dienste:

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Leiste nicht sichtbar?</summary>
<div>

Starten Sie Tsumiki neu und überprüfen Sie die Ausgabe:

```sh
pkill tsumiki
tsu -start
```

Bei `ModuleNotFoundError` Abhängigkeiten installieren:

```sh
pip install -r requirements.txt
```

</div>
</details>

<details>
<summary id="sass-error">Sass-Kompilierungsfehler?</summary>
<div>

Ihre `config.toml` könnte ungültig sein. Zurücksetzen:

```sh
cp example/config.toml config.toml
```

</div>
</details>

<details>
<summary id="blur-effects">Unschärfe-Effekte aktivieren?</summary>
<div>

Fügen Sie `layerrule`-Einträge in `hyprland.conf` hinzu.

</div>
</details>

<details>
<summary id="updating">Tsumiki aktualisieren?</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

:::note
Erstellen Sie vor größeren Updates ein Backup Ihrer `config.toml`.
:::

</div>
</details>
