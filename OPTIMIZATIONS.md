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

### 50. Stats Widget GPU Polling Blocks Main Thread

**Files**: `widgets/stats.py` (line 147)
**Effort**: Small | **Impact**: Medium

`_poll_gpu_stats()` calls `exec_shell_command("nvtop -s")` synchronously, blocking the GTK main loop. This runs every `_gpu_poll_interval` seconds (default 2s). The `nvtop -s` command spawns a subprocess and parses JSON output — both blocking operations.

```python
# Current — blocks main thread
out = exec_shell_command("nvtop -s")
data = json.loads(out)

# Fix — run in background
exec_shell_command_async("nvtop -s", callback=self._on_gpu_stats_received)
```

**Fix**: Use `exec_shell_command_async()` with a callback. Cache the last result and only update UI on actual changes.

### 51. USB Manager lsblk Polling Blocks Main Thread

**Files**: `widgets/usb_manager.py` (line 187)
**Effort**: Small | **Impact**: Medium

`refresh_devices()` calls `exec_shell_command("lsblk -J ...")` synchronously. This blocks the GTK main loop during device enumeration. The `lsblk` command can take 100-500ms depending on the number of devices.

```python
# Current — blocks main thread
output = exec_shell_command("lsblk -J -o NAME,PATH,TYPE,SIZE,...")

# Fix — run in background
exec_shell_command_async("lsblk -J ...", callback=self._on_lsblk_ready)
```

**Fix**: Use `exec_shell_command_async()` with a callback. The animation (refresh button spin) can continue while the command runs.

### 52. Git Companion GitHub API Calls Block Main Thread

**Files**: `widgets/git_companion.py` (line 82)
**Effort**: Small | **Impact**: Medium

`_run_gh_command()` calls `exec_shell_command(cmd_str)` synchronously. GitHub CLI commands (`gh`) can take 1-5 seconds depending on network latency. This blocks the entire GTK main loop during API calls.

```python
# Current — blocks main thread
result = exec_shell_command(cmd_str)

# Fix — run in background
exec_shell_command_async(cmd_str, callback=self._on_gh_result)
```

**Fix**: Use `exec_shell_command_async()` with a callback. Show a loading state while the command runs.

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

### 53. Sass Compilation Blocks Main Thread During Theme Switch

**Files**: `services/style.py` (line 310)
**Effort**: Medium | **Impact**: Medium

`_compile_sass()` calls `exec_shell_command("sass styles/main.scss ...")` synchronously. Sass compilation can take 100-500ms. This blocks the GTK main loop during theme switching, causing visible UI freeze.

```python
# Current — blocks main thread
output = exec_shell_command(f"sass styles/main.scss {CSS_PATH} --no-source-map")

# Fix — run in background thread
exec_shell_command_async(
    f"sass styles/main.scss {CSS_PATH} --no-source-map", callback=self._on_sass_compiled
)
```

**Fix**: Move Sass compilation to a background thread. Use `exec_shell_command_async()` or `threading.Thread()`. Apply CSS via `idle_add()` after compilation completes.

### 54. Matugen Color Generation Blocks Main Thread

**Files**: `services/matugen.py` (line 85)
**Effort**: Small | **Impact**: Medium

`generate_colors()` calls `exec_shell_command(cmd)` synchronously. Matugen can take 1-3 seconds to generate color palettes. This blocks the GTK main loop during theme generation.

```python
# Current — blocks main thread
exec_shell_command(cmd)

# Fix — run in background
exec_shell_command_async(cmd, callback=self._on_colors_generated)
```

**Fix**: Use `exec_shell_command_async()` with a callback. Emit `colors_generated` signal from the callback.

### 55. Sinewave Slider 60fps Animation Loop Wastes CPU

**Files**: `shared/sinewave_slider.py` (line 144)
**Effort**: Small | **Impact**: Low

`SinewaveSlider.__init__()` starts a 60fps animation loop (`GLib.timeout_add(16, self._tick)`) immediately on creation. The animation runs continuously even when the slider is not visible or not being interacted with.

```python
# Current — always running
self._anim_id: int | None = GLib.timeout_add(16, self._tick)

# Fix — only run when visible/interacting
self.connect("map", self._start_animation)
self.connect("unmap", self._stop_animation)
```

**Fix**: Start the animation loop only when the widget is mapped (visible). Stop it when unmapped. Use `_register_repeater()` for proper cleanup.

### 56. Icon Resolver File I/O on Main Thread

**Files**: `utils/icon_resolver.py` (line 118)
**Effort**: Small | **Impact**: Low

`_resolve_icon_name()` reads `.desktop` files synchronously with `open(desktop_file_path, "r")`. This blocks the GTK main loop during icon resolution. Desktop files are typically small (1-10KB), but the I/O can still cause micro-stutters.

```python
# Current — blocks main thread
with open(desktop_file_path, "r") as f:
    content = f.read()


# Fix — cache resolved icons
@lru_cache(maxsize=256)
def _resolve_icon_name(self, desktop_file_path: str) -> str | None: ...
```

**Fix**: Cache resolved icon names with `@lru_cache`. Desktop files rarely change during a session.

### 57. Weather Cache File I/O on Main Thread

**Files**: `services/weather.py` (line 306)
**Effort**: Small | **Impact**: Low

`_load_cached_weather()` reads JSON from disk synchronously with `open(WEATHER_CACHE_FILE, "r")`. Weather cache files are typically 5-50KB.

```python
# Current — blocks main thread
with open(WEATHER_CACHE_FILE, "r") as f:
    cached_data = json.load(f)

# Fix — cache in memory after first load
self._cached_weather = None  # populated on first read
```

**Fix**: Cache the parsed weather data in memory. Only re-read from disk if the file modification time changes.

### 58. Emoji Picker Loads JSON on Every Open

**Files**: `widgets/emoji_picker.py` (line 107)
**Effort**: Small | **Impact**: Low

`_load_emoji_data()` reads `emoji.json` from disk every time the picker is opened. The file is typically 200-500KB.

```python
# Current — reads from disk every time
with open(self._emoji_file_path, "r") as f:
    data = json.load(f)

# Fix — cache after first load
if self._emoji_data is None:
    with open(self._emoji_file_path, "r") as f:
        self._emoji_data = json.load(f)
return self._emoji_data
```

**Fix**: Cache the parsed emoji data in a class variable or module-level cache. The emoji list is static and doesn't change during a session.

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

### 59. Kanban GLib.timeout_add Without Cleanup Tracking

**Files**: `widgets/kanban.py` (line 200)
**Effort**: Trivial | **Impact**: Low

`InlineEditor` uses `GLib.timeout_add(200, lambda: ...)` without tracking the timer ID. If the widget is destroyed before the timeout fires, the callback may run on a destroyed widget.

```python
# Current — no cleanup
GLib.timeout_add(200, lambda: (editor.text_view.grab_focus(), False))

# Fix — use _register_repeater for cleanup
self._register_repeater(
    GLib.timeout_add(200, lambda: (editor.text_view.grab_focus(), False))
)
```

**Fix**: Use `_register_repeater()` to track the timer ID and ensure cleanup on destroy.

### 60. USB Manager _run_command Blocks Main Thread

**Files**: `widgets/usb_manager.py` (line 483)
**Effort**: Small | **Impact**: Low

`_run_command()` calls `exec_shell_command(command)` synchronously. USB operations (mount, unmount, eject) can take 100ms-2s. This blocks the GTK main loop during device operations.

```python
# Current — blocks main thread
exec_shell_command(command)

# Fix — run in background
exec_shell_command_async(command, callback=self._on_action_done)
```

**Fix**: Use `exec_shell_command_async()` with a callback. The refresh animation can continue while the command runs.

---

## 📊 Summary

| Priority  | Count | Total Effort | Total Impact |
| --------- | ----- | ------------ | ------------ |
| 🔥 High   | 5     | Medium       | High         |
| 🥈 Medium | 8     | Medium       | Medium       |
| 🥉 Lower  | 7     | Small        | Low          |

**Top 3 Quick Wins (High Impact, Low Effort):**

1. **Stats GPU polling** (#50) — Move `nvtop -s` to async, 10 min fix
2. **USB Manager lsblk** (#51) — Move `lsblk` to async, 10 min fix
3. **Git Companion GitHub API** (#52) — Move `gh` to async, 15 min fix

**Top 3 Architectural Improvements (High Impact, Medium Effort):**

1. **Thread safety for Stats Fabricator** (#1) — Prevents race conditions
2. **Lazy gi.repository imports** (#4) — Faster startup
3. **Sass compilation to background** (#53) — Eliminates UI freeze on theme switch
