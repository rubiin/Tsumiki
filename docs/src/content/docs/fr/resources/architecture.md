---
title: Architecture
description: Aperçu de l'architecture de Tsumiki
sidebar:
  order: 5
---

```
tsumiki/
├── main.py                  # Point d'entrée
├── config.toml              # Configuration
├── themes/                  # Fichiers de thème
├── styles/                  # SCSS
├── widgets/                 # Widgets de la barre
├── modules/                 # Fenêtres et overlays
├── services/                # Services d'arrière-plan
├── shared/                  # Composants réutilisables
├── utils/                   # Utilitaires
└── assets/                  # Ressources
```

## Services

| Service  | Source         | Description          |
| -------- | -------------- | -------------------- |
| Batterie | UPower D-Bus   | Niveau, charge       |
| Réseau   | NetworkManager | WiFi, Ethernet       |
| Météo    | Open-Meteo     | Conditions           |
| MPRIS    | Playerctl      | Média                |
| Matugen  | binaire        | Palette Material You |
