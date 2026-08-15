---
title: FAQ
description: Perguntas frequentes sobre o Tsumiki
---

<details>
<summary id="system-tray">Não consigo ver a bandeja do sistema?</summary>
<div>

Outra barra pode estar em execução. Pare-a primeiro:

```sh
pkill nome-da-barra
```

</div>
</details>

<details>
<summary id="notifications">Não consigo ver as notificações?</summary>
<div>

Outro daemon de notificações pode estar ativo.

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">Não consigo ver a barra?</summary>
<div>

```sh
pkill tsumiki
tsu -start
```

Se vir `ModuleNotFoundError`:

```sh
uv sync
```

</div>
</details>

<details>
<summary id="sass-error">Erro de compilação Sass?</summary>
<div>

```sh
cp example/config.toml config.toml
```

</div>
</details>

<details>
<summary id="updating">Como atualizar o Tsumiki?</summary>
<div>

```sh
cd ~/.config/tsumiki
git pull
```

</div>
</details>
