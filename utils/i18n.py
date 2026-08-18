"""Internationalization (i18n) support for Tsumiki."""

import json
import os

from fabric.utils import logger

# Default language
DEFAULT_LANGUAGE = "en"

# Singleton instance
_instance = None


class I18n:
    """Internationalization manager that loads and provides translations."""

    _instance = None
    __slots__ = ("_fallback", "_initialized", "_language", "_translations")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._translations: dict[str, str] = {}
        self._language: str = DEFAULT_LANGUAGE
        self._fallback: dict[str, str] = {}
        self._initialized = True

    def load(self, language: str) -> None:
        """Load translations for the specified language."""
        self._language = language

        # Always load English as fallback
        if language != DEFAULT_LANGUAGE:
            self._fallback = self._load_language_file(DEFAULT_LANGUAGE)

        # Load requested language
        self._translations = self._load_language_file(language)

        logger.info(f"[I18n] Loaded translations for '{language}'")

    def _load_language_file(self, lang: str) -> dict[str, str]:
        """Load a language file from assets/i18n/."""
        from utils.constants import ASSETS_DIR

        file_path = os.path.join(ASSETS_DIR, "i18n", f"{lang}.json")

        if not os.path.exists(file_path):
            logger.warning(f"[I18n] Language file not found: {file_path}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Flatten nested keys to dot notation
                return self._flatten_dict(data)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error(f"[I18n] Failed to load {file_path}: {exc}")
            return {}

    def _flatten_dict(self, d: dict, prefix: str = "") -> dict[str, str]:
        """Flatten a nested dictionary to dot-notation keys."""
        items: dict[str, str] = {}
        for key, value in d.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                items.update(self._flatten_dict(value, new_key))
            else:
                items[new_key] = str(value)
        return items

    def translate(self, key: str, **kwargs) -> str:
        """Translate a key to the current language.

        Args:
            key: The translation key (dot-notation for nested keys).
            **kwargs: Optional format arguments for string interpolation.

        Returns:
            The translated string, or the key itself if not found.
        """
        # Try current language first
        text = self._translations.get(key)

        # Fall back to English
        if text is None:
            text = self._fallback.get(key)

        # Fall back to key itself
        if text is None:
            return key

        # Apply formatting if kwargs provided
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text

        return text

    @property
    def language(self) -> str:
        """Get the current language code."""
        return self._language


# Module-level convenience function
def _(key: str, **kwargs) -> str:
    """Translate a key to the current language.

    Usage:
        from utils.i18n import _

        # Simple translation
        label = _("widget.battery.tooltip")

        # With formatting
        label = _("widget.battery.low", percent=15)
    """
    return get_i18n().translate(key, **kwargs)


def get_i18n() -> I18n:
    """Get the singleton I18n instance."""
    global _instance
    if _instance is None:
        _instance = I18n()
    return _instance
