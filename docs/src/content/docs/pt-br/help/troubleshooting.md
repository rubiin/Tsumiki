---
title: Solução de Problemas
description: Diagnosticar problemas comuns do Tsumiki
---

## O Painel Não Aparece

1. Verifique se o Hyprland está em execução.
2. Mate outras barras: `pkill nome-da-barra`.
3. Inicie o Tsumiki: `tsu -start`.

## Widget Ausente

- Confirme que o widget está ativado em `config.toml`.
- Verifique se está listado em uma seção `layout`.

## Tema Não Aplica

- Verifique `theme_name` no `config.toml`.
- Recompile: `./tsumiki.sh -recompile`.

## Alto Uso de CPU

- Reduza intervalos de sondagem.
- Desative widgets não utilizados.
