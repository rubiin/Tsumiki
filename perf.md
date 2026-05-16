# Performance and Memory Hotspots

Scope: static code scan for memory hogs and perf bottlenecks.

## Highest impact

1. Lockkeys OSD polls shell command every 200ms
- Evidence: `modules/osds/lockkeys.py:26`, `modules/osds/lockkeys.py:49`, `modules/osds/lockkeys.py:54`
- Why hot: spawns `hyprctl devices -j` 5x/sec forever. Process spawn + JSON parse churn on main loop.
- Risk: steady CPU burn, battery drain, jitter under load.
- Fix direction: event-driven lock-state updates if possible; else raise interval (>=1000ms), pause polling when OSD hidden.

2. Overview rebuilds entire UI on every window event
- Evidence: `modules/overview.py:215`, `modules/overview.py:216`, `modules/overview.py:217`, `modules/overview.py:263`, `modules/overview.py:270`
- Why hot: each open/close/move event triggers full `j/monitors` + `j/clients`, destroys/recreates all widgets.
- Risk: large spikes with many windows/events, GC pressure, frame drops.
- Fix direction: incremental diff update (add/remove/move only changed clients), debounce burst events.

3. Dock sync still does full Hyprland snapshots
- Evidence: `modules/dock.py:330`, `modules/dock.py:353`, `modules/dock.py:364`
- Why hot: `j/activewindow` + `j/clients` snapshot in sync path; expensive when event stream chatty.
- Risk: unnecessary CPU and allocations, especially with many clients.
- Fix direction: keep debounce, but fast-path active-window style updates without full `j/clients`; snapshot only on structural events.

4. GPU widget shells out to `nvtop` repeatedly
- Evidence: `widgets/stats.py:143`, `widgets/stats.py:159`
- Why hot: external process spawn/parsing every poll window (default 2.5s) is expensive.
- Risk: periodic CPU spikes; worse on low-power devices.
- Fix direction: reuse long-lived collector process or switch to lighter source (e.g. direct NVML bindings), increase default poll interval.

## Memory hog risks

5. DONE: Custom module/widget may deadlock or grow buffers on stderr
- Evidence: `widgets/custom_module.py:225`, `widgets/custom_module.py:226`, `widgets/custom_module.py:243`, `widgets/custom_widget.py:225`, `widgets/custom_widget.py:226`, `widgets/custom_widget.py:243`
- Why hot: both stdout and stderr are piped, but reader thread drains stdout only. If command writes enough stderr, child can block; buffered data can grow.
- Risk: stuck modules, memory growth, zombie-like behavior.
- Fix direction: DONE via stderr->stdout merge in continuous executors.

6. Global util fabricator runs infinite stats loop once created
- Evidence: `utils/widget_utils.py:28`, `utils/widget_utils.py:31`, `utils/widget_utils.py:44`, `utils/widget_utils.py:57`
- Why hot: `while True` with 1s cadence; includes `psutil.sensors_temperatures()` and disk polling. Fabricator is singleton/lazy but effectively permanent after first use.
- Risk: background CPU overhead even if stats widgets removed; extra sensor I/O.
- Fix direction: reference-count subscribers and stop poller at zero; split fast vs slow metrics (temps/disk less frequent).

7. DONE: Popover window pooling path not used on hide
- Evidence: `shared/popover.py:99`, `shared/popover.py:355`, `shared/popover.py:372`, `shared/popover.py:380`
- Why hot: manager has `return_popover_window`, but hide path calls only `.hide()`. Windows/content can stay resident longer than needed.
- Risk: retained hidden widgets/windows, memory creep across many popovers.
- Fix direction: DONE by releasing popover window to manager pool on hide/destroy and disconnecting per-window handlers.

## Medium impact / situational

8. Lottie loops can be expensive with many instances
- Evidence: `shared/lottie.py:95`, `shared/lottie.py:99`, `shared/lottie.py:120`
- Why hot: frame timer renders every frame; multiple looping widgets multiply cost.
- Risk: high CPU/GPU on animation-heavy setups.
- Fix direction: lower frame rate for small widgets, auto-pause when offscreen/hidden.

9. CSS live-reload recompiles on each file change
- Evidence: `main.py:18`, `main.py:139`, `main.py:140`
- Why hot: developer-time only, but can reprocess CSS frequently while editing.
- Risk: transient stutter in dev sessions.
- Fix direction: debounce file-change handlers.

## Quick wins first (best ROI)

1. Raise lockkeys poll interval + disable polling when hidden.
2. DONE: Fix stderr draining in custom module/widget executors.
3. DONE: Add incremental update path for overview (avoid full rebuild).
4. DONE: Split dock sync into lightweight active-window update vs full client refresh.
5. Make util fabricator lifecycle-aware (start/stop based on subscribers).
