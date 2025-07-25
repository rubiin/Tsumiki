from fabric import Service, Signal
from gi.repository import Gio, GLib
from loguru import logger

from utils.dbus_helper import GioDBusHelper
from utils.icons import text_icons


class PowerProfilesService(Service):
    """Service to interact with the PowerProfiles service via GIO."""

    @Signal
    def changed(self) -> None:
        """Signal emitted when profile changes."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bus_name = "net.hadess.PowerProfiles"
        self.object_path = "/net/hadess/PowerProfiles"
        self.interface_name = "net.hadess.PowerProfiles"

        self.power_profiles = {}

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
            member="PropertiesChanged",
            callback=self.handle_property_change,
        )

        for profile in self.get_profiles():
            profile_name = profile.get("Profile", "")

            if profile_name == "balanced":
                self.power_profiles[profile_name] = {
                    "name": "Balanced",
                    "icon": text_icons["powerprofiles"]["balanced"],
                }
            elif profile_name == "performance":
                self.power_profiles[profile_name] = {
                    "name": "Performance",
                    "icon": text_icons["powerprofiles"]["performance"],
                }
            elif profile_name == "power-saver":
                self.power_profiles[profile_name] = {
                    "name": "Power Saver",
                    "icon": text_icons["powerprofiles"]["power-saver"],
                }

    def get_profiles(self):
        """Retrieve available power profiles."""
        try:
            value = self.proxy.get_cached_property("Profiles")
            return value.unpack() if value else []
        except Exception as e:
            logger.exception(f"[PowerProfile] Error retrieving profiles: {e}")
            return []

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
                interface_name=self.interface_name,
                property_name="ActiveProfile",
                value_variant=GLib.Variant("s", profile),
            )
            logger.info(f"[PowerProfile] Power profile set to {profile}")
        except Exception as e:
            logger.exception(
                f"[PowerProfile] Could not change power level to {profile}: {e}"
            )

    def handle_property_change(self, *_):
        self.emit("changed")

    def get_profile_icon(self, profile: str) -> str:
        return self.power_profiles.get(profile, self.power_profiles["balanced"]).get(
            "icon"
        )
