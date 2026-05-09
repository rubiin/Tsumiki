# CLAUDE.md

Project: Tsumiki
Repo root: /home/devina/.config/tsumiki

## What this repo is
- Tsumiki is a modular status bar / panel for Hyprland.
- Main code is Python, with UI widgets under `modules/`, `widgets/`, `shared/`, `services/`, and helpers in `utils/`.
- Styles live in `styles/`. Docs and site assets live in `docs/`.

## Editing rules
- Prefer small, focused changes.
- Do not revert user changes unless explicitly asked.
- Keep style consistent with nearby code.
- Prefer refactors that reduce duplication and nested branching.
- When changing popup, dock, notification, OSD, or settings UI code, check for shared helpers first.
- Use ASCII unless existing file clearly uses Unicode.

## Useful commands
- Start app: `./init.sh -start`
- Setup deps: `./init.sh -setup`
- Install from bootstrap: `./install.sh`
- Generate docs: `python doc_gen.py`
- Freeze deps: `pip freeze > requirements.txt`
- Generate stubs: `fabric-cli gs Glace-0.1 GtkLayerShell-0.1 Playerctl-2.0 NM-1.0`

## Practical notes
- `pyproject.toml` targets Python 3.12 style checks.
- Ruff is enabled; keep imports clean and avoid obvious lint noise.
- Popup-related logic is centralized in `shared/popup.py`.
- Lazy widget loading happens in `modules/bar.py`.
- Settings UI is large and repetitive; prefer generic builders over copy-paste.

## When fixing bugs
- Validate the touched file with existing error checks if available.
- If a change affects shared state, check call sites before editing.
- If a refactor touches UI lifecycle code, watch for stale handlers, duplicate timers, and destroy/cleanup paths.
