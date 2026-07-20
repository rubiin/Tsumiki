---
title: Visão Geral
description: O que é Tsumiki, pré-requisitos e conceitos-chave
sidebar:
  order: 1
---

## O que é Tsumiki?

Tsumiki (anteriormente Hydepanel) é uma barra de status modular para o compositor Wayland [Hyprland](https://hyprland.org). Construído no sistema de widgets [Fabric](https://github.com/Fabric-Development/fabric), fornece uma arquitetura flexível para criar painéis de desktop personalizados através de widgets componíveis.

O nome **Tsumiki** (積み木) significa "blocos de construção" em japonês — refletindo o design modular e empilhável do projeto.

## Pré-requisitos

Antes de instalar o Tsumiki, certifique-se de que seu sistema atende a estes requisitos:

| Requisito | Notas |
|---|---|
| [Hyprland](https://hyprland.org) | Uma instalação funcional do Hyprland é necessária |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Necessário para renderização de ícones e glifos |
| **Python 3.12+** | Tsumiki requer Python 3.12 |
| **Arch Linux** (recomendado) | Pacotes otimizados para Arch; outras distribuições podem precisar de configuração manual |
| **NetworkManager** | Necessário para widgets e serviços de rede |
| **PipeWire** | Necessário para widgets de áudio e OSD |

## Conceitos-chave

### Widgets

Widgets são os blocos de construção individuais que aparecem na barra. Existem mais de 45 widgets integrados cobrindo:

- **Informações do sistema** — CPU, memória, GPU, armazenamento, uso de rede
- **Controle de hardware** — Volume, brilho, microfone, bateria
- **Gerenciamento da área de trabalho** — Espaços de trabalho, título da janela, barra de tarefas
- **Utilitários** — Captura de tela, OCR, área de transferência, gravação de tela
- **Produtividade** — Temporizador Pomodoro, quadro Kanban, cronômetro, seletor de emoji
- **Integração** — Clima, controles de mídia, Git companion, alternador de DNS

Cada widget é configurado em `[widgets.<nome>]` no `config.toml`. Consulte a [Referência de Widgets](/pt-br/features/widgets) para a lista completa.

### Módulos

Módulos são superfícies de UI maiores que vão além da barra — são janelas ou sobreposições independentes:

- **Barra** — O próprio painel principal
- **Sistema de Notificações** — Exibição de notificações da área de trabalho
- **Dock** — Dock de aplicativos com intellihide
- **Visão Geral** — Exposé de espaços de trabalho em tela cheia
- **Lançador de Aplicativos** — Pesquisa de aplicativos por teclado
- **OSD** — Exibições na tela para volume, brilho, etc.
- **Relógio da Área de Trabalho** — Sobreposição decorativa de relógio
- **Citações da Área de Trabalho** — Exibição de citações inspiradoras

Os módulos são configurados em `[modules.<nome>]` no `config.toml`. Consulte a [Referência de Módulos](/pt-br/features/modules) para detalhes.

### Layout

O posicionamento dos widgets na barra é controlado pela seção `[layout]` do `config.toml`:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Widgets também podem ser agrupados ou colocados em grupos recolhíveis. Consulte [Configuração](/pt-br/configuring/config) para detalhes.

### Serviços

Serviços são processos em segundo plano que fornecem dados aos widgets — eles monitoram níveis de bateria, estado da rede, players de mídia, clima e muito mais. Widgets se conectam aos serviços via sinais GTK, mantendo as atualizações eficientes.

## Arquitetura

A arquitetura do Tsumiki segue um design em camadas:

```text
┌──────────────────────────────────────────────┐
│                  main.py                       │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│   │ Config    │  │ CSS      │  │ Module     │  │
│   │ Loader   │  │ Compiler │  │ Init       │  │
│   └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────┬────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Services │  │ Widgets  │  │ Modules  │
  │ (DBus,   │──▶│ (Panel   │──▶│ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **Serviços** são executados em segundo plano e emitem sinais GTK em mudanças de estado
- **Widgets** são botões do painel que se inscrevem nos sinais dos serviços
- **Módulos** são janelas GTK independentes para sobreposições e popups

Consulte a página [Arquitetura](/pt-br/resources/architecture) para uma visão mais aprofundada.

## Caminho Recomendado

1. **[Instalar Tsumiki](/pt-br/getting-started/installation)** — Clonar, instalar dependências, configurar o ambiente.
2. **Siga [Primeiros Passos](/pt-br/getting-started/first-steps)** — Inicie a barra, configure seu layout, aplique regras pós-instalação.
3. **Aprenda [Configuração](/pt-br/configuring/config)** — Entenda a estrutura de configuração TOML e as opções disponíveis.
4. **Escolha seu tema** — Comece com um tema integrado ou crie o seu próprio com [Criação de Temas](/pt-br/theming/making-themes).
5. **Explore** — Adicione widgets, ative módulos, personalize o comportamento.

## Precisa de Ajuda?

- Consulte a [FAQ](/pt-br/help/faq) para problemas comuns.
- Visite [Solução de Problemas](/pt-br/help/troubleshooting) para orientação de depuração.
- Junte-se ao [Discord](https://discord.gg/8nWbDC4SnP) para suporte da comunidade.
