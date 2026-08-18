---
title: Arquitectura
description: Visión general de la arquitectura de Tsumiki para desarrolladores y colaboradores
sidebar:
  order: 5
---

## Estructura del Proyecto

```
tsumiki/
├── main.py                  # Punto de entrada
├── config.toml              # Configuración del usuario
├── themes/                  # Archivos .toml de temas
├── styles/                  # Hojas de estilo SCSS
├── widgets/                 # Widgets de la barra
├── modules/                 # Superposiciones y ventanas
├── services/                # Servicios en segundo plano
├── shared/                  # Componentes UI reutilizables
├── utils/                   # Módulos de utilidad
└── assets/                  # Activos estáticos
```

## Servicios Clave

| Servicio | Fuente               | Descripción             |
| -------- | -------------------- | ----------------------- |
| Batería  | UPower D-Bus         | Nivel, estado de carga  |
| Red      | NetworkManager D-Bus | WiFi, Ethernet          |
| Brillo   | brightnessctl        | Brillo pantalla/teclado |
| Clima    | Open-Meteo           | Condiciones climáticas  |
| MPRIS    | Playerctl            | Control de medios       |
| Matugen  | binario matugen      | Paleta Material You     |

## Añadir un Nuevo Widget

1. Cree `widgets/mi_widget.py`
2. Añada configuración en `utils/widget_settings.py`
3. Añada entrada de esquema en `tsumiki.schema.json`
4. Registre en `modules/bar.py`
5. Añada estilos SCSS
6. Referencie en el layout
