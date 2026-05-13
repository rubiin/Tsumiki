I’ll scan for eager service/widget initialization and heavy imports, then map concrete lazy-load candidates with low-risk refactor ideas. I’m starting with targeted searches across module bootstrap paths and shared service access patterns.

I’m running a fast read-only search to locate current lazy-loading mechanisms and the main startup hot paths so we can spot what is still eagerly loaded.

Searched for regex `lazy|Lazy|_LazyServiceProxy|lazyload|lazy_load` (`**/*.py`), 48 results

Searched for regex `import .*services|from services import|from modules import|get_hyprland_connection` (`**/*.py`), 36 results

Searched for files matching `**/modules/**/*.py`, 17 matches

I found existing lazy-loading infrastructure already in place for widgets and services, so next I’m checking startup entry points and module constructors to identify what is still eagerly instantiated and worth deferring.

Read [](file:///home/devina/.config/tsumiki/main.py)

Read [](file:///home/devina/.config/tsumiki/modules/bar.py#1-1), lines 1 to 260

Read [](file:///home/devina/.config/tsumiki/services/__init__.py)

I confirmed startup already lazily imports most widgets/services; now I’m auditing module internals for eager object creation that still happens even when features aren’t used.

Read [](file:///home/devina/.config/tsumiki/modules/osd.py)

Read [](file:///home/devina/.config/tsumiki/widgets/quick_settings/quick_settings.py#1-1), lines 1 to 320

Read [](file:///home/devina/.config/tsumiki/modules/overview.py#1-1), lines 1 to 260

Read [](file:///home/devina/.config/tsumiki/modules/dock.py#1-1), lines 1 to 340

Read [](file:///home/devina/.config/tsumiki/widgets/quick_settings/quick_settings.py#320-320), lines 320 to 595

I’ve pinpointed likely hotspots in quick settings and dock; next I’m doing a quick cross-file scan for eagerly created services/managers to produce a concrete lazy-loading checklist.

Searched for regex `=\s*(NetworkService|BrightnessService|MprisPlayerManager|AppUtils|get_hyprland_connection)\(` (`**/*.py`), 25 results

Searched for regex `from modules\.app_launcher import AppLauncher|from services\.network import NetworkService|from services\.brightness import BrightnessService` (`**/*.py`), 9 results

Read [](file:///home/devina/.config/tsumiki/modules/notification.py#1-1), lines 1 to 240

Read [](file:///home/devina/.config/tsumiki/widgets/datetime_menu.py#1-1), lines 1 to 260

Read [](file:///home/devina/.config/tsumiki/utils/icons.py#1-1), lines 1 to 260

Searched for regex `^[A-Za-z_][A-Za-z0-9_]*\s*=\s*[A-Z][A-Za-z0-9_]*\(` (`**/*.py`), 96 results

Read [](file:///home/devina/.config/tsumiki/utils/config.py)

Read [](file:///home/devina/.config/tsumiki/utils/decorators.py)

Read [](file:///home/devina/.config/tsumiki/modules/app_launcher.py#1-1), lines 1 to 260

Read [](file:///home/devina/.config/tsumiki/widgets/mpris.py)

Searched for regex `AppUtils\(|invoke_repeater\(|exec_shell_command_async\(|send_command\("j/` (`**/*.py`), 59 results

I’ve finished the scan and found several concrete lazy-load opportunities, mostly in quick settings, dock, and global utility initialization. I’ll now summarize them by impact with exact file locations and what to defer.

Audit complete. You already have solid lazy-loading in place for widgets and core services:
- bar.py uses lazy widget class imports.
- __init__.py uses lazy service proxies.

Best remaining lazy-load targets:

1. Quick settings panel services are eagerly created on widget init
- quick_settings.py
- quick_settings.py
- Why: NetworkService and BrightnessService start even if user never opens quick settings.
- Lazyload idea: instantiate these in show_popover or first icon refresh, then cache.

2. Dock imports AppLauncher eagerly at module import
- dock.py
- Why: pulls launcher code even if launcher button is never clicked.
- Lazyload idea: move import into on_launcher_clicked, similar to existing lazy instance creation at dock.py.

3. Dock and overview build full app registries immediately
- dock.py
- overview.py
- Why: AppUtils scans desktop apps; this can be expensive on startup.
- Lazyload idea: defer AppUtils construction until first window list render or first unknown app id.

4. Global ThreadPoolExecutor is created at import time
- decorators.py
- Why: thread pool starts even if threading helpers are unused.
- Lazyload idea: create pool on first thread/run_in_thread call.

5. Global config singleton loads config and writes SCSS at import time
- config.py
- Why: importing this module triggers disk I/O and background work immediately.
- Lazyload idea: instantiate configuration inside main startup path only, expose getter instead of module-global object.

6. Overview creates many hyprland connections per window button/workspace widget
- overview.py
- overview.py
- Why: repeated connection retrieval/usage objects.
- Lazyload idea: pass one shared connection from menu/container into child objects.

7. Large weather icon map is always imported with general icon utilities
- icons.py
- Why: very large weather dictionary is loaded even when weather widget is not used.
- Lazyload idea: split weather mappings into a weather-only module loaded by weather widget.

Skeptical note:
- Not everything should be lazy. For always-visible widgets (for example dock when enabled), delaying too much can cause first-interaction jank. The best wins are where objects are initialized before user can ever use them (quick settings services, module-level imports, global config/thread pool side effects).

If you want, I can implement the top 2 with lowest risk first:
1. quick settings deferred service init
2. dock deferred AppLauncher import
