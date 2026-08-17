---
title: Post Installation
description: Things you should do after installing Tsumiki
---

After installing Tsumiki, add these Hyprland layer rules so blur and popup effects render correctly.

```lua
hl.layer_rule({
	name = "tsumiki-notifications",
	match = { namespace = "tsumiki-notifications" },
	blur = true,
	xray = true,
	blur_popups = true,
	ignore_alpha = 0,
	no_anim = true,
})

hl.layer_rule({
	name = "tsumiki-layer",
	match = { namespace = "tsumiki" },
	blur = true,
	xray = true,
	blur_popups = true,
	ignore_alpha = 0,
})

hl.layer_rule({
	name = "gtk-layer-shell",
	match = { namespace = "gtk-layer-shell" },
	blur = true,
	ignore_alpha = 0,
})

hl.layer_rule({
	name = "launcher-layer",
	match = { namespace = "launcher" },
	blur = true,
	xray = true,
	blur_popups = true,
	ignore_alpha = 0,
	animation = "popin",
})

```

## Next Steps

1. Restart Hyprland or reload your config.
2. Start Tsumiki with `tsu -start`.
3. If visuals still look wrong, check [FAQ](/en/help/faq).
