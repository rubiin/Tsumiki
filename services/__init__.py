"""Lazy-loaded services for improved startup performance.

Services are initialized on first access, not at import time.
This avoids establishing D-Bus connections until they're actually needed.
"""

# Internal cache for lazy-loaded services
_services_cache = {}


def _get_service(name: str, factory):
    """Lazy-load a service on first access."""
    if name not in _services_cache:
        _services_cache[name] = factory()
    return _services_cache[name]


def get_audio_service():
    """Get the audio service (lazy-loaded)."""
    from fabric.audio import Audio

    return _get_service("audio", Audio)


def get_notification_service():
    """Get the notification service (lazy-loaded)."""
    from .custom_notification import CustomNotifications

    return _get_service("notification", CustomNotifications)


def get_bluetooth_service():
    """Get the bluetooth service (lazy-loaded)."""
    from fabric.bluetooth import BluetoothClient

    return _get_service("bluetooth", BluetoothClient)


def get_power_profiles_service():
    """Get the power profiles service (lazy-loaded)."""
    from fabric.power_profiles import PowerProfiles

    return _get_service("power_profiles", PowerProfiles)


# Backward compatibility - these now trigger lazy loading on access
class _LazyServiceProxy:
    """Proxy that lazily loads a service on first attribute access."""

    def __init__(self, getter):
        object.__setattr__(self, "_getter", getter)
        object.__setattr__(self, "_service", None)

    def _ensure_loaded(self):
        if object.__getattribute__(self, "_service") is None:
            getter = object.__getattribute__(self, "_getter")
            object.__setattr__(self, "_service", getter())
        return object.__getattribute__(self, "_service")

    def __getattr__(self, name):
        return getattr(self._ensure_loaded(), name)

    def __setattr__(self, name, value):
        setattr(self._ensure_loaded(), name, value)


# Backward-compatible lazy proxies
audio_service = _LazyServiceProxy(get_audio_service)
notification_service = _LazyServiceProxy(get_notification_service)
bluetooth_service = _LazyServiceProxy(get_bluetooth_service)
power_pfl_service = _LazyServiceProxy(get_power_profiles_service)
