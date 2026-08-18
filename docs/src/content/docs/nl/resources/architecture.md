---
title: Architectuur
description: Overzicht van de Tsumiki-architectuur
sidebar:
  order: 5
---

```
tsumiki/
├── main.py                  # Ingangspunt
├── config.toml              # Configuratie
├── themes/                  # Thema .toml-bestanden
├── styles/                  # SCSS
├── widgets/                 # Balkwidgets
├── modules/                 # Vensters en overlays
├── services/                # Achtergrondservices
└── utils/                   # Hulpprogramma's
```

## Services

| Service  | Beschrijving       |
| -------- | ------------------ |
| Batterij | UPower D-Bus       |
| Netwerk  | NetworkManager     |
| Weer     | Open-Meteo         |
| MPRIS    | Playerctl          |
| Matugen  | Material You-palet |
