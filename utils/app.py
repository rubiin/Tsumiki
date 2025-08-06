from fabric.utils.helpers import get_desktop_applications


class AppUtils:
    """Singleton utility class for managing desktop applications"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._all_applications = get_desktop_applications()
        self._app_identifiers = self.build_app_identifiers_map()

    @property
    def all_applications(self):
        """Return all desktop applications."""
        return self._all_applications

    @property
    def app_identifiers(self):
        """Return the mapping of app identifiers to DesktopApp objects."""
        return self._app_identifiers

    def refresh(self):
        """Return all desktop applications, optionally refreshing the list."""
        self._all_applications = get_desktop_applications()
        self._app_identifiers = self.build_app_identifiers_map()
        return True

    def _normalize_window_class(self, class_name):
        """Normalize window class by removing common suffixes and lowercase."""
        if not class_name:
            return ""

        normalized = class_name.lower()

        # Remove common suffixes
        suffixes = [".bin", ".exe", ".so", "-bin", "-gtk"]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[: -len(suffix)]

        return normalized

    def classes_match(self, class1, class2):
        """Check if two window class names match with stricter comparison."""
        if not class1 or not class2:
            return False

        # Normalize both classes
        norm1 = self._normalize_window_class(class1)
        norm2 = self._normalize_window_class(class2)

        # Direct match after normalization
        return norm1 == norm2

        # Don't do substring matching as it's too error-prone
        # This avoids incorrectly matching flatpak apps and others

    # -------------------------
    # App Lookup Helpers
    # -------------------------

    def build_app_identifiers_map(self):
        """Create a fast lookup dictionary for app identifiers."""
        identifiers = {}
        for app in self._all_applications:
            for key in [
                app.name,
                app.display_name,
                app.window_class,
                getattr(app, "executable", None) and app.executable.split("/")[-1],
                getattr(app, "command_line", None)
                and app.command_line.split()[0].split("/")[-1],
            ]:
                if key:
                    identifiers[key.lower()] = app
        return identifiers

    def find_app(self, app_identifier):
        """Find an app by dict or direct identifier."""
        if not app_identifier:
            return None
        if isinstance(app_identifier, dict):
            for key in [
                "window_class",
                "executable",
                "command_line",
                "name",
                "display_name",
            ]:
                if app_identifier.get(key):
                    app = self._find_app_by_key(app_identifier[key])
                    if app:
                        return app
            return None
        return self._find_app_by_key(app_identifier)

    def _find_app_by_key(self, key_value):
        """Find app by identifier or partial match."""
        if not key_value:
            return None
        normalized_id = str(key_value).lower()
        if normalized_id in self._app_identifiers:
            return self._app_identifiers[normalized_id]

        # Fallback partial matching
        return next(
            (
                app
                for app in self._all_applications
                if any(
                    normalized_id in (getattr(app, attr) or "").lower()
                    for attr in [
                        "name",
                        "display_name",
                        "window_class",
                        "executable",
                        "command_line",
                    ]
                )
            ),
            None,
        )
