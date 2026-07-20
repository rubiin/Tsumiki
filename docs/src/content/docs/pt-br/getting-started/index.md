---
title: Início Rápido
description: Coloque o Tsumiki em funcionamento em minutos
---

Tsumiki é uma barra de status modular para Hyprland construída no sistema de widgets Fabric.

## Pré-requisitos

Antes de começar, certifique-se de ter:

- **Hyprland** — uma instalação funcional do Hyprland
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` deve mostrar 3.12 ou superior

## Instalação Rápida

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

A flag `-setup` instala todos os pacotes de sistema necessários e dependências Python. Sua senha pode ser solicitada durante a configuração.

Para métodos alternativos de instalação (script bootstrap, configuração manual), consulte o [guia de instalação completo](/pt-br/getting-started/installation).

## Inicialização Automática

Adicione esta linha ao `~/.config/hypr/hyprland.conf`:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Configuração Mínima

Aqui está um `config.toml` mínimo para começar:

```toml
$schema = "./tsumiki.schema.json"

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

Após salvar, reinicie a barra:

```sh
pkill tsumiki
./init.sh -start
```

## Próximos Passos

<CardGrid stagger>
  <Card title="Primeiros Passos" icon="rocket">
    Configure seu layout, teste widgets e personalize.
    <br />
    <a href="/pt-br/getting-started/first-steps">Ler guia →</a>
  </Card>
  <Card title="Configuração" icon="setting">
    Aprenda sobre cada widget, módulo e opção.
    <br />
    <a href="/pt-br/configuring/config">Ler docs →</a>
  </Card>
  <Card title="Regras Pós-Instalação" icon="list">
    Adicione regras de camada do Hyprland para efeitos de desfoque e popup.
    <br />
    <a href="/pt-br/resources/post-install">Ver regras →</a>
  </Card>
  <Card title="FAQ & Ajuda" icon="question">
    Problemas comuns e conselhos de solução.
    <br />
    <a href="/pt-br/help/faq">Obter ajuda →</a>
  </Card>
</CardGrid>
