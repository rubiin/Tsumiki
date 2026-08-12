"""Plugin system for the app launcher slash commands.

Plugins are plain Python files (or packages) placed inside the launcher's
plugins directory — by default ``<tsumiki-config>/plugins`` (overridable via
``modules.app_launcher.plugins_dir``). Each plugin subclasses
:class:`LauncherPlugin` and is registered under its ``name`` (used as the
slash command, e.g. ``/calc``) together with any aliases.

Example::

    # ~/.config/tsumiki/plugins/hello.py
    from utils.plugin_manager import LauncherPlugin, PluginResult, copy_to_clipboard

    class HelloPlugin(LauncherPlugin):
        name = "hello"
        description = "Say hello to someone"
        icon = "face-smile-symbolic"

        def handle(self, args: str) -> list[PluginResult]:
            who = args.strip() or "world"
            return [PluginResult(f"Hello, {who}!", subtitle="Press Enter to copy")]

        def execute(self, result: PluginResult | None = None) -> bool:
            if result:
                copy_to_clipboard(result.title)
            return False  # close the launcher after executing

Notes for plugin authors:

* ``handle()`` runs on a worker thread — keep it free of any GTK calls and
  make it safe for network/CPU work.
* ``execute()`` runs on the main thread when the user selects a result.
* For multi-file plugins, use a package (a directory with ``__init__.py``)
  and re-export your plugin class from ``__init__.py``. Use relative imports
  (``from .helpers import ...``) inside the package.
"""

from __future__ import annotations

import importlib.util
import inspect
import os
import sys
from typing import Any, ClassVar

from fabric.utils import Gio, logger

from utils.functions import find_executable

# Module-name prefix used when importing plugin files so that a plugin file
# can never shadow a stdlib or third-party module.
_PLUGIN_MODULE_PREFIX = "tsumiki_plugin_"


class PluginResult:
    """A single selectable row rendered in the launcher for a slash command."""

    __slots__ = ("data", "icon", "subtitle", "title")

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        icon: str | None = None,
        data: Any = None,
    ):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.data = data

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<PluginResult title={self.title!r}>"


class LauncherPlugin:
    """Base class for launcher slash-command plugins.

    Subclasses must set at least ``name`` and ``description`` and should
    override :meth:`handle` (and usually :meth:`execute`).
    """

    name: str = ""
    description: str = ""
    #: GTK icon name (e.g. ``"accessories-calculator-symbolic"``) or a Nerd
    #: Font glyph string. Falls back to the launcher default when unset.
    icon: str | None = None
    #: Extra slash-command names that trigger this plugin.
    aliases: ClassVar[list[str]] = []
    #: Optional per-plugin debounce (ms) before ``handle()`` is dispatched
    #: while typing. ``None`` or ``0`` falls back to the launcher's default
    #: debounce. Set a larger value for expensive plugins (e.g. those that
    #: spawn a subprocess like /calc) to avoid one query per keystroke.
    debounce_ms: int | None = None
    #: When True, the launcher stays open after ``execute()`` (useful for
    #: converters that want to keep showing results). ``execute()`` may also
    #: return True to keep the launcher open.
    keep_open: bool = False

    def handle(self, args: str) -> list[PluginResult]:
        """Return the result rows for the given argument string.

        Runs on a worker thread — no GTK calls allowed here.
        """
        return []

    def execute(self, result: PluginResult | None = None) -> bool:
        """Run when the user activates *result* (or the bare command).

        Return True to keep the launcher open.
        """
        return False

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<{type(self).__name__} name={self.name!r}>"


def copy_to_clipboard(text: str) -> bool:
    """Copy *text* to the system clipboard (wl-copy, falling back to xclip)."""
    text = text or ""
    try:
        if find_executable("wl-copy"):
            proc = Gio.SubprocessLauncher.new(Gio.SubprocessFlags.STDIN_PIPE).spawnv(
                ["wl-copy", "--type", "text/plain"]
            )
            proc.communicate_utf8(text, None)
            return True
        if find_executable("xclip"):
            proc = Gio.SubprocessLauncher.new(Gio.SubprocessFlags.STDIN_PIPE).spawnv(
                ["xclip", "-selection", "clipboard"]
            )
            proc.communicate_utf8(text, None)
            return True
        logger.warning("[LauncherPlugin] No clipboard tool (wl-copy/xclip) found")
    except Exception as exc:
        logger.exception(f"[LauncherPlugin] Failed to copy to clipboard: {exc}")
    return False


class PluginManager:
    """Loads launcher plugins from a directory and registers their commands."""

    def __init__(self, plugins_dir: str):
        self.plugins_dir = os.path.expanduser(plugins_dir)
        self._plugins: dict[str, LauncherPlugin] = {}
        self._instances: list[LauncherPlugin] = []

    # -- discovery ----------------------------------------------------

    def load(self) -> int:
        """Discover and load plugins from the configured directory.

        Returns the number of successfully registered plugin commands.
        Broken or unrelated files are skipped with a warning.
        """
        self._plugins.clear()
        self._instances.clear()

        if not os.path.isdir(self.plugins_dir):
            logger.info(
                f"[LauncherPlugin] Plugins directory "
                f"'{self.plugins_dir}' not found, no slash commands loaded"
            )
            return 0

        count = 0
        for path in sorted(os.listdir(self.plugins_dir)):
            full_path = os.path.join(self.plugins_dir, path)
            module_name: str | None = None
            try:
                if path.endswith(".py") and not path.startswith("_"):
                    module_name = self._import_file(full_path)
                elif os.path.isdir(full_path) and os.path.exists(
                    os.path.join(full_path, "__init__.py")
                ):
                    module_name = self._import_package(full_path, path)
                else:
                    continue
            except Exception as exc:
                logger.exception(
                    f"[LauncherPlugin] Failed to load plugin '{path}': {exc}"
                )
                continue

            if module_name:
                count += self._register_from_module(module_name, path)

        logger.info(
            f"[LauncherPlugin] Loaded {count} slash command(s) from {self.plugins_dir}"
        )
        return count

    def _import_file(self, path: str) -> str | None:
        """Import a single-file plugin under a unique synthetic module name."""
        stem = os.path.splitext(os.path.basename(path))[0]
        module_name = f"{_PLUGIN_MODULE_PREFIX}{stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module_name

    def _import_package(self, path: str, dirname: str) -> str | None:
        """Import a package plugin (dir with __init__.py) with relative imports."""
        module_name = f"{_PLUGIN_MODULE_PREFIX}{dirname}"
        init_path = os.path.join(path, "__init__.py")
        spec = importlib.util.spec_from_file_location(module_name, init_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module_name

    # -- registration -------------------------------------------------

    def _register_from_module(self, module_name: str, source: str) -> int:
        """Register every LauncherPlugin subclass exposed by the module."""
        module = sys.modules.get(module_name)
        if module is None:
            return 0
        count = 0
        for attr in vars(module).values():
            if (
                inspect.isclass(attr)
                and issubclass(attr, LauncherPlugin)
                and attr is not LauncherPlugin
                and not inspect.isabstract(attr)
                and self._register(attr, source)
            ):
                count += 1
        return count

    def _register(self, plugin_cls: type, source: str) -> bool:
        """Instantiate a plugin and register it under its name + aliases."""
        try:
            instance = plugin_cls()
        except Exception as exc:
            logger.exception(
                f"[LauncherPlugin] Failed to instantiate "
                f"{plugin_cls.__name__} from {source}: {exc}"
            )
            return False

        if not instance.name:
            logger.warning(
                f"[LauncherPlugin] Plugin {plugin_cls.__name__} in {source} "
                f"has no name — skipped"
            )
            return False

        keys = [instance.name.casefold()] + [
            alias.casefold() for alias in instance.aliases
        ]
        for key in keys:
            if key in self._plugins:
                logger.warning(
                    f"[LauncherPlugin] Duplicate slash command '/{key}' "
                    f"from {source} — keeping the first registration"
                )
                continue
            self._plugins[key] = instance
        self._instances.append(instance)
        return True

    # -- lookup -------------------------------------------------------

    def get(self, command: str) -> LauncherPlugin | None:
        """Return the plugin registered for *command* (case-insensitive)."""
        return self._plugins.get(command.casefold())

    def all(self) -> list[LauncherPlugin]:
        """Return all loaded plugins, sorted by command name."""
        return sorted(self._instances, key=lambda plugin: plugin.name)

    def match(self, prefix: str) -> list[LauncherPlugin]:
        """Return plugins whose command or alias starts with *prefix*."""
        prefix = prefix.casefold()
        matched: set[LauncherPlugin] = set()
        for key, plugin in self._plugins.items():
            if key.startswith(prefix):
                matched.add(plugin)
        return sorted(matched, key=lambda plugin: plugin.name)


_manager: PluginManager | None = None
_manager_dir: str = ""


def get_plugin_manager(plugins_dir: str) -> PluginManager:
    """Return a cached :class:`PluginManager`, reloading if the dir changed."""
    global _manager, _manager_dir
    plugins_dir = os.path.expanduser(plugins_dir)
    if _manager is None or _manager_dir != plugins_dir:
        _manager = PluginManager(plugins_dir)
        _manager.load()
        _manager_dir = plugins_dir
    return _manager
