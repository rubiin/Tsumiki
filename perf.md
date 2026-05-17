# Performance and Memory Hotspots

Scope: static code scan for memory hogs and perf bottlenecks.

## Highest impact



6. Global util fabricator runs infinite stats loop once created
- Evidence: `utils/widget_utils.py:28`, `utils/widget_utils.py:31`, `utils/widget_utils.py:44`, `utils/widget_utils.py:57`
- Why hot: `while True` with 1s cadence; includes `psutil.sensors_temperatures()` and disk polling. Fabricator is singleton/lazy but effectively permanent after first use.
- Risk: background CPU overhead even if stats widgets removed; extra sensor I/O.
- Fix direction: reference-count subscribers and stop poller at zero; split fast vs slow metrics (temps/disk less frequent).
