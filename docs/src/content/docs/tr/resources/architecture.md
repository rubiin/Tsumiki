---
title: Mimari
description: Tsumiki mimarisine genel bakış
sidebar:
  order: 5
---

```
tsumiki/
├── main.py                  # Giriş noktası
├── config.toml              # Yapılandırma
├── themes/                  # Tema .toml dosyaları
├── styles/                  # SCSS
├── widgets/                 # Çubuk widget'ları
├── modules/                 # Pencereler ve katmanlar
├── services/                # Arka plan servisleri
└── utils/                   # Yardımcı araçlar
```

## Servisler

| Servis | Açıklama |
|---|---|
| Pil | UPower D-Bus |
| Ağ | NetworkManager |
| Hava Durumu | Open-Meteo |
| MPRIS | Playerctl |
| Matugen | Material You paleti |
