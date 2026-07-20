---
title: Hızlı Başlangıç
description: Tsumiki'yi dakikalar içinde çalıştırın
---

Tsumiki, Fabric widget sistemi üzerine inşa edilmiş, Hyprland için modüler bir durum çubuğudur.

## Ön Koşullar

Başlamadan önce aşağıdakilere sahip olduğunuzdan emin olun:

- **Hyprland** — çalışan bir Hyprland kurulumu
- **JetBrains Nerd Font** — `sudo pacman -S ttf-jetbrains-mono-nerd`
- **Python 3.12+** — `python --version` 3.12 veya üstünü göstermeli

## Hızlı Kurulum

```sh
git clone https://github.com/rubiin/tsumiki.git ~/.config/tsumiki
cd ~/.config/tsumiki
./init.sh -setup
./init.sh -start
```

`-setup` bayrağı gerekli tüm sistem paketlerini ve Python bağımlılıklarını yükler. Kurulum sırasında şifreniz istenebilir.

Alternatif kurulum yöntemleri için (bootstrap betiği, manuel kurulum), [tam kurulum kılavuzuna](/tr/getting-started/installation) bakın.

## Otomatik Başlatma

`~/.config/hypr/hyprland.conf` dosyasına şu satırı ekleyin:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

## Minimum Yapılandırma

İşte başlamak için minimum bir `config.toml`:

```toml
$schema = "./tsumiki.schema.json"

[general]
debug = false
auto_restart = true

[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray"]

[modules.bar]
layer = "top"
location = "top"

[widgets.workspaces]
count = 10
hide_unoccupied = true

[widgets.volume]
tooltip = true

[widgets.battery]
tooltip = true
```

Kaydettikten sonra çubuğu yeniden başlatın:

```sh
pkill tsumiki
./init.sh -start
```

## Sonraki Adımlar

<CardGrid stagger>
  <Card title="İlk Adımlar" icon="rocket">
    Düzeninizi yapılandırın, widget'ları test edin ve kişiselleştirin.
    <br />
    <a href="/tr/getting-started/first-steps">Kılavuzu okuyun →</a>
  </Card>
  <Card title="Yapılandırma" icon="setting">
    Her widget, modül ve seçenek hakkında bilgi edinin.
    <br />
    <a href="/tr/configuring/config">Dökümanı okuyun →</a>
  </Card>
  <Card title="Kurulum Sonrası Kurallar" icon="list">
    Bulanıklık ve açılır pencere efektleri için Hyprland katman kuralları ekleyin.
    <br />
    <a href="/tr/resources/post-install">Kuralları görüntüleyin →</a>
  </Card>
  <Card title="SSS ve Yardım" icon="question">
    Yaygın sorunlar ve sorun giderme tavsiyeleri.
    <br />
    <a href="/tr/help/faq">Yardım alın →</a>
  </Card>
</CardGrid>
