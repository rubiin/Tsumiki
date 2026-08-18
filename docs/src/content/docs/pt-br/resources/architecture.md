---
title: Arquitetura
description: Visão geral da arquitetura do Tsumiki
sidebar:
  order: 5
---

```
tsumiki/
├── main.py                  # Ponto de entrada
├── config.toml              # Configuração
├── themes/                  # Temas .toml
├── styles/                  # SCSS
├── widgets/                 # Widgets da barra
├── modules/                 # Janelas e sobreposições
├── services/                # Serviços de fundo
└── utils/                   # Utilitários
```

## Serviços

| Serviço | Descrição           |
| ------- | ------------------- |
| Bateria | UPower D-Bus        |
| Rede    | NetworkManager      |
| Clima   | Open-Meteo          |
| MPRIS   | Playerctl           |
| Matugen | Paleta Material You |
