# Simplification Hotspots

Generated: 2026-05-09

1. modules/dock.py:567
- `_create_app_group` mixes UI creation, menu logic, click behavior, and drag/drop wiring.
- Simplify by splitting into: `build_group_ui`, `wire_group_events`, `wire_group_dnd`.

2. modules/dock.py:323
- `_sync_clients` combines data fetch, normalization, reconciliation, and visibility updates.
- Simplify by separating state snapshot from render reconciliation.

3. modules/dock.py:778
- `_sync_ungrouped_clients` does multi-pass mutation and styling in one method.
- Simplify by diffing first, then apply remove/add/update phases.

4. modules/dock.py:448
- Menu construction pattern repeated for single/group contexts.
- Simplify using declarative menu spec + one menu renderer.

5. modules/notification.py:102
- `NotificationWidget.__init__` handles layout, state, gestures, timeout, and actions.
- Simplify by extracting `_build_header`, `_build_body`, `_build_actions`, `_wire_events`.

6. modules/notification.py:368
- Swipe gesture handler mixes gesture state with rendering side effects.
- Simplify with explicit swipe state model and dedicated render/reset methods.

7. modules/notification.py:478
- Timeout progress animation loop is separate from close timeout lifecycle.
- Simplify into one timer source of truth for progress + close.

8. modules/settings_gui.py:441
- Theme/config UI generation has repetitive recursion and control creation branches.
- Simplify with schema-driven form renderer (type -> control factory).

9. modules/settings_gui.py:264
- Nested section creation duplicated across general/theme paths.
- Simplify with one recursive section builder + pluggable update callback.

10. shared/popup.py:77
- `make_layout` has repeated anchor/padding patterns.
- Simplify with anchor map + reusable composition helpers.

11. modules/osd.py:113
12. modules/osd.py:187
- `AudioOSDContainer` and `MicrophoneOSDContainer` duplicate most flow.
- Simplify with shared base/mixin and source-specific adapters.

13. modules/overview.py:23
14. modules/overview.py:125
- Icon resolution/fallback/scaling duplicated in constructor and `update_image`.
- Simplify with single `resolve_icon_pixbuf(app_id, size, desktop_app)` helper.

15. shared/popover.py:240
- `_create_popover` combines content creation, signal wiring, manager activation, and positioning.
- Simplify by splitting lifecycle steps and moving handler wiring to dedicated method.

16. widgets/custom_module.py:164
- Continuous process lifecycle, JSON formatting, event handlers, and signal cleanup in one class.
- Simplify into executor (process/signal) + presenter (format/render).

17. modules/app_launcher.py:274
- `arrange_viewport` mixes filtering, handler cleanup, lazy rendering, and resize logic.
- Simplify into pipeline: filter -> clear -> schedule render.

18. utils/functions.py
- Utility module carries unrelated domains (I/O, backend detection, color, cache, theme copy).
- Simplify by splitting into focused utility modules.
