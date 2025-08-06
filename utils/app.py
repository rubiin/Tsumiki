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

    def all_applications(self, refresh=False):
        if refresh:
            self.refresh_applications()
        return self._all_applications
