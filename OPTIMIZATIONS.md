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



### 15. Battery Service Creates Separate DBus Connection
**Files**: `services/battery.py`
**Effort**: Small | **Impact**: Low

Creates its own `GioDBusHelper` instance for UPower communication, adding a separate DBus connection.

**Fix**: Investigate sharing DBus connections between services or using fabric's built-in DBus integration.

---

# New Findings (July 2026)

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


### 38. Widget Config Boilerplate in `_settings.scss` and `_widgets.scss`
**Files**: `styles/_settings.scss`, `styles/common/_widgets.scss`
**Effort**: Medium | **Impact**: High

Every widget declares the same 5 variables in `_settings.scss`:
```scss
$bar-widgets-{x}-border-enabled: false;
$bar-widgets-{x}-border-radius: 16px;
$bar-widgets-{x}-border-width: 1px;
$bar-widgets-{x}-icon_size: 14px;
$bar-widgets-{x}-spacing: 0.125em;
```

This is repeated for ~30 widgets = ~150 near-identical variable declarations. Then `_widgets.scss` mirrors this with a 30-entry tuple list (`$widget-shell-widgets`) consumed by a `@each` loop. Adding a new widget requires touching 3 files with ~25 lines of repetition.

**Fix**: Collapse into a single SCSS map and generate both variables and `@each` loops from it:
```scss
$widget-configs: (
  "battery":   (border-radius: 16px, border-enabled: false, border-width: 1px, icon-size: 14px, spacing: 0.125em),
  "bluetooth": (border-radius: 16px, border-enabled: false, border-width: 1px, icon-size: 12px, spacing: 0.125em),
  // ... all widgets
);
```
Use `@each` to declare variables and generate widget-shell blocks from a single source of truth.

### 39. `transition: all` Replaced with Specific Properties (Resolved)
**Files**: `styles/_dock.scss`, `styles/_overview.scss`, `styles/common/_common.scss`
**Effort**: Small | **Impact**: Medium
**Status**: ✅ Fixed in this session

4 instances of `transition: all` were replaced with explicit property lists:

| File | Before | After |
|------|--------|-------|
| `_dock.scss` (#dock-bar) | `transition: all 0.25s` | `background-color, padding, margin, border-radius, border-color` |
| `_overview.scss` (overlay elements) | `transition: all 0.1s` | `background-color` |
| `_common.scss` (check, radio) | `transition: all 75ms` | `background-color, color, box-shadow` (75ms/150ms separate) |
| `_common.scss` (switch) | `transition: all 75ms` | `background-color, opacity` |
| `_common.scss` (switch slider) | `transition: all 75ms` | `background-color, margin` |

`transition: all` forces the compositor to check every animatable property on each frame. Explicit lists restrict animations to only the properties that actually change.

**Note**: `_workspace.scss` already used specific properties via `$workspace-transition` — no change needed.


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


### 40. Hardcoded Border Values in `_dns_switcher.scss` and `_cloudflare_warp.scss`
**Files**: `styles/_dns_switcher.scss`, `styles/_cloudflare_warp.scss`
**Effort**: Small | **Impact**: Low

Both files use literal values instead of settings variables:
```scss
// _dns_switcher.scss
@include common.widget_border(16px, false, 1px);

// _cloudflare_warp.scss
@include common.widget_border(16px, false, 1px);
```

These bypass the entire `_settings.scss` variable system, making them unconfigurable.

**Fix**: Add proper settings variables (e.g., `$bar-widgets-dns_switcher-border-radius`, `$bar-widgets-cloudflare_warp-border-radius`) and reference them from the `@include`.

### 41. Mixed Naming Convention in `_theme.scss`
**Files**: `styles/_theme.scss`
**Effort**: Small | **Impact**: Low

Theme variable names mix underscore and hyphen inconsistently:
```scss
$general-bar_background          // hyphen + underscore
$accent-light_blue               // underscore after hyphen
$text-muted_dark                 // underscore after hyphen
$text-muted_light                // underscore after hyphen
```

Compare with consistently-hyphenated names like `$accent-blue`, `$background-dark`, `$surface-disabled`.

**Fix**: Normalize to all-hyphenated: `$general-bar-background`, `$accent-light-blue`, `$text-muted-dark`, `$text-muted-light`. Update all references across the codebase.

### 42. Hardcoded Colors and Unused Import in `_media.scss`
**Files**: `styles/_media.scss`
**Effort**: Small | **Impact**: Low

Two issues:
1. Hardcoded `black` instead of theme variable:
```scss
text-shadow: 1px 1px 3px black;
box-shadow: 0 0 4px 0 black;
```

2. Unnecessary `sass:math` import — only used for `math.floor()` (single use, SCSS handles division natively).

**Fix**: Replace `black` with `theme.$general-shadow-color`. Remove `@use "sass:math";` and replace `math.floor()` with native division.


---

## 🥉 Lower Priority (New)

### 29. Duplicate Functions Across shell.py and functions.py
**Files**: `utils/shell.py`, `utils/functions.py`
**Effort**: Small | **Impact**: Low

Multiple functions are duplicated between these files:
- `set_process_name()` — both files have the same `ctypes.CDLL("libc.so.6")` implementation
- `kill_process()` — identical `pkill` wrapper in both
- `is_app_running()` — identical `pidof` wrapper in both
- `check_executable_exists()` — identical `GLib.find_program_in_path` wrapper in both
- `play_sound()` — identical `pw-play` wrapper in both
- `toggle_command()` — identical `subprocess.Popen` wrapper in both

This creates maintenance burden and potential drift.

**Fix**: Consolidate all process/shell utilities into `utils/shell.py` and import from there in `utils/functions.py`, or vice versa. Remove the duplicate definitions.


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

### 43. Dead Variable Declarations for `radio_player`
**Files**: `styles/_settings.scss`
**Effort**: Trivial | **Impact**: Low

`_settings.scss` declares a full set of variables for `radio_player`:
```scss
$bar-widgets-radio_player-border-enabled: false;
$bar-widgets-radio_player-border-radius: 16px;
$bar-widgets-radio_player-border-width: 1px;
$bar-widgets-radio_player-icon_size: 12px;
$bar-widgets-radio_player-spacing: 0.125em;
```

No `_radio_player.scss` file or widget exists in the codebase. These variables are compiled into the CSS but never referenced.

**Fix**: Remove the dead variable declarations.

### 44. Deep Nesting in `_datemenu.scss`
**Files**: `styles/_datemenu.scss`
**Effort**: Small | **Impact**: Low

The `#datemenu-notification-box` selector is nested up to 9 levels deep within `#date_time-menu > #notification-column > .notification-scrollable > ...`. While GTK CSS doesn't suffer from the specificity issues of web CSS, deep nesting hurts readability and generates large compiled selectors.

**Fix**: Flatten deeply nested blocks with intermediate `// --- section ---` comments. Extract some deeply-nested groups into their own top-level selectors (e.g., `#datemenu-notification-box` could be a flat rule).

### 45. Inconsistent Local Variable Naming in `_media.scss`
**Files**: `styles/_media.scss`
**Effort**: Trivial | **Impact**: Low

Local variable `$player_width` uses snake_case but the rest of the codebase uses kebab-case for SCSS variables. `$player_height`, `$image_size`, `$inner_player_width` are inconsistent.

**Fix**: Rename to `$player-width`, `$player-height`, `$image-size`, `$inner-player-width`.

### 46. Fragile `if(sass(...): ...)` Pattern in `_common.scss`
**Files**: `styles/common/_common.scss`, `styles/_workspace.scss`
**Effort**: Small | **Impact**: Low

Several files use an inline conditional syntax that's syntactically fragile:
```scss
border: if(sass(variable.$bar-menus-tooltip-border-enabled): variable.$border; else: none);
```

This embeds colons and semicolons inside parentheses, which is valid Dart Sass but easy to break. Used in `tooltip`, `#workspaces_widget > button.active`, and `floating-widget` mixin.

**Fix**: Replace with standard `@if` / `@else` blocks for clarity and robustness.

### 47. Duplicate `separator` Color Declarations in `_datemenu.scss`
**Files**: `styles/_datemenu.scss`
**Effort**: Trivial | **Impact**: Low

`separator` is declared at two levels with different colors:
- Bar separator: `background-color: variable.$border-color`
- Menu separator: `background-color: color.mix(variable.$popover-border-color, black, 60%)`

The bar and menu are different elements, but using the same element selector with different colors in nested contexts could cause confusion.

**Fix**: Use more specific class-based selectors (e.g., `.datemenu-bar-separator`, `.datemenu-menu-separator`) or named variables to make the intent clear.
