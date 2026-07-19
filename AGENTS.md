# Claude Configuration for Tsumiki

## What this repo is

Tsumiki is a modular status bar / panel for Hyprland written using [Fabric](https://github.com/Fabric-Development/fabric) (Python GTK3 widget framework). Main code is Python, with UI widgets under `modules/`, `widgets/`, `shared/`, `services/`, and helpers in `utils/`. Styles live in `styles/`. Docs and site assets live in `docs/`

## Project Structure

- **modules/** — Core UI modules (dock, overview, notification, settings, etc.)
- **services/** — Background services (battery, weather, network, brightness, etc.)
- **widgets/** — Individual widget implementations
- **shared/** — Reusable UI components and mixins
- **styles/** — SCSS stylesheets and theming
- **utils/** — Utility functions, config management, helpers
- **docs/** — Astro-based documentation site
- **tests/** — Test suite
- **assets/** — Static assets (icons, images, i18n, emoji, etc.)

## Key Files

- `main.py` — Entry point
- `pyproject.toml` — Python project metadata
- `config.toml` — Configuration examples
- `tsumiki.schema.json` — Configuration schema
- `Justfile` — Task recipes

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

## Working with This Codebase

### Before Starting

- Read `README.md` for setup instructions
- Check `CONTRIBUTING.md` for guidelines
- Review `doc.md` for architecture notes
- Run `init.sh` to set up environment

### Running Tasks

Use `Justfile` recipes:
```bash
just --list  # Show available tasks
```

### Testing

Tests are in `tests/` directory:
```bash
python -m pytest tests/
```

### Documentation

Docs are in `docs/` (Astro + pnpm). Build with:
```bash
cd docs && pnpm install && pnpm build
```

## Communication Preferences

- **Be concise** — Respect token budgets; prioritize clarity over elaboration
- **Focus on facts** — Ground answers in code inspection, not assumptions
- **Concrete examples** — Show code snippets rather than descriptions
- **Progressive disclosure** — Start simple, add detail only if needed
- **Challenge assumptions** — Point out issues in plans or designs plainly

## When Reviewing Code

Check against:
1. **Does it follow project conventions?** (structure, naming, patterns)
2. **Does it integrate cleanly?** (minimal coupling, proper separation)
3. **Is it maintainable?** (readable, documented, testable)
4. **Config schema alignment** — Does it respect `tsumiki.schema.json`?

## Tools & Workflows

- Use `pylance` for Python analysis
- Use branch/commit tools for git workflows
- Use `review` skill for PR reviews
- Use `diagnose` skill for bug investigations
- Use `tdd` skill for feature development

## Common Tasks

| Task | Approach |
|------|----------|
| Add new widget | Copy template from `widgets/`, implement in module |
| Add new service | Create in `services/`, register in main |
| Add config option | Update schema, add to `utils/config.py`, update docs |
| Style changes | Edit relevant SCSS, test theme variants |
| Fix UI bug | Check widget state, animator, signal handling |

## Adding a New Widget (Panel-based, toggleable)

Widgets go in `widgets/` and are typically panel buttons that can open popovers or display quick info.

### Step 1: Create Widget File
Create `widgets/my_widget.py`:
```python
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon

class MyWidgetMenu(Box):
    """Popover content."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(
            name="my-widget-menu",
            orientation="v",
            spacing=8,
            **kwargs,
        )
        self._parent = parent
        self.children = [Label(label="Menu content")]

    def close(self, *_):
        if self._parent:
            self._parent.hide_popover()

class MyWidget(ButtonWidget, PopoverMixin):
    """Panel widget."""
    def __init__(self, **kwargs):
        super().__init__(name="my_widget", **kwargs)

        self.container_box.add(
            nerd_font_icon(
                icon=self.config.get("icon", "📦"),
                props={"style_classes": ["panel-font-icon"]},
            )
        )

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            self.set_tooltip_text("My Widget")

        self.setup_popover(lambda: MyWidgetMenu(parent=self))
```

### Step 2: Add to Bar Layout
In `config.toml`, add widget to layout:
```toml
[layout]
bar = [
    # ... existing widgets ...
    "my_widget",
]

[widgets.my_widget]
enabled = true
icon = "📦"
tooltip = true
```

### Step 3: Add Config Schema
In `tsumiki.schema.json`, add to `widgets` properties:
```json
"my_widget": {
  "type": "object",
  "properties": {
    "enabled": {"type": "boolean", "default": true},
    "icon": {"type": "string", "default": "📦"},
    "tooltip": {"type": "boolean", "default": true}
  }
}
```

### Step 4: Add Styling
Create `styles/_my_widget.scss`:
```scss
#my-widget-menu {
  padding: 12px;
}

#my-widget-menu-label {
  color: #ffffff;
  font-size: 12px;
}
```

Import in `styles/main.scss`:
```scss
@use "my_widget.scss";
```

### Step 5: GTK3 CSS Best Practices
- **Use**: Only styles that are supported by GTK3 CSS (https://docs.gtk.org/gtk3/css-properties.html)
- **Avoid**: `text-align`, `align-items`, `justify-content`, `margin: auto`, `transition`
- For centering labels: use `h_align="center"` in Python
- For centering boxes: use `h_align="center"` in Python property

---

## Adding a New Module (Standalone overlay/popup)

Modules are top-level windows (overlays, popups, full panels). Common examples: notification, overview, dock, desktop_clock.

### Step 1: Create Service (if needed)
If module manages state, create `services/my_module.py`:
```python
from fabric.core.service import Signal
from fabric.utils import GLib, logger

from services.base import SingletonService

class MyModuleService(SingletonService):
    @Signal
    def updated(self) -> None:
        """Signal emitted on state change."""

    def __init__(self):
        super().__init__()
        self.state = "idle"

    def do_something(self):
        self.state = "active"
        self.emit("updated")
        logger.info("[MyModule] State updated")

my_module_service = MyModuleService()
```

### Step 2: Create Module Widget
Create `widgets/my_module.py` (or `modules/my_module.py` if very complex):
```python
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from services.my_module import my_module_service
from utils.widget_utils import nerd_font_icon

class MyModulePopover(Box):
    """Popover content for module."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(
            name="my-module-popover",
            orientation="v",
            spacing=12,
            **kwargs,
        )
        self._parent = parent
        self.service = my_module_service

        self.title = Label(
            name="my-module-title",
            markup="<span font='14' color='#ffffff'>My Module</span>",
        )

        self.children = [self.title]
        self.service.connect("updated", self._on_update)

    def _on_update(self, *_):
        pass

    def close(self, *_):
        if self._parent:
            self._parent.hide_popover()

class MyModuleWidget(ButtonWidget, PopoverMixin):
    """Panel button for module."""
    def __init__(self, **kwargs):
        super().__init__(name="my_module", **kwargs)

        self.container_box.add(
            nerd_font_icon(
                icon=self.config.get("icon", "🎯"),
                props={"style_classes": ["panel-font-icon"]},
            )
        )

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            self.set_tooltip_text("My Module")

        self.setup_popover(lambda: MyModulePopover(parent=self))
```

### Step 3: Register in Main
In `main.py`, add initialization:
```python
# After other modules
if module_options.get("my_module", {}).get("enabled", False):
    from widgets.my_module import MyModuleWidget
    # If it's a panel widget, it's auto-loaded via layout
    # If it's a standalone overlay, add window:
    # app.add_window(MyModuleWindow(widget_config))
```

### Step 4: Add Config Schema
In `tsumiki.schema.json`, add to `modules` properties:
```json
"my_module": {
  "type": "object",
  "properties": {
    "enabled": {"type": "boolean", "default": false},
    "anchor": {
      "type": "string",
      "enum": ["center", "top-right", "bottom-left", ...],
      "default": "center"
    },
    "layer": {
      "type": "string",
      "enum": ["top", "overlay", "bottom", "background"],
      "default": "overlay"
    }
  }
}
```

### Step 5: Add Config Entry
In `config.toml`:
```toml
[modules.my_module]
enabled = false
anchor = "center"
layer = "overlay"
```


### Step 6: Add Styling
Create `styles/_my_module.scss`. Always use nesting to avoid global selectors:
```scss
#my-module {
  background-color: rgba(40, 40, 50, 0.95);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(200, 200, 220, 0.2);
}

#my-module-popover {
  padding: 12px;
}

#my-module-title {
  color: #ffffff;
  font-size: 14px;
}
```

Import in `styles/main.scss`:
```scss
@use "my_module.scss";
```

### Step 7: Testing
```bash
python3 -c "from services.my_module import my_module_service; print('✓ Service OK')"
python3 -c "from widgets.my_module import MyModuleWidget; print('✓ Widget OK')"
```

---

## Special Notes

- Configuration is hot-reloadable via `utils/config_watcher.py`
- Themes are generated dynamically (see `services/matugen.py`)
- DBus is used for system integration (`utils/dbus_helper.py`)
- Internationalization via JSON files in `assets/i18n/`

## When fixing bugs

- Validate the touched file with existing error checks if available.
- If a change affects shared state, check call sites before editing.
- If a refactor touches UI lifecycle code, watch for stale handlers, duplicate timers, and destroy/cleanup paths.

## Questions to Ask Before Starting

- Is this a feature, bugfix, or refactor?
- Does it affect the public config schema?
- Does it require new tests?
- Is documentation needed (README, docs site, or schema)?


## gi.repository type stubs

`gi.repository` imports lack type checking by default. Stubs are generated via `gengir`. The Fabric wiki has more detail: https://fabric-development.github.io/fabric-wiki/installing-stubs.html

## GTK Best Practices

- Keep UI updates on main thread only; push heavy work to background and return via GLib idle/timeout callbacks.
- Prefer signal-driven updates over polling; if polling is required, store timer IDs and stop them on destroy/unmap.
- Avoid duplicate signal connections; guard repeated setup paths and lifecycle re-entry.
- Always clean up on destroy: signal handlers, timers, async callbacks, subprocess readers.
- Use fallback labels/icons for missing services or unavailable devices.
- Avoid rebuilding full widget trees for small state changes; update existing widgets in place.
- Keep widget hierarchy shallow and avoid expensive style churn in hot paths.
- Keep service state logic separate from rendering logic for easier testing and safer refactors.
- Debounce noisy event streams to limit redundant relayout/repaint work.
- Never block GTK callbacks with synchronous shell/process operations.
