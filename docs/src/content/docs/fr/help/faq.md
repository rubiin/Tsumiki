---
title: FAQ
description: Questions fréquemment posées sur Tsumiki
---

:::tip
Pour le comportement spécifique à Hyprland, consultez le [Wiki Hyprland](https://wiki.hyprland.org).
:::

<details>
<summary id="system-tray">Impossible de voir la barre système ?</summary>
<div>

Une autre barre est peut-être encore en cours d'exécution. Arrêtez-la d'abord :

```sh
pkill nom-barre
```

</div>
</details>

<details>
<summary id="notifications">Impossible de voir les notifications ?</summary>
<div>

Un autre démon de notifications peut les gérer. Arrêtez les démons courants :

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Impossible de voir la barre ?</summary>
<div>

Redémarrez Tsumiki depuis la racine du projet et inspectez la sortie :

```sh
pkill tsumiki
tsu -start
```

Si vous voyez `ModuleNotFoundError`, installez les dépendances :

```sh
uv sync
```

</div>
</details>

<details>
<summary id="sass-error">Erreur de compilation Sass ou interface non rendue ?</summary>
<div>

Votre `config.toml` peut être obsolète ou invalide. Réinitialisez-le depuis l'exemple :

```sh
cp example/config.toml config.toml
```

</div>
</details>

<details>
<summary id="import-error">ImportError : impossible d'importer XX</summary>
<div>

Cela signifie généralement qu'une dépendance requise est manquante.

```sh
tsu -setup
```

ou :

```sh
uv sync
```

</div>
</details>

<details>
<summary id="blur-effects">Comment activer le flou et les effets ?</summary>
<div>

Ajoutez ces entrées `layerrule` à `hyprland.conf`.

</div>
</details>

<details>
<summary id="updating">Comment mettre à jour Tsumiki ?</summary>
<div>

Tirez les derniers changements :

```sh
cd ~/.config/tsumiki
git pull
```

:::note
Conservez une sauvegarde de `config.toml` avant les mises à jour importantes.
:::

</div>
</details>
