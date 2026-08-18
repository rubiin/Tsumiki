# Tsumiki Optimizations

> Generated analysis of optimization opportunities across the Tsumiki codebase.
> Organized by category with priority, effort, and impact estimates.

---

## 🔥 High Priority

### 1. Thread Safety for Stats Fabricator

**Files**: `utils/widget_utils.py`
**Effort**: Small | **Impact**: Medium

`_util_fabricator` is accessed/created across threads without a lock. The `stats_poll()` generator runs in a background thread via `Fabricator(poll_from=...)`, while `get_util_fabricator()`, `connect_util_fabricator_changed()`, and `disconnect_util_fabricator_changed()` can be called from any thread. Multiple widgets (`stats.py`, `updates.py`, `cava.py`) can trigger concurrent access.

**Fix**: Add `threading.Lock()` guard around creation and mutation of `_util_fabricator`, `_util_subscribers`, and `_util_changed_handler_ids`.

### 4. Expensive gi.repository Imports at Module Level

**Files**: `services/network.py`, `services/mpris.py`, `shared/scrollable_text.py`, `shared/popover.py`, `widgets/quick_settings/submenu/wifi.py`
**Effort**: Medium | **Impact**: Medium

`gi.repository` imports (NM, Playerctl, PangoCairo, GtkLayerShell) are loaded at module import time, not deferred. These are C extension modules with significant overhead. `services/network.py` and `services/mpris.py` import them at the top level even if the service is never used (e.g., network widget disabled).

**Fix**: Move `gi.repository` imports into lazy initializers or inside `__init__` methods so they only load when the service/widget is actually instantiated. NetworkManager and Playerctl introspection are particularly expensive.

---

## 🥈 Medium Priority

### 6. Signal Connection Leaks (Many Widgets Bypass TeardownMixin)

**Files**: `widgets/battery.py`, `widgets/bluetooth.py`, `widgets/volume.py`, `widgets/datetime_menu.py`, `widgets/kanban.py`, `services/network.py`, `widgets/quick_settings/submenu/bluetooth.py`, `widgets/quick_settings/togglers.py`, `widgets/settings_gui.py`
**Effort**: Medium | **Impact**: Medium

Many widgets connect to signals directly without using `_register_handler()` from `TeardownMixin`. When the widget is destroyed, these signal handlers remain connected to the source object. For singleton services that outlive widgets, stale callbacks can cause memory leaks and potential crashes.

**Fix**: Route all signal connections through `_register_handler()`. For singleton services, disconnect handlers on widget destroy.

### 8. Synchronous Hyprland send_command Blocks UI Thread

**Files**: `modules/overview.py`, `modules/dock.py`, `utils/monitors.py`
**Effort**: Medium | **Impact**: Medium

`send_command("j/clients")`, `send_command("j/monitors")`, `send_command("j/activewindow")` block the GTK main loop. The overview's `update()` queries both `j/monitors` and `j/clients` sequentially — two synchronous round-trips.

**Fix**: Use `send_command_async()` with callbacks. Combine related queries into fewer round-trips.

---

## 🥉 Lower Priority

### 10. In-Process Sass Compilation

**Files**: `main.py`, `utils/theme_css.py`
**Effort**: Medium | **Impact**: Low

Uses blocking `exec_shell_command("sass ...")` in a thread (subprocess spawn). Could use `libsass` Python bindings for in-process compilation, avoiding subprocess overhead (~50-200ms per compile).

**Fix**: Replace `exec_shell_command("sass ...")` with Python `import sass` library.

### 13. ScreenRecording Service Uses Gio.Subprocess Directly

**Files**: `services/screen_record.py`
**Effort**: Small | **Impact**: Low

Uses `Gio.Subprocess.new()` with manual `Gio.Task` callbacks instead of `exec_shell_command_async()`.

**Fix**: Refactor to use `exec_shell_command_async()` or `Gio.SubprocessLauncher`.

---

# New Findings (July 2026)

## 🔥 High Priority (New)

### 40. Unnecessary Widget Nesting — EventBoxWidget Wraps Single-Child in Extra Box

**Files**: `shared/widget_container.py`
**Effort**: Small | **Impact**: Medium

`EventBoxWidget.__init__()` creates an `EventBox` → adds a `Box(container_box)` → adds children to that Box. Every widget using `EventBoxWidget` gets an extra Box node in the widget tree for no reason — the EventBox can hold children directly.

```python
# Current — 2 levels
self.container_box = Box(name="widget-container", style_classes=["panel-box"])
self.add(self.container_box)  # EventBox → unnecessary Box

# Fix — 1 level; apply style_classes + name directly to EventBox
self.add(self.container_box)  # → remove, add children to self directly
```

Similarly `ButtonWidget` does `Button` → `Box` (`container_box`) → children. Buttons can hold child widgets directly. The `widget-container` CSS class can be applied to the Button itself.

```python
# Current
self.container_box = Box(style_classes=["widget-container"])
self.add(self.container_box)

# Fix — remove container_box, add children directly to Button
# Button inherits from Bin — supports single child natively
```

**Savings**: Removes 1 Box per button widget (~30+ widgets × 1 Box = 30+ fewer nodes).

## 🥈 Medium Priority (New)

### 44. Unnecessary Widget Nesting — Popup Layout Creates Up to 5 Nested Containers

**Files**: `shared/popup.py`
**Effort**: Medium | **Impact**: Medium

`PopupWindow` uses `make_layout()` which creates:
`BaseWindow` → `Box` (horizontal) → `Box` (_make_v_column) → `Padding(EventBox → Box)` → `PopupRevealer(EventBox → Revealer → child)`

That's **6 container widgets** before the actual content. The `Padding` class is itself `EventBox(child=Box(...))` — an EventBox wrapping a Box.

```python
# Current — Padding class
class Padding(EventBox):
    def __init__(self, ..., style=""):
        super().__init__(
            child=Box(style=style, h_expand=True, v_expand=True),  # ← redundant Box
            ...
        )
```

The `Padding` EventBox can just receive the `style` directly and skip the inner `Box`. Also, for the `top`, `bottom`, and `center` layouts, the padding could be CSS on the parent Box instead of extra EventBox children.

**Fix**:

- Remove `Padding` inner Box, apply style to EventBox directly (or use CSS on parent)
- For `top`/`bottom` layouts, use CSS `margin` on the popup instead of spacer Padding widgets
- For `center` layout, use CSS flexbox-style centering instead of 3 Padding widgets

**Savings**: 1-3 container widgets removed per popup.

#

### 46. Unnecessary Widget Nesting — Dock Revealer Extra Box Wrapper

**Files**: `modules/dock.py` (lines 928-931)
**Effort**: Trivial | **Impact**: Low

```python
self.revealer = Revealer(
    child=Box(children=[self._app_bar], style=padding_style),
    ...
)
```

The `Box` wrapping `self._app_bar` is unnecessary. The `padding_style` can be applied directly to the AppBar (`BoxWidget`) or to the Revealer itself (GTK3 Revealer supports CSS padding).

**Fix**: Apply `padding_style` to `self._app_bar` styling instead of wrapping in a Box.

**Savings**: 1 Box per dock.

### 47. Many Widgets Use `nerd_font_icon()` Result Wrapped in Additional Container

**Files**: `widgets/battery.py`, `widgets/volume.py`, `widgets/brightness.py`, `widgets/power_button.py`, etc.
**Effort**: Medium | **Impact**: Low

`nerd_font_icon()` returns a `Label`. Many widgets then add this Label to a `ButtonWidget.container_box` (which is a `Box`). That means `ButtonWidget(Button)` → `Box(container_box)` → `Label(nerd_font_icon)`. Since `Button` is a `Gtk.Bin` (single-child container), the middle Box is often serving as a pass-through just for multiple children.

Many widgets only have **one child** (just the icon) or **two** (icon + text label). For the single-child case, the icon Label can be set directly as the Button's child, skipping container_box entirely. For two-child cases, a Box is still needed but could be the direct container without the widget-container name/style overhead.

**Fix**: Add a `set_child()` method to `ButtonWidget` that sets the button's direct child for single-child widgets, bypassing `container_box`.

**Savings**: 1 Box per single-child widget (~half of all widgets).

---

## 🥉 Lower Priority (New)

### 49. `shared/widget_container.py` — `EventBoxWidget` Always Creates `container_box` Even if Empty

**Files**: `shared/widget_container.py` (line 144)
**Effort**: Trivial | **Impact**: Low

`EventBoxWidget.__init__()` always creates `self.container_box = Box(name=..., style_classes=...)` and adds it, even if the subclass never adds children. At minimum this is an invisible empty Box in the widget tree.

**Fix**: Lazily create `container_box` only when children are actually added, or allow opting out.

## 🔥 High Priority (New)

### 16. LockKeys OSD Polls hyprctl at 200ms — 5x/second Subprocess Spawn

**Files**: `modules/osds/lockkeys.py`, `utils/constants.py`
**Effort**: Small | **Impact**: Medium

The LockKeys OSD polls `hyprctl devices -j` every **200ms** by default. Each poll spawns a subprocess, parses JSON output, and updates GTK widgets. That's 5 subprocess spawns/second just for capslock/numlock state detection — which changes maybe once per session.

**Fix**:

- Increase default `poll_interval` to 2000ms (2 seconds) — keyboard lock state doesn't change rapidly enough to warrant 200ms
- Switch to listening for keyboard events via DBus or `hyprctl` event socket instead of polling
- Or use `exec_shell_command_async` and cache the last result, only updating UI on actual changes

### 17. DnsSwitcher Service Polls nmcli Every 3s Unconditionally

**Files**: `services/dns_switcher.py`
**Effort**: Small | **Impact**: Medium

`DnsSwitcherService` polls `nmcli -t -f UUID con show --active` every 3 seconds via `GLib.timeout_add`. Each poll involves a blocking `exec_shell_command()` call. The poll never pauses — it runs even when no DNS switcher widget is visible.

**Fix**: Add `pause_polling()`/`resume_polling()` methods (like CloudflareWarpService already has) and connect to widget map/unmap events. Increase default interval to 5000ms+.

### 18. CloudflareWarp Service Polls warp-cli Every 5s Unconditionally at Module Level

**Files**: `services/cloudflare_warp.py`
**Effort**: Small | **Impact**: Low

Similar to DnsSwitcher — polls `warp-cli status` every 5 seconds. The widget does connect map/unmap to pause/resume polling, but the **service singleton starts polling in `__init__`** — whenever `services/cloudflare_warp.py` is imported (typically at widget module load time), polling begins immediately, even before any widget is created or mapped.

**Fix**: Defer starting the poll timer to first widget map event instead of `__init__`. Or default to paused state and only start on first widget map.

### 20. Privacy Service Calls pw-dump Synchronously on Main Thread

**Files**: `services/privacy.py`
**Effort**: Small | **Impact**: Medium

`_load_pipewire_objects()` calls `exec_shell_command("pw-dump")` synchronously. `pw-dump` can produce several megabytes of JSON output. This is called from the privacy indicator's repeater (every 3500ms). Blocks the GTK main loop during execution.

**Fix**: Move `exec_shell_command("pw-dump")` to a background thread, parse the JSON there, then idle_add the result back to the main thread.

---

## 🥈 Medium Priority (New)

### 25. LockKeys OSD Does Not Use TeardownMixin for Timer Cleanup

**Files**: `modules/osds/lockkeys.py`
**Effort**: Small | **Impact**: Low

`LockkeysOSDContainer` manages `_poll_timer` manually with `do_destroy()` calling `cleanup()`. It does **not** use `TeardownMixin` from `shared/widget_container.py`. This is inconsistent with the pattern used by other widgets and could miss cleanup in edge cases.

**Fix**: Switch to `TeardownMixin` and use `_register_repeater()` for the poll timer.

### 26. CloudflareWarp Service Uses Raw exec_shell_command Instead of Async

**Files**: `services/cloudflare_warp.py`
**Effort**: Small | **Impact**: Low

`_run_warp_cli()` calls `exec_shell_command(f"warp-cli {action}")` synchronously. The poll function uses `exec_shell_command_async` but action calls are synchronous.

**Fix**: Replace synchronous `exec_shell_command` with `exec_shell_command_async` for all warp-cli invocations.

---

## 🥉 Lower Priority (New)

### 34. Notification Timer Uses invoke_repeater at 250ms for Second-Level Timeouts

**Files**: `modules/notification.py`
**Effort**: Trivial | **Impact**: Low

Although the old 10ms interval was already fixed to 250ms (per OPTIMIZATIONS.md fix notes), 250ms is still 4x more wake-ups than needed for timeouts measured in seconds. A 500ms or 1000ms tick would be sufficient for notification auto-dismiss.

**Fix**: Change to 500ms interval.

### 36. ConfigWatcher Uses Raw subprocess.Popen for Restart

**Files**: `utils/config_watcher.py`
**Effort**: Small | **Impact**: Low

`_restart_tsumiki()` calls `subprocess.Popen([self.init_script, "-restart"], ...)` directly. This is a raw subprocess call outside the abstraction layer in `utils/functions.py`.

**Fix**: Replace with `exec_shell_command_async()` or centralize via `utils/functions.py`'s `toggle_command()` pattern.

### 37. utils/functions.py Imports Many Modules at Top Level Used Only in Specific Functions

**Files**: `utils/functions.py`
**Effort**: Medium | **Impact**: Low

Several module-level imports are only used in specific functions:

- `psutil` — only used in `uptime()`
- `html` — only used in `parse_markup()`
- `shutil` — only used in `cleanup_temp_resources()`
- `importlib` — only used in `lazy_load_class()`
- `string.Formatter` — only used in `_get_named_format_keys()`
- `BytesIO` — only used in `make_qrcode()`
- `Counter` — only used in `_pillow_worker()`

These add import overhead at module load time even when the features are never used.

**Fix**: Move these imports inside their respective functions (lazy imports). For `psutil`, it's already imported by `stats_poll()` in `widget_utils.py`, so it's already in memory — the import is fast but unnecessary.
