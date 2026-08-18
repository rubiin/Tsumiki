---
title: Sorun Giderme
description: Yaygın Tsumiki sorunlarını teşhis etme
---

## Panel Görünmüyor

1. Hyprland'in çalıştığından emin olun.
2. Diğer çubukları durdurun: `pkill çubuk-adı`.
3. Tsumiki'yi başlatın: `tsu -start`.

## Widget Eksik

- Widget'ın `config.toml` içinde etkinleştirildiğini doğrulayın.
- Bir `layout` bölümünde listelendiğini kontrol edin.

## Tema Uygulanmıyor

- `config.toml` içinde `theme_name`'i kontrol edin.
- Yeniden derleyin: `./tsumiki.sh -recompile`.

## Yüksek CPU Kullanımı

- Yoklama aralıklarını azaltın.
- Kullanılmayan widget'ları devre dışı bırakın.
