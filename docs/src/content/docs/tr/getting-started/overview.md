---
title: Genel Bakış
description: Tsumiki nedir, ön koşullar ve temel kavramlar
sidebar:
  order: 1
---

## Tsumiki Nedir?

Tsumiki (eski adıyla Hydepanel), [Hyprland](https://hyprland.org) Wayland birleştiricisi için modüler bir durum çubuğudur. [Fabric](https://github.com/Fabric-Development/fabric) widget sistemi üzerine inşa edilmiş olup, birleştirilebilir widget'lar aracılığıyla özel masaüstü panelleri oluşturmak için esnek bir mimari sağlar.

**Tsumiki** (積み木) adı Japoncada "yapı taşları" anlamına gelir — projenin modüler, istiflenebilir tasarımını yansıtır.

## Ön Koşullar

Tsumiki'yi kurmadan önce sisteminizin bu gereksinimleri karşıladığından emin olun:

| Gereksinim | Notlar |
|---|---|
| [Hyprland](https://hyprland.org) | Çalışan bir Hyprland kurulumu gereklidir |
| [JetBrains Nerd Font](https://www.nerdfonts.com) | Simge ve glif oluşturma için gereklidir |
| **Python 3.12+** | Tsumiki, Python 3.12 hedefler |
| **Arch Linux** (önerilir) | Arch için optimize edilmiş paketler; diğer dağıtımlar manuel kurulum gerektirebilir |
| **NetworkManager** | Ağ ile ilgili widget'lar ve servisler için gereklidir |
| **PipeWire** | Ses ile ilgili widget'lar ve OSD için gereklidir |

## Temel Kavramlar

### Widget'lar

Widget'lar çubukta görünen bireysel yapı taşlarıdır. 45'in üzerinde yerleşik widget şunları kapsar:

- **Sistem bilgisi** — CPU, bellek, GPU, depolama, ağ kullanımı
- **Donanım kontrolü** — Ses, parlaklık, mikrofon, pil
- **Masaüstü yönetimi** — Çalışma alanları, pencere başlığı, görev çubuğu
- **Araçlar** — Ekran görüntüsü, OCR, pano, ekran kaydı
- **Verimlilik** — Pomodoro zamanlayıcı, Kanban paneli, kronometre, emoji seçici
- **Entegrasyon** — Hava durumu, medya kontrolleri, Git arkadaşı, DNS değiştirici

Her widget `config.toml` dosyasında `[widgets.<ad>]` altında yapılandırılır. Tam liste için [Widget'lar Referansı](/tr/features/widgets) bölümüne bakın.

### Modüller

Modüller çubuğun ötesine geçen daha büyük UI yüzeyleridir — bağımsız pencereler veya katmanlardır:

- **Çubuk** — Ana panelin kendisi
- **Bildirim Sistemi** — Masaüstü bildirim görüntüleme
- **Dock** — Intellihide özellikli uygulama dock'u
- **Genel Bakış** — Tam ekran çalışma alanı exposé
- **Uygulama Başlatıcı** — Klavye odaklı uygulama arama
- **OSD** — Ses, parlaklık vb. için ekran üstü görüntüler
- **Masaüstü Saati** — Dekoratif saat katmanı
- **Masaüstü Alıntıları** — İlham verici alıntı görüntüleme

Modüller `config.toml` dosyasında `[modules.<ad>]` altında yapılandırılır. Ayrıntılar için [Modüller Referansı](/tr/features/modules) bölümüne bakın.

### Düzen

Widget'ların çubuktaki yerleşimi `config.toml` dosyasının `[layout]` bölümü tarafından kontrol edilir:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]
```

Widget'lar ayrıca gruplandırılabilir veya daraltılabilir gruplara yerleştirilebilir. Ayrıntılar için [Yapılandırma](/tr/configuring/config) bölümüne bakın.

### Servisler

Servisler widget'lara veri sağlayan arka plan işlemleridir — pil seviyelerini, ağ durumunu, medya oynatıcıları, hava durumunu ve daha fazlasını izlerler. Widget'lar GTK sinyalleri aracılığıyla servislere bağlanır ve güncellemeleri verimli tutar.

## Mimari

Tsumiki'nin mimarisi katmanlı bir tasarım izler:

```text
┌──────────────────────────────────────────────┐
│                  main.py                       │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│   │ Config    │  │ CSS      │  │ Module     │  │
│   │ Loader   │  │ Compiler │  │ Init       │  │
│   └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────┬────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Services │  │ Widgets  │  │ Modules  │
  │ (DBus,   │──▶│ (Panel   │──▶│ (Overlay │
  │ polling) │  │ buttons) │  │ windows) │
  └──────────┘  └──────────┘  └──────────┘
```

- **Servisler** arka planda çalışır ve durum değişikliklerinde GTK sinyalleri yayar
- **Widget'lar** servis sinyallerine abone olan panel düğmeleridir
- **Modüller** katmanlar ve açılır pencereler için bağımsız GTK pencereleridir

Daha derin bir bakış için [Mimari](/tr/resources/architecture) sayfasına bakın.

## Önerilen Yol

1. **[Tsumiki'yi Kurun](/tr/getting-started/installation)** — Kopyalayın, bağımlılıkları yükleyin, ortamı kurun.
2. **[İlk Adımlar](/tr/getting-started/first-steps)** — Çubuğu başlatın, düzeninizi yapılandırın, kurulum sonrası kuralları uygulayın.
3. **[Yapılandırma](/tr/configuring/config)** — TOML yapılandırma yapısını ve mevcut seçenekleri anlayın.
4. **Temanızı seçin** — Yerleşik bir temayla başlayın veya [Tema Oluşturma](/tr/theming/making-themes) ile kendiniz yapın.
5. **Keşfedin** — Widget'lar ekleyin, modülleri etkinleştirin, davranışı özelleştirin.

## Yardıma mı ihtiyacınız var?

- Yaygın sorunlar için [SSS](/tr/help/faq) bölümünü kontrol edin.
- Hata ayıklama rehberliği için [Sorun Giderme](/tr/help/troubleshooting) bölümünü ziyaret edin.
- Topluluk desteği için [Discord](https://discord.gg/8nWbDC4SnP)'a katılın.
