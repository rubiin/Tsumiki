from fabric import Service, Signal
from gi.repository import Gio, GLib
from loguru import logger

from utils.colors import Colors
from utils.dbus_helper import GioDBusHelper
from utils.icons import text_icons


class PowerProfilesService(Service):
    """Service to interact with the PowerProfiles service via GIO."""

    @Signal
    def profile(self, value: str) -> None:
        """Signal emitted when profile changes."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PowerProfilesService, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bus_name = "net.hadess.PowerProfiles"
        self.object_path = "/net/hadess/PowerProfiles"
        self.interface_name = "net.hadess.PowerProfiles"

        self.power_profiles = {
            "power-saver": {
                "name": "Power Saver",
                "icon": text_icons["powerprofiles"]["power-saver"],
            },
            "balanced": {
                "name": "Balanced",
                "icon": text_icons["powerprofiles"]["balanced"],
            },
            "performance": {
                "name": "Performance",
                "icon": text_icons["powerprofiles"]["performance"],
            },
        }

        self.dbus_helper = GioDBusHelper(
            bus_type=Gio.BusType.SYSTEM,
            bus_name=self.bus_name,
            object_path=self.object_path,
            interface_name=self.interface_name,
        )

        self.bus = self.dbus_helper.bus
        self.proxy = self.dbus_helper.proxy

        # Listen for PropertiesChanged signals
        self.dbus_helper.listen_signal(
            sender=self.bus_name,
            interface_name="org.freedesktop.DBus.Properties",
            member="PropertiesChanged",
            object_path=self.object_path,
            callback=self.handle_property_change,
        )

    def get_current_profile(self):
        try:
            value = self.proxy.get_cached_property("ActiveProfile")
            return value.unpack().strip() if value else "balanced"
        except Exception as e:
            logger.exception(
                f"[PowerProfile] Error retrieving current power profile: {e}"
            )
            return "balanced"

    def set_power_profile(self, profile: str):
        try:
            self.dbus_helper.set_property(
                self.bus_name,
                self.object_path,
                self.interface_name,
                "ActiveProfile",
                GLib.Variant("s", profile),
            )
            logger.info(f"[PowerProfile] Power profile set to {profile}")
        except Exception as e:
            logger.exception(
                f"[PowerProfile] Could not change power level to {profile}: {e}"
            )

    def handle_property_change(self, *_args):
        """Callback for property change signals.
        args: (connection, sender_name, object_path,
        interface_name, signal_name,parameters)"""

        parameters = _args[-1]
        interface, changed_props, _invalidated = parameters.unpack()
        if "ActiveProfile" in changed_props:
            new_profile = changed_props["ActiveProfile"]
            logger.info(f"{Colors.INFO}Profile changed: {new_profile}")
            self.emit("profile", new_profile)

    def get_profile_icon(self, profile: str) -> str:
        return self.power_profiles.get(profile, self.power_profiles["balanced"]).get(
            "icon"
        )
