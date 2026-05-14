
4. Medium: popover lifecycle cleanup appears incomplete; pooling path is unused
- Evidence: popover manager defines window pool return API, but no caller exists: popover.py.
- Popover creation always grabs window and attaches content: popover.py, popover.py, popover.py.
- Hide only hides/marks inactive, does not return window to pool or clear content bindings: popover.py, popover.py.
- Impact: long-lived hidden windows/content and handlers can persist longer than intended, especially across widget churn.

6. Medium: network service has avoidable runtime overhead and callback bug
- Evidence: debug print on every speed notify: network.py.
- Evidence: lambda closes over loop variable names in notifier wiring: network.py, network.py. This likely reports only the last property name, causing noisy/incorrect update behavior.
- Impact: unnecessary stdout churn and potentially wrong notification fanout.


Assumptions and gaps
- This is static code audit, not runtime profile. I have not run heap snapshots, perf tracing, or long-session soak tests.
- Highest-confidence issues are the stats listener accumulation risk, GPU subprocess frequency, and dock full-snapshot sync frequency.
