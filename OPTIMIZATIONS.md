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

### 2. ConfigWatcher Still Uses Raw subprocess
**Files**: `utils/config_watcher.py`
**Effort**: Small | **Impact**: Low

`_restart_tsumiki()` uses `subprocess.Popen([self.init_script, "-restart"], ...)` — the last remaining raw `subprocess` call outside of `utils/functions.py`'s abstraction layer.

**Fix**: Replace `subprocess.Popen(...)` with `exec_shell_command_async(f"{self.init_script} -restart", lambda *_: None)`.

### 3. CloudflareWarpService Still Polls and Uses Raw subprocess
**Files**: `services/cloudflare_warp.py`
**Effort**: Small | **Impact**: Low

Polls `warp-cli status` every 5 seconds unconditionally. Also uses raw `subprocess.run(["warp-cli", action], ...)` in `_run_warp_cli()`.

**Fix**: Pause polling on widget unmap/resume on map. Replace `subprocess.run` with `exec_shell_command`.

### 4. Expensive gi.repository Imports at Module Level
**Files**: `services/network.py`, `services/mpris.py`, `shared/scrollable_text.py`, `shared/popover.py`, `widgets/quick_settings/submenu/wifi.py`
**Effort**: Medium | **Impact**: Medium

`gi.repository` imports (NM, Playerctl, PangoCairo, GtkLayerShell) are loaded at module import time, not deferred. These are C extension modules with significant overhead. `services/network.py` and `services/mpris.py` import them at the top level even if the service is never used (e.g., network widget disabled).

**Fix**: Move `gi.repository` imports into lazy initializers or inside `__init__` methods so they only load when the service/widget is actually instantiated. NetworkManager and Playerctl introspection are particularly expensive.

---

## 🥈 Medium Priority

### 5. GTK Frame Clock for Animations
**Files**: `shared/animator.py`, `shared/animated/scale.py`
**Effort**: Medium | **Impact**: Medium

- `shared/animator.py` — falls back to `GLib.timeout_add(16ms)` when no `tick_widget`. Misses vsync. The widget-path (`add_tick_callback`) already exists.
- `shared/animated/scale.py` — uses `GLib.timeout_add(50ms)` instead of frame clock.

**Fix**: Use `add_tick_callback` (GTK frame clock) for sub-second animations instead of `timeout_add`.

### 6. Signal Connection Leaks (Many Widgets Bypass TeardownMixin)
**Files**: `widgets/battery.py`, `widgets/bluetooth.py`, `widgets/volume.py`, `widgets/datetime_menu.py`, `widgets/kanban.py`, `services/network.py`, `widgets/quick_settings/submenu/bluetooth.py`, `widgets/quick_settings/togglers.py`, `widgets/settings_gui.py`
**Effort**: Medium | **Impact**: Medium

Many widgets connect to signals directly without using `_register_handler()` from `TeardownMixin`. When the widget is destroyed, these signal handlers remain connected to the source object. For singleton services that outlive widgets, stale callbacks can cause memory leaks and potential crashes.

**Fix**: Route all signal connections through `_register_handler()`. For singleton services, disconnect handlers on widget destroy.

### ~~7. Timer Cleanup Gaps (Some Widgets Bypass TeardownMixin)~~
**Files**: `widgets/clipboard.py`, `widgets/usb_manager.py`, `widgets/pomodoro.py`, `modules/desktop_clock.py`, `widgets/kanban.py`, `widgets/breathing.py`
**Effort**: Medium | **Impact**: Medium

✅ Done — Routed through TeardownMixin via `_register_repeater()`:
- `clipboard.py` — `_search_timer_id` in `on_search_text_changed()`
- `usb_manager.py` — `_refresh_timer_id` in `_on_action_done()`
- `pomodoro.py` — `timer_id` in `start()` and `_transition_phase()`
- `desktop_clock.py` — `_tick_id` for the clock tick

**Intentionally left as-is:**
- `kanban.py` — one-shot 50ms `GLib.timeout_add` on `KanbanNote` (inherits `EventBox`, not `TeardownMixin`). Self-cleaning, fires once and auto-removes. Harmless.
- `breathing.py` — `BreathingMenu(BoxWidget)` manages `_timer_id` manually with `GLib.source_remove()` in `_stop_exercise()`, `_toggle_pause()`, and `_schedule_tick()`. Destroy handler calls `_stop_exercise()`. Already thorough.

### 8. Synchronous Hyprland send_command Blocks UI Thread
**Files**: `modules/overview.py`, `modules/dock.py`, `utils/monitors.py`
**Effort**: Medium | **Impact**: Medium

`send_command("j/clients")`, `send_command("j/monitors")`, `send_command("j/activewindow")` block the GTK main loop. The overview's `update()` queries both `j/monitors` and `j/clients` sequentially — two synchronous round-trips.

**Fix**: Use `send_command_async()` with callbacks. Combine related queries into fewer round-trips.

### 9. Unbuffered os.path.exists Calls on Hot Paths
**Files**: `utils/icon_resolver.py`, `services/weather.py`, `services/quotes.py`, `services/custom_notification.py`, `services/brightness.py`, `services/privacy.py`, `widgets/system_tray.py`
**Effort**: Small | **Impact**: Low

Multiple services and widgets call `os.path.exists()` directly on the filesystem without caching the result. For example:
- `utils/icon_resolver.py` — checks `ICON_CACHE_FILE` exists on every `_ensure_cache_loaded()`
- `services/brightness.py` — checks brightness paths on each poll
- `services/privacy.py` — scans `/sys/class/video4linux` and `/proc` on each update
- `widgets/system_tray.py` — checks icon paths repeatedly

Each call is a syscall. Privacy scanning of `/sys` and `/proc` is particularly expensive.

**Fix**: Cache filesystem existence checks with TTL. For frequently checked paths, store in a dict with a refresh interval. For privacy service, debounce `/sys`/`/proc` scans.

---

## 🥉 Lower Priority

### 10. In-Process Sass Compilation
**Files**: `main.py`, `utils/theme_css.py`
**Effort**: Medium | **Impact**: Low

Uses blocking `exec_shell_command("sass ...")` in a thread (subprocess spawn). Could use `libsass` Python bindings for in-process compilation, avoiding subprocess overhead (~50-200ms per compile).

**Fix**: Replace `exec_shell_command("sass ...")` with Python `import sass` library.

### 11. Notification Timer Fires at 10ms
**Files**: `modules/notification.py`
**Effort**: Trivial | **Impact**: Low

`invoke_repeater(10, self._timer_tick)` fires 100 times per second for notification timeouts measured in seconds.

**Fix**: Change to `invoke_repeater(250, self._timer_tick)` — reduces CPU wake-ups by 96%.

### 12. Excessive Style Class Churn
**Files**: `modules/dock.py`, `widgets/datetime_menu.py`, `widgets/cheatsheet.py`, `widgets/git_companion.py`, `widgets/quick_settings/submenu/power_profiles.py`
**Effort**: Small | **Impact**: Low

`add_style_class("active")` / `remove_style_class("active")` per-button triggers individual GTK style recalc. `dock.py` does this for every client button on every sync.

**Fix**: Use `set_style_classes()` atomically. For bulk updates, collect changes and apply once.

### 13. ScreenRecording Service Uses Gio.Subprocess Directly
**Files**: `services/screen_record.py`
**Effort**: Small | **Impact**: Low

Uses `Gio.Subprocess.new()` with manual `Gio.Task` callbacks instead of `exec_shell_command_async()`.

**Fix**: Refactor to use `exec_shell_command_async()` or `Gio.SubprocessLauncher`.

### 14. Clipboard Widget Heavy Subprocess Launcher Usage
**Files**: `widgets/clipboard.py`
**Effort**: Small | **Impact**: Low

Creates new `Gio.SubprocessLauncher` instances per clipboard operation. Clipboard history re-queried on every toggle with no caching.

**Fix**: Cache clipboard history with a TTL. Reuse `Gio.SubprocessLauncher` instances.

### 15. Battery Service Creates Separate DBus Connection
**Files**: `services/battery.py`
**Effort**: Small | **Impact**: Low

Creates its own `GioDBusHelper` instance for UPower communication, adding a separate DBus connection.

**Fix**: Investigate sharing DBus connections between services or using fabric's built-in DBus integration.

### 16. Widget Tree Rebuilds on Small State Changes
**Files**: `widgets/kanban.py`, `widgets/clipboard.py`
**Effort**: Medium | **Impact**: Low

Several widgets destroy and recreate entire GTK widget subtrees when a single item changes (clipboard history toggle, kanban card refresh).

**Fix**: Add/remove individual list items instead of rebuilding whole containers. Pre-allocate widget pools for bounded lists.

### 17. HTTP Client Instances Created Per Request
**Files**: `services/weather.py`, `services/quotes.py`, `widgets/ip_monitor.py`, `widgets/git_companion.py`, `shared/media.py`
**Effort**: Small | **Impact**: Low

Multiple HTTP clients created independently:
- `weather.py` and `quotes.py` each create their own `httpx.Client`
- `ip_monitor.py` and `git_companion.py` use `urllib.request.urlopen()` (no connection pooling)
- `shared/media.py` also uses `urllib`

No shared session or connection pool between these.

**Fix**: Create a shared `httpx.Client` session that all services reuse, providing connection pooling and consistent timeout/retry configuration.

### 18. Dead Code: Unreferenced Private Methods
**Files**: Potentially across the codebase
**Effort**: Medium | **Impact**: Low

Multiple private methods defined but potentially never called (e.g., `_on_enter_notify`, `_recreate_bars`, `_start_polling` in lockkeys.py, various `_build_*` methods). Dead code adds compilation overhead and confuses maintainers.

**Fix**: Audit for unreferenced methods with a tool like `vulture` or manual grep for method references. Remove or document.

### 19. Regex Compilation at Module Import Time
**Files**: `services/privacy.py`, `utils/functions.py`, `utils/icon_resolver.py`, `services/dns_switcher.py`, `widgets/system_tray.py`
**Effort**: Trivial | **Impact**: Low

Module-level `re.compile()` calls are evaluated at import time even if the regex is never used (e.g., privacy indicator patterns when the widget is disabled).

**Fix**: Move regex compilation inside the functions/methods that use them, or defer to a lazy property.

### ~~20. Cache Expiration Gaps in LRU Caches~~
**Files**: `modules/overview.py`, `utils/icon_resolver.py`
**Effort**: Small | **Impact**: Low

✅ Done — `_resolve_icon_pixbuf` in `overview.py` and `get_icon_pixbuf` in `icon_resolver.py` switched from `@lru_cache(maxsize=256)` to `@ttl_lru_cache(seconds_to_live=3600, maxsize=256)`. Animation math caches (`lerp`, `steps`, `cubic_bezier`) left as-is because TTL batch-invalidation would cause performance regressions mid-animation. `circle_image.py` `_load_pixbuf_cached` left as-is (maxsize=64 is already small).
