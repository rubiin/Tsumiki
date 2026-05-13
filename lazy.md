
1. High: signal/listener leak risk on bar hotplug recreation
- Evidence: stats widgets register global fabricator listeners in multiple constructors, but there is no disconnect path when bars/widgets are destroyed: stats.py, stats.py, stats.py, stats.py, stats.py.
- Hotplug recreates bars/widgets repeatedly: bar.py, bar.py.
- Root cause: global poll stream keeps running forever (widget_utils.py, widget_utils.py, widget_utils.py); callbacks can accumulate across recreate cycles and increase CPU/work each tick.
- Impact: memory growth (retained widget callbacks), duplicate UI updates, rising CPU over time.

2. High: expensive subprocess storm in GPU widget
- Evidence: each fabricator changed event triggers nvtop subprocess spawn: stats.py, stats.py.
- Poll cadence is ~1s from shared stats stream: widget_utils.py.
- Impact: continuous process creation, possible overlap if nvtop call latency exceeds interval, elevated CPU and scheduler overhead.

3. High: dock does full Hyprland snapshot/reconcile on very chatty events
- Evidence: all these events trigger full sync: dock.py, dock.py, dock.py, dock.py, dock.py, dock.py.
- Full sync path does j/activewindow + j/clients JSON roundtrips and rebuild/restyle work: dock.py, dock.py, dock.py, dock.py, dock.py.
- Additional cost from repeated icon pixbuf resolution during refresh/update: dock.py, dock.py.
- Impact: noticeable UI jank under frequent title/activity changes, unnecessary CPU and IPC load.

4. Medium: popover lifecycle cleanup appears incomplete; pooling path is unused
- Evidence: popover manager defines window pool return API, but no caller exists: popover.py.
- Popover creation always grabs window and attaches content: popover.py, popover.py, popover.py.
- Hide only hides/marks inactive, does not return window to pool or clear content bindings: popover.py, popover.py.
- Impact: long-lived hidden windows/content and handlers can persist longer than intended, especially across widget churn.

5. Medium: clipboard cleanup relies on destructor, which is unreliable for GTK/GObject lifetimes
- Evidence: temp dir and cache cleanup in destructor only: cliphist.py, cliphist.py, cliphist.py, temp dir created at cliphist.py.
- Impact: temp directories/resources may remain until process exit or never be reclaimed promptly.

6. Medium: network service has avoidable runtime overhead and callback bug
- Evidence: debug print on every speed notify: network.py.
- Evidence: lambda closes over loop variable names in notifier wiring: network.py, network.py. This likely reports only the last property name, causing noisy/incorrect update behavior.
- Impact: unnecessary stdout churn and potentially wrong notification fanout.

7. Low: bar auto-hide timer has no explicit destroy-time cancel path
- Evidence: timer set/cancel helpers exist (bar.py, bar.py), but no destroy override guaranteeing cleanup before bar.py destroy path.
- Impact: usually short-lived, but can leave pending callbacks during teardown/recreate windows.

Assumptions and gaps
- This is static code audit, not runtime profile. I have not run heap snapshots, perf tracing, or long-session soak tests.
- Highest-confidence issues are the stats listener accumulation risk, GPU subprocess frequency, and dock full-snapshot sync frequency.

