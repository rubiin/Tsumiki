---
title: Modüller Referansı
description: Tüm Tsumiki modüllerinin tam dokümantasyonu
sidebar:
  order: 2
---

## Çubuk

```toml
[modules.bar]
layer = "top"
auto_hide = false
location = "top"
```

## Bildirim Sistemi

```toml
[modules.notification]
enabled = true
anchor = "top-right"
auto_dismiss = true
```

## Dock

```toml
[modules.dock]
enabled = false
icon_size = 40
behavior = "intellihide"
preview_apps = true
```

## Genel Bakış

```toml
[modules.overview]
enabled = false
layer = "top"
anchor = "center"
```

## Uygulama Başlatıcı

```toml
[modules.app_launcher]
enabled = false
layout = "grid"
grid_columns = 3
```

## OSD

```toml
[modules.osd]
enabled = false
timeout = 3000
osds = ["brightness", "volume"]
```

## Masaüstü Saati

```toml
[modules.desktop_clock]
enabled = false
type = "cookie"
layer = "bottom"
```

## Masaüstü Alıntıları

```toml
[modules.desktop_quotes]
enabled = false
interval = 600
```
