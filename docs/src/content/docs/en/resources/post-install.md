---
title: Post Installation
description: Things you should do after installing Tsumiki
---

After installing Tsumiki, add these Hyprland layer rules so blur and popup effects render correctly.

```bash
layerrule = blur, ^tsumiki-notifications$
layerrule = xray 0, ^tsumiki-notifications$
layerrule = blurpopups, ^tsumiki-notifications$
layerrule = ignorezero, ^tsumiki-notifications$
layerrule = noanim , ^tsumiki-notifications$
layerrule = blur, ^fabric$
layerrule = ignorezero, ^fabric$
layerrule = xray 0, ^fabric$
layerrule = blurpopups, ^fabric$
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
layerrule = blur ,gtk-layer-shell
layerrule = ignorezero ,gtk-layer-shell
layerrule = blur, ^launcher$
layerrule = xray 0, ^launcher$
layerrule = blurpopups, ^launcher$
layerrule = ignorezero, ^launcher$
layerrule = animation popin, ^launcher$
```

## Next Steps

1. Restart Hyprland or reload your config.
2. Start Tsumiki with `tsu -start`.
3. If visuals still look wrong, check [FAQ](/en/help/faq).
