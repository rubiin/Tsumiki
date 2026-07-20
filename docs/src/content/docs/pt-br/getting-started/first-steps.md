---
title: Primeiros Passos
description: O que fazer logo após instalar o Tsumiki
sidebar:
  order: 3
---

Você instalou o Tsumiki e aplicou as etapas de [Pós-Instalação](/pt-br/resources/post-install). Aqui está como obter um painel funcional rapidamente.

## 1. Iniciar o Painel

A partir do diretório do projeto Tsumiki, execute:

```sh
./init.sh -start
```

Se o Hyprland estiver em execução, a barra deve aparecer no topo da sua tela. Se a barra não aparecer, verifique a saída de erros no terminal e consulte [Solução de Problemas](/pt-br/help/troubleshooting).

:::tip
Você pode parar o Tsumiki a qualquer momento com:

```sh
pkill tsumiki
```
:::

## 2. Configurar Inicialização Automática

Adicione o Tsumiki à sua configuração do Hyprland para que ele inicie automaticamente ao fazer login:

Abra `~/.config/hypr/hyprland.conf` e adicione:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

O atraso `sleep 5` dá tempo ao Hyprland para inicializar completamente. Ajuste o caminho se você clonou o Tsumiki em um diretório diferente.

## 3. Copiar a Configuração de Exemplo

O Tsumiki vem com uma configuração de exemplo completa. Copie-a para obter um ponto de partida válido:

```sh
cp example/config.toml config.toml
```

:::tip
Abra `example/config.toml` em um editor de texto para ver todas as opções disponíveis com documentação.
:::

## 4. Personalizar seu Layout

Edite `config.toml` e ajuste a seção `[layout]`. Cada seção (`left_section`, `middle_section`, `right_section`) é uma matriz de nomes de widgets:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Isso cria uma barra com:

| Seção | Widgets |
|---|---|
| **Esquerda** | Alternador de espaços de trabalho, título da janela ativa |
| **Centro** | Data e hora atuais |
| **Direita** | Controle de volume, status da bateria, bandeja do sistema, menu de energia |

## 5. Recarregar para Aplicar Alterações

Após salvar suas edições, reinicie o Tsumiki:

```sh
pkill tsumiki
./init.sh -start
```

Se a configuração for válida, a barra deve reaparecer com seu novo layout.

## 6. Testar Widgets Comuns

Tente interagir com seus widgets:

- **Espaços de trabalho** — Clique para alternar, role para percorrer as áreas de trabalho.
- **Volume** — Clique para silenciar/ativar som, role para ajustar.
- **Bateria** — Passe o mouse para ver o tempo restante e o status da carga.
- **Data/Hora** — Clique para abrir o calendário e o painel de notificações.
- **Bandeja do Sistema** — Os ícones da bandeja devem aparecer automaticamente.

## 7. Personalize

- **Altere cores** — Consulte [Criação de Temas](/pt-br/theming/making-themes) para personalização SCSS ou [Matugen](/pt-br/theming/matugen) para temas automáticos baseados em papel de parede.
- **Adicione mais widgets** — Navegue pela [Referência de Widgets](/pt-br/features/widgets) para todos os 45+ widgets disponíveis.
- **Ative módulos** — Experimente o [Dock](/pt-br/features/modules#dock), o [Lançador de Aplicativos](/pt-br/features/modules#lançador-de-aplicativos) ou o [OSD](/pt-br/features/modules#osd-exibição-na-tela).
- **Configure o comportamento** — Consulte a referência completa de [Configuração](/pt-br/configuring/config) para cada opção.

## Solução de Problemas

Se algo parecer errado:

- **A barra não aparece** — Verifique se você está executando o Hyprland e se não há outras barras em execução (`pkill waybar`).
- **Sem ícones** — Verifique se o [JetBrains Nerd Font](https://www.nerdfonts.com) está instalado e configurado como fonte do seu terminal/UI.
- **Funcionalidade ausente** — Alguns widgets requerem ferramentas externas (ex., `playerctl` para mídia, `brightnessctl` para brilho). Execute `./init.sh -setup` para garantir que todas as dependências estejam instaladas.
- **Erros SASS** — Seu `config.toml` pode ser inválido. Compare com `example/config.toml`.

Para mais ajuda, consulte as páginas [FAQ](/pt-br/help/faq) ou [Solução de Problemas](/pt-br/help/troubleshooting).
