import dbus
from dbus.mainloop.glib import DBusGMainLoop
from fabric import Service, Signal
from loguru import logger



DeviceState = {
    0: "UNKNOWN",
    1: "CHARGING",
    2: "DISCHARGING",
    3: "EMPTY",
    4: "FULLY_CHARGED",
    5: "PENDING_CHARGE",
    6: "PENDING_DISCHARGE",
}

class BatteryService(Service):
    """Service to interact with the PowerProfiles service."""

    @Signal
    def temperature(self, value: float) -> None:
        """Signal emitted when battery changes."""


    @Signal
    def percentage(self, value: float) -> None:
        """Signal emitted when battery changes."""

    @Signal
    def time_to_empty(self, value: float) -> None:
        """Signal emitted when battery changes."""

    @Signal
    def time_to_full(self, value: float) -> None:
        """Signal emitted when battery changes."""

    @Signal
    def icon(self, value: str) -> None:
        """Signal emitted when battery changes."""

    @Signal
    def state(self, value: str) -> None:
        """Signal emitted when battery changes."""

    instance = None

    @staticmethod
    def get_default():
        if BatteryService.instance is None:
            BatteryService.instance = BatteryService()

        return BatteryService.instance

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self.bus_name = "org.freedesktop.UPower"
        self.object_path = "/org/freedesktop/UPower/devices/DisplayDevice"


        # Set up the dbus main loop
        DBusGMainLoop(set_as_default=True)

        self.bus = dbus.SystemBus()

        self.power_profiles_obj = self.bus.get_object(self.bus_name, self.object_path)

        self.iface = dbus.Interface(
            self.power_profiles_obj, "org.freedesktop.DBus.Properties"
        )

        # Connect the 'g-properties-changed' signal to the handler
        self.iface.connect_to_signal("PropertiesChanged", self.handle_property_change)

    def get(self, property: str):
        try:
            return self.iface.Get("org.freedesktop.UPower.Device", property)

        except dbus.DBusException as e:
            logger.error(f"[Battery] Error retrieving info: {e}")


    # Function to handle properties change signals
    def handle_property_change(self, proxy, changed, invalidated):

      signal_mapping = {
          "Percentage": "percentage",
          "Temperature": "temperature",
          "TimeToEmpty": "time_to_empty",
          "TimeToFull": "time_to_full",
          "Icon": "icon",
          "State": "state"
      }

      # Loop through the mapping and emit signals if the key exists in 'changed'
      for key, signal in signal_mapping.items():
          if key in changed:
              self.emit(signal, changed[key])
