import json
import threading

from fabric import Application
from fabric.core.service import Signal
from fabric.utils import (
    exec_shell_command,
    get_relative_path,
    idle_add,
    logger,
    os,
)

from utils.colors import Colors
from utils.config import tsumiki_config
from utils.constants import CSS_PATH
from utils.decorators import run_in_thread
from utils.functions import (
    check_executable_exists,
    exclude_keys,
    flatten_dict,
    read_toml_file,
    update_theme_config,
)

from .base import SingletonService

# Bounded memoization cache for raw TOML theme data keyed by theme name.
# Theme TOML files are static assets and never change at runtime, so once
# parsed the result is cached forever (within process lifetime).
_MAX_CACHED_THEMES = 64
_theme_file_cache: dict[str, dict] = {}


class StyleService(SingletonService):
    """Centralized service for style/theme management.

    Handles:
    - Loading and listing available themes
    - Applying themes (from TOML files or Matugen)
    - Recompiling and applying CSS
    - Cycling through themes
    - Emitting signals on theme changes

    Signals
    -------
    theme_changed (theme_name: str)
        Emitted when a theme is successfully applied.
    css_recompiled
        Emitted when CSS is recompiled and applied.
    """

    @Signal
    def theme_changed(self, theme_name: str) -> None:
        """Signal emitted after a new theme is applied."""

    @Signal
    def css_recompiled(self) -> None:
        """Signal emitted when CSS has been recompiled and applied."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._themes_dir = get_relative_path("../themes")
        self._styles_dir = get_relative_path("../styles")

        self._compile_lock = threading.Lock()
        self._compiling = False

        check_executable_exists("sass")

        self._config = tsumiki_config
        self._styling_config = self._config.get("styling", {})

        self._current_theme: str = self._styling_config.get(
            "theme_name", "catpuccin-mocha"
        )
        self._mode: str = self._styling_config.get("mode", "dark")

        # Cache of available themes (name -> path)
        self._available_themes: list[str] = []
        self._refresh_available_themes()

        # Parsed contents of the currently active theme (the selected mode's section)
        self._theme_contents: dict | None = None

        logger.info(
            f"{Colors.INFO}[StyleService] Initialized with theme="
            f"'{self._current_theme}', mode='{self._mode}'"
        )

    # ── Public properties ──────────────────────────────────────

    @property
    def current_theme(self) -> str:
        """Name of the currently active theme."""
        return self._current_theme

    @property
    def mode(self) -> str:
        """Current color mode ('dark' or 'light')."""
        return self._mode

    @property
    def available_themes(self) -> list[str]:
        """List of available theme names from the themes directory."""
        return list(self._available_themes)

    @property
    def theme_contents(self) -> dict | None:
        """Parsed contents of the currently active theme (the selected mode's section).

        Returns a dictionary with keys like ``background``, ``text``,
        ``surface``, ``accent``, ``general`` --- or ``None`` if no
        theme has been loaded yet.
        """
        return self._theme_contents

    # ── Public API ─────────────────────────────────────────────

    def apply_theme_from_config(self) -> None:
        """Load and apply the theme as configured in ``config.toml``.

        This is the main entry point used at startup. If Matugen is
        enabled it runs that first; otherwise it copies the named theme
        TOML file to ``_theme.scss`` and recompiles CSS.
        """
        matugen_config = self._styling_config.get("matugen", {})

        if matugen_config.get("enabled", False):
            self._apply_matugen()
        else:
            self._copy_and_apply(self._current_theme, self._mode)

    def apply_theme(self, theme_name: str) -> None:
        """Switch to a different theme by name.

        Parameters
        ----------
        theme_name : str
            Name of the theme (without ``.toml`` suffix).
        """
        if theme_name not in self._available_themes:
            logger.warning(
                f"{Colors.WARNING}[StyleService] Theme '{theme_name}' not found, "
                f"falling back to '{self._available_themes[0]}'"
            )
            theme_name = (
                self._available_themes[0]
                if self._available_themes
                else "catpuccin-mocha"
            )

        self._current_theme = theme_name
        self._copy_and_apply(theme_name, self._mode)

        # Persist the choice to config.toml
        update_theme_config(theme_name)

        self.emit("theme_changed", theme_name)
        logger.info(f"{Colors.INFO}[StyleService] Applied theme '{theme_name}'")

    def next_theme(self) -> str:
        """Cycle to the next theme in the alphabetical list.

        Returns
        -------
        str
            The new theme name.
        """
        if not self._available_themes:
            return self._current_theme

        try:
            idx = self._available_themes.index(self._current_theme)
        except ValueError:
            idx = -1

        next_idx = (idx + 1) % len(self._available_themes)
        next_name = self._available_themes[next_idx]
        self.apply_theme(next_name)
        return next_name

    def previous_theme(self) -> str:
        """Cycle to the previous theme in the alphabetical list.

        Returns
        -------
        str
            The new theme name.
        """
        if not self._available_themes:
            return self._current_theme

        try:
            idx = self._available_themes.index(self._current_theme)
        except ValueError:
            idx = 0

        prev_idx = (idx - 1) % len(self._available_themes)
        prev_name = self._available_themes[prev_idx]
        self.apply_theme(prev_name)
        return prev_name

    def set_mode(self, mode: str) -> None:
        """Set the color mode and re-apply the current theme.

        Parameters
        ----------
        mode : str
            Either ``'dark'`` or ``'light'``.
        """
        if mode not in ("dark", "light"):
            logger.warning(
                f"{Colors.WARNING}[StyleService] Invalid mode '{mode}', "
                f"must be 'dark' or 'light'"
            )
            return

        self._mode = mode
        self.apply_theme(self._current_theme)

    def refresh(self) -> None:
        """Recompile and re-apply the current CSS without changing the theme."""
        self._compile_css()
        self.emit("css_recompiled")

    # ── Internal helpers ───────────────────────────────────────

    def _refresh_available_themes(self) -> None:
        """Scan the themes directory for available ``.toml`` files."""
        try:
            if not os.path.isdir(self._themes_dir):
                logger.warning(
                    f"{Colors.WARNING}[StyleService] Themes directory "
                    f"'{self._themes_dir}' not found"
                )
                self._available_themes = []
                return

            theme_files = sorted(
                f.replace(".toml", "")
                for f in os.listdir(self._themes_dir)
                if f.endswith(".toml")
            )
            self._available_themes = theme_files
        except OSError as exc:
            logger.error(f"{Colors.ERROR}[StyleService] Failed to list themes: {exc}")
            self._available_themes = []

    def _copy_and_apply(self, theme_name: str, mode: str) -> None:
        """Copy a TOML theme file to ``_theme.scss``.

        Loads theme contents into memory and writes SCSS variables
        synchronously. CSS compilation is a separate step (``refresh()``).
        """
        self._load_theme_contents(theme_name, mode)
        self._write_theme_variables(theme_name, mode)

    def _get_raw_theme(self, theme_name: str) -> dict | None:
        """Return the full parsed TOML for *theme_name*, memoized."""
        if theme_name in _theme_file_cache:
            return _theme_file_cache[theme_name]

        source_file = f"{self._themes_dir}/{theme_name}.toml"
        if not os.path.exists(source_file):
            logger.warning(
                f"{Colors.WARNING}[StyleService] Theme file "
                f"'{theme_name}.toml' not found"
            )
            return None

        contents = read_toml_file(source_file)
        if contents is not None and len(_theme_file_cache) < _MAX_CACHED_THEMES:
            _theme_file_cache[theme_name] = contents
        return contents

    def _load_theme_contents(self, theme_name: str, mode: str) -> None:
        """Parse the theme TOML and cache the active mode's section.

        Sets ``self._theme_contents`` to the resolved dict (or ``None``
        if the file can't be read).
        """
        contents = self._get_raw_theme(theme_name)
        if contents is None:
            # Fall back to default
            contents = self._get_raw_theme("catpuccin-mocha")

        self._theme_contents = contents.get(mode, contents) if contents else None

    def _write_theme_variables(self, theme: str, mode: str = "dark"):
        """Write flattened theme color values into ``_theme.scss``.

        This writes the SCSS variables file only — it does **not** invoke
        ``sass``. Actual CSS compilation is handled separately by
        ``refresh()`` (for explicit refresh) or by the
        optional file watcher in ``main.py``.
        """
        destination_file = f"{self._styles_dir}/_theme.scss"

        contents = self._get_raw_theme(theme)
        if contents is None:
            logger.warning(
                f"{Colors.WARNING}[StyleService] Theme file "
                f"'{theme}.toml' not found, falling back to default"
            )
            contents = self._get_raw_theme("catpuccin-mocha")

        if contents is None:
            logger.exception(f"{Colors.ERROR}Error: Could not read any theme file.")
            exit(1)

        selected_theme = contents.get(mode, contents)
        self.write_css_settings(flatten_dict(selected_theme), destination_file)

    def write_css_settings(self, contents, file):
        """Generate SCSS settings file from theme config."""
        logger.info("[CONFIG] Applying css settings...")

        css_styles = contents

        # Use list comprehension and join for faster string building
        lines = [
            f"${setting}: {json.dumps(value) if isinstance(value, bool) else value};"
            for setting, value in css_styles.items()
        ]

        with open(file, "w") as f:
            f.write("\n".join(lines))
            f.write("\n")

    def _apply_matugen(self) -> None:
        """Generate colors via Matugen and apply them."""
        try:
            from services import matugen_service

            # Run synchronously at startup
            matugen_service.generate_sync()
            # Matugen themes don't have a parsable TOML contents cache
            self._theme_contents = None
            self.emit("theme_changed", "matugen")
        except Exception as exc:
            logger.exception(
                f"{Colors.ERROR}[StyleService] Matugen generation failed: {exc}"
            )

    # ── CSS compilation (moved from utils/functions.py) ─────────

    @staticmethod
    def _apply_css_to_app(file):
        """Load the compiled CSS file into the running application."""
        try:
            app = Application.get_default()
            if app:
                app.set_stylesheet_from_file(file)
                logger.info(f"{Colors.INFO}[Theme] CSS applied to application")
        except Exception as e:
            logger.exception(f"{Colors.ERROR}[Theme] Error applying CSS to app: {e}")

    @run_in_thread
    def _compile_css(self):
        """Run ``sass`` to compile SCSS into CSS.

        Uses a ``_compiling`` flag + lock to skip concurrent compilations
        — if sass is already running, subsequent calls return early.
        Errors are printed to stderr and logged.
        """
        with self._compile_lock:
            if self._compiling:
                logger.info(f"{Colors.INFO}[Theme] CSS compilation already in progress")
                return
            self._compiling = True

        try:
            logger.info(f"{Colors.INFO}[Theme] Recompiling CSS")
            output = exec_shell_command(
                f"sass styles/main.scss {CSS_PATH} --no-source-map"
            )

            print(f"{Colors.INFO}[Theme] CSS compilation output:\n{output}")

            if output == "":
                logger.info(f"{Colors.INFO}[Main] CSS applied")
                idle_add(lambda: self._apply_css_to_app(get_relative_path(CSS_PATH)))
            else:
                logger.exception(f"{Colors.ERROR}[Main]Failed to compile sass!")
                logger.exception(f"{Colors.ERROR}[Main] {output}")

                idle_add(lambda: self._apply_css_to_app(""))

        except Exception as e:
            logger.exception(f"{Colors.ERROR}[Theme] Error recompiling CSS: {e}")
        finally:
            with self._compile_lock:
                self._compiling = False

    def write_settings_css(self):
        self.write_css_settings(
            flatten_dict(exclude_keys(self._config.get("styling", {}), ["matugen"])),
            f"{self._styles_dir}/_settings.scss",
        )


# Module-level singleton instance
style_service = StyleService()
