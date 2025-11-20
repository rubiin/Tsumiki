---
title: Post Installation
description: Things you should do after installing Tsumiki
---

Add these rules to your hyprland.conf to make blur and other effects work properly

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
