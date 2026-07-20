---
title: İlk Adımlar
description: Tsumiki'yi kurduktan hemen sonra yapılacaklar
sidebar:
  order: 3
---

Tsumiki'yi kurdunuz ve [Kurulum Sonrası](/tr/resources/post-install) adımlarını uyguladınız. İşte hızlı bir şekilde çalışan bir panel elde etmenin yolu.

## 1. Paneli Başlatma

Tsumiki proje dizininden şunu çalıştırın:

```sh
./init.sh -start
```

Hyprland çalışıyorsa, çubuk ekranınızın üst kısmında görünmelidir. Çubuk görünmezse, terminaldeki hata çıktısını kontrol edin ve [Sorun Giderme](/tr/help/troubleshooting) bölümüne bakın.

:::tip
Tsumiki'yi istediğiniz zaman şu şekilde durdurabilirsiniz:

```sh
pkill tsumiki
```
:::

## 2. Otomatik Başlatmayı Ayarlama

Tsumiki'yi Hyprland yapılandırmanıza ekleyin, böylece oturum açtığınızda otomatik olarak başlasın:

`~/.config/hypr/hyprland.conf` dosyasını açın ve ekleyin:

```sh
exec-once = sleep 5; ~/.config/tsumiki/init.sh -start
```

`sleep 5` gecikmesi, Hyprland'in tamamen başlatılması için zaman tanır. Tsumiki'yi farklı bir dizine kopyaladıysanız yolu ayarlayın.

## 3. Örnek Yapılandırmayı Kopyalama

Tsumiki, eksiksiz bir örnek yapılandırmayla birlikte gelir. Geçerli bir başlangıç noktası elde etmek için kopyalayın:

```sh
cp example/config.toml config.toml
```

:::tip
Tüm mevcut seçenekleri belgeleriyle görmek için `example/config.toml` dosyasını bir metin düzenleyicide açın.
:::

## 4. Düzeninizi Özelleştirme

`config.toml` dosyasını düzenleyin ve `[layout]` bölümünü ayarlayın. Her bölüm (`left_section`, `middle_section`, `right_section`) bir widget adları dizisidir:

```toml
[layout]
left_section = ["workspaces", "window_title"]
middle_section = ["date_time"]
right_section = ["volume", "battery", "system_tray", "power"]
```

Bu, aşağıdaki gibi bir çubuk oluşturur:

| Bölüm | Widget'lar |
|---|---|
| **Sol** | Çalışma alanı değiştirici, aktif pencere başlığı |
| **Orta** | Geçerli tarih ve saat |
| **Sağ** | Ses kontrolü, pil durumu, sistem tepsisi, güç menüsü |

## 5. Değişiklikleri Uygulamak için Yeniden Yükleme

Düzenlemelerinizi kaydettikten sonra Tsumiki'yi yeniden başlatın:

```sh
pkill tsumiki
./init.sh -start
```

Yapılandırma geçerliyse, çubuk yeni düzeninizle yeniden görünmelidir.

## 6. Yaygın Widget'ları Test Etme

Widget'larınızla etkileşim kurmayı deneyin:

- **Çalışma alanları** — Değiştirmek için tıklayın, masaüstlerinde gezinmek için kaydırın.
- **Ses** — Sesi kapatmak/açmak için tıklayın, ayarlamak için kaydırın.
- **Pil** — Kalan süreyi ve şarj durumunu görmek için üzerine gelin.
- **Tarih/Saat** — Takvimi ve bildirim panelini açmak için tıklayın.
- **Sistem Tepsisi** — Mevinci sistem tepsisi simgeleri otomatik olarak görünmelidir.

## 7. Kendinize Göre Yapın

- **Renkleri değiştirin** — SCSS özelleştirmesi için [Tema Oluşturma](/tr/theming/making-themes) veya otomatik duvar kağıdı tabanlı temalama için [Matugen](/tr/theming/matugen) bölümüne bakın.
- **Daha fazla widget ekleyin** — 45'ten fazla widget için [Widget'lar Referansı](/tr/features/widgets) bölümüne göz atın.
- **Modülleri etkinleştirin** — [Dock](/tr/features/modules#dock), [Uygulama Başlatıcı](/tr/features/modules#uygulama-başlatıcı) veya [OSD](/tr/features/modules#osd-ekran-görüntüsü)'yi deneyin.
- **Davranışı yapılandırın** — Her seçenek için tam [Yapılandırma](/tr/configuring/config) referansına bakın.

## Sorun Giderme

Bir şey yanlış görünüyorsa:

- **Çubuk görünmüyor** — Hyprland'in çalıştığından ve başka çubukların çalışmadığından emin olun (`pkill waybar`).
- **Simgeler yok** — [JetBrains Nerd Font](https://www.nerdfonts.com) kurulu ve terminal/UI yazı tipiniz olarak yapılandırılmış mı kontrol edin.
- **Eksik işlevsellik** — Bazı widget'lar harici araçlar gerektirir (örn. medya için `playerctl`, parlaklık için `brightnessctl`). Tüm bağımlılıkların kurulu olduğundan emin olmak için `./init.sh -setup` komutunu çalıştırın.
- **SASS hataları** — `config.toml` dosyanız geçersiz olabilir. `example/config.toml` ile karşılaştırın.

Daha fazla yardım için [SSS](/tr/help/faq) veya [Sorun Giderme](/tr/help/troubleshooting) sayfalarına bakın.
