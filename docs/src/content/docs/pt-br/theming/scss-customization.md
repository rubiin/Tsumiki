---
title: Personalização SCSS
description: Personalização avançada de temas SCSS no Tsumiki
sidebar:
  order: 3
---

| Variável             | Padrão      | Descrição             |
| -------------------- | ----------- | --------------------- |
| `$bar-background`    | cor do tema | Fundo da barra        |
| `$bar-border-radius` | `16px`      | Cantos arredondados   |
| `$bar-padding`       | `4px 12px`  | Preenchimento interno |

```toml
[styling.bar]
background = "#1e1e2e"
border-radius = 16
```

| Classe     | Efeito               |
| ---------- | -------------------- |
| `compact`  | Espaçamento reduzido |
| `bordered` | Adiciona borda       |
| `pill`     | Forma de pílula      |

Recompile: `./tsumiki.sh -recompile`.
