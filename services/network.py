import subprocess
import time
from typing import Any, Literal

import gi
from fabric.core.service import Property, Service, Signal
from fabric.utils import bulk_connect, logger
from gi.repository import Gio

from utils.constants import NETWORK_RECENCY_THRESHOLD_SECONDS
from utils.exceptions import NetworkManagerNotFoundError

try:
    gi.require_version("NM", "1.0")
    from gi.repository import NM
except ValueError:
    raise NetworkManagerNotFoundError()


class Wifi(Service):
    """A service to manage wifi devices"""

    @Signal
    def changed(self) -> None: ...

    @Signal
    def enabled(self) -> bool: ...

    @Signal
    def scanning(self, is_scanning: bool) -> None: ...

    def __init__(self, client: NM.Client, device: NM.DeviceWifi, **kwargs):
        self._client: NM.Client = client
        self._device: NM.DeviceWifi = device
        self._ap: NM.AccessPoint | None = None
        self._ap_signal: int | None = None
        super().__init__(**kwargs)

        self._client.connect(
            "notify::wireless-enabled",
            lambda *args: self.notifier("enabled", args),
        )
        if self._device:
            bulk_connect(
                self._device,
                {
                    "notify::active-access-point": self._activate_ap,
                    "access-point-added": lambda *_: self.emit("changed"),
                    "access-point-removed": lambda *_: self.emit("changed"),
                    "state-changed": self.ap_update,
                },
            )
            self._activate_ap()

    def ap_update(self, *_):
        self.emit("changed")
        for sn in [
            "enabled",
            "internet",
            "strength",
            "frequency",
            "access-points",
            "ssid",
            "state",
            "icon-name",
        ]:
            self.notify(sn)

    def _activate_ap(self, *_):
        if self._ap:
            self._ap.disconnect(self._ap_signal)
        self._ap = self._device.get_active_access_point()
        if not self._ap:
            return

        self._ap_signal = self._ap.connect(
            "notify::strength", lambda *args: self.ap_update()
        )  # type: ignore

    def toggle_wifi(self):
        self._client.wireless_set_enabled(not self._client.wireless_get_enabled())

    def get_ap_security(
        self, nm_ap: NM.AccessPoint
    ) -> Literal["WEP", "WPA1", "WPA2", "802.1X", "unsecured"]:
        """Parse the security flags to return a string with 'WPA2', etc."""
        flags = nm_ap.get_flags()
        wpa_flags = nm_ap.get_wpa_flags()
        rsn_flags = nm_ap.get_rsn_flags()
        sec_str = ""
        if (
            (flags & getattr(NM, "80211ApFlags").PRIVACY)
            and (wpa_flags == 0)
            and (rsn_flags == 0)
        ):
            sec_str += " WEP"
        if wpa_flags != 0:
            sec_str += " WPA1"
        if rsn_flags != 0:
            sec_str += " WPA2"
        if (wpa_flags & getattr(NM, "80211ApSecurityFlags").KEY_MGMT_802_1X) or (
            rsn_flags & getattr(NM, "80211ApSecurityFlags").KEY_MGMT_802_1X
        ):
            sec_str += " 802.1X"

        # If there is no security use "--"
        if sec_str == "":
            sec_str = "unsecured"
        return sec_str.lstrip()

    def scan(self):
        """Start scanning for WiFi networks and emit scanning signal"""
        if self._device:
            self.emit("scanning", True)  # Emit signal that scanning has started
            self._device.request_scan_async(
                None,
                lambda device, result: [
                    device.request_scan_finish(result),
                    self.emit(
                        "scanning", False
                    ),  # Emit signal that scanning has stopped
                ],
            )

    def is_active_ap(self, name) -> bool:
        return self._ap.get_bssid() == name if self._ap else False

    def notifier(self, name: str, *_):
        self.notify(name)
        self.emit("changed")
        return

    def forget_access_point(self, ssid):
        try:
            # List all saved connections
            result = subprocess.check_output(
                "nmcli connection show", shell=True, text=True
            )

            # Find connection ID that matches SSID
            for line in result.splitlines():
                if ssid in line:
                    connection_id = line.split()[0]
                    subprocess.check_call(
                        f"nmcli connection delete id '{connection_id}'", shell=True
                    )
                    logger.info(
                        f"[NetworkService] Deleted saved connection: {connection_id}"
                    )
                    return True

            logger.warning(
                f"[NetworkService] No saved connection found for SSID: {ssid}"
            )
            return False

        except subprocess.CalledProcessError as e:
            logger.exception(f"[NetworkService] Error forgetting connection: {e}")
            return False

    def connect_network(
        self, ssid: str, password: str = "", remember: bool = True
    ) -> bool:
        """Connect to a WiFi network"""
        if not ssid:
            logger.exception("[NetworkService] SSID cannot be empty")
            return False
        try:
            # First try to connect using saved connection
            try:
                subprocess.run(["nmcli", "con", "up", ssid], check=True)
                return True
            except subprocess.CalledProcessError:
                # If saved connection fails, try with password if provided
                if password:
                    cmd = [
                        "nmcli",
                        "device",
                        "wifi",
                        "connect",
                        ssid,
                        "password",
                        password,
                    ]
                    if not remember:
                        cmd.extend(["--temporary"])
                    subprocess.run(cmd, check=True)
                    return True
                return False
        except subprocess.CalledProcessError as e:
            logger.exception(f"[NetworkService] Failed connecting to network: {e}")
            return False

    def disconnect_network(self, ssid: str) -> bool:
        """Disconnect from a WiFi network"""
        if not ssid:
            logger.exception("[NetworkService] SSID cannot be empty")
            return False
        try:
            subprocess.run(["nmcli", "con", "down", ssid], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.exception(f"[NetworkService] Failed disconnecting from network: {e}")
            return False

    @Property(bool, "read-write", default_value=False)
    def enabled(self) -> bool:  # noqa: F811
        return bool(self._client.wireless_get_enabled())

    @enabled.setter
    def enabled(self, value: bool):
        self._client.wireless_set_enabled(value)

    @Property(int, "readable")
    def strength(self):
        return self._ap.get_strength() if self._ap else -1

    @Property(str, "readable")
    def icon_name(self):
        if not self._ap:
            return "network-wireless-disabled-symbolic"

        if self.internet == "activated":
            return {
                80: "network-wireless-signal-excellent-symbolic",
                60: "network-wireless-signal-good-symbolic",
                40: "network-wireless-signal-ok-symbolic",
                20: "network-wireless-signal-weak-symbolic",
                00: "network-wireless-signal-none-symbolic",
            }.get(
                min(80, 20 * round(self._ap.get_strength() / 20)),
                "network-wireless-no-route-symbolic",
            )
        if self.internet == "activating":
            return "network-wireless-acquiring-symbolic"

        return "network-wireless-offline-symbolic"

    @Property(int, "readable")
    def frequency(self):
        return self._ap.get_frequency() if self._ap else -1

    @Property(int, "readable")
    def internet(self):
        active_connection = self._device.get_active_connection()
        if not active_connection:
            return "disconnected"

        return {
            NM.ActiveConnectionState.ACTIVATED: "activated",
            NM.ActiveConnectionState.ACTIVATING: "activating",
            NM.ActiveConnectionState.DEACTIVATING: "deactivating",
            NM.ActiveConnectionState.DEACTIVATED: "deactivated",
        }.get(
            active_connection.get_state(),
            "unknown",
        )

    def make_ap_dict(self, network_data):
        ap = network_data["ap"]
        ssid = network_data["ssid"]
        strength = network_data["strength"]

        return {
            "bssid": ap.get_bssid(),
            "last_seen": ap.get_last_seen(),
            "ssid": ssid,
            "active-ap": self._ap,
            "strength": strength,
            "frequency": ap.get_frequency(),
            "icon-name": {
                80: "network-wireless-signal-excellent-symbolic",
                60: "network-wireless-signal-good-symbolic",
                40: "network-wireless-signal-ok-symbolic",
                20: "network-wireless-signal-weak-symbolic",
                00: "network-wireless-signal-none-symbolic",
            }.get(
                min(80, 20 * round(strength / 20)),
                "network-wireless-no-route-symbolic",
            ),
        }

    @Property(object, "readable")
    def access_points(self) -> list[object]:
        points: list[NM.AccessPoint] = self._device.get_access_points()

        # Filter and deduplicate access points
        unique_networks = {}
        current_time = time.time()

        for ap in points:
            # Skip if no SSID data
            if not ap.get_ssid():
                continue

            ssid_data = ap.get_ssid().get_data()
            if not ssid_data:
                continue

            ssid = NM.utils_ssid_to_utf8(ssid_data)
            if not ssid or ssid.strip() == "":
                continue

            # Skip hidden networks (empty SSID)
            if ssid == "Unknown":
                continue

            strength = ap.get_strength()
            bssid = ap.get_bssid()
            last_seen = ap.get_last_seen()

            # Add network info for filtering
            network_info = {
                "ap": ap,
                "strength": strength,
                "bssid": bssid,
                "ssid": ssid,
                "last_seen": last_seen,
                "is_recent": last_seen == 0
                or (current_time - last_seen) <= NETWORK_RECENCY_THRESHOLD_SECONDS,
            }

            # For duplicate SSIDs, keep the one with the strongest signal
            # But prioritize recent networks over old ones
            if ssid in unique_networks:
                existing = unique_networks[ssid]
                # Prefer recent networks, then strength
                new_is_more_recent = (
                    network_info["is_recent"] and not existing["is_recent"]
                )
                is_stronger_with_same_recency = (
                    network_info["is_recent"] == existing["is_recent"]
                    and strength > existing["strength"]
                )
                if new_is_more_recent or is_stronger_with_same_recency:
                    unique_networks[ssid] = network_info
            else:
                unique_networks[ssid] = network_info

        # Sort by signal strength (strongest first)
        sorted_networks = sorted(
            unique_networks.values(), key=lambda x: x["strength"], reverse=True
        )

        return list(map(self.make_ap_dict, sorted_networks))

    @Property(str, "readable")
    def ssid(self):
        if not self._ap:
            return "Disconnected"
        ssid = self._ap.get_ssid().get_data()
        return NM.utils_ssid_to_utf8(ssid) if ssid else "Unknown"

    @Property(int, "readable")
    def state(self):
        return {
            NM.DeviceState.UNMANAGED: "unmanaged",
            NM.DeviceState.UNAVAILABLE: "unavailable",
            NM.DeviceState.DISCONNECTED: "disconnected",
            NM.DeviceState.PREPARE: "prepare",
            NM.DeviceState.CONFIG: "config",
            NM.DeviceState.NEED_AUTH: "need_auth",
            NM.DeviceState.IP_CONFIG: "ip_config",
            NM.DeviceState.IP_CHECK: "ip_check",
            NM.DeviceState.SECONDARIES: "secondaries",
            NM.DeviceState.ACTIVATED: "activated",
            NM.DeviceState.DEACTIVATING: "deactivating",
            NM.DeviceState.FAILED: "failed",
        }.get(self._device.get_state(), "unknown")


class Ethernet(Service):
    """A service to manage ethernet devices"""

    @Signal
    def changed(self) -> None: ...

    @Signal
    def enabled(self) -> bool: ...

    @Property(int, "readable")
    def speed(self) -> int:
        return self._device.get_speed()

    @Property(str, "readable")
    def internet(self) -> str:
        active_connection = self._device.get_active_connection()
        if not active_connection:
            return "disconnected"

        return {
            NM.ActiveConnectionState.ACTIVATED: "activated",
            NM.ActiveConnectionState.ACTIVATING: "activating",
            NM.ActiveConnectionState.DEACTIVATING: "deactivating",
            NM.ActiveConnectionState.DEACTIVATED: "deactivated",
        }.get(
            active_connection.get_state(),
            "disconnected",
        )

    @Property(str, "readable")
    def icon_name(self) -> str:
        network = self.internet
        if network == "activated":
            return "network-wired-symbolic"

        elif network == "activating":
            return "network-wired-acquiring-symbolic"

        elif self._device.get_connectivity != NM.ConnectivityState.FULL:
            return "network-wired-no-route-symbolic"

        return "network-wired-disconnected-symbolic"

    def __init__(self, client: NM.Client, device: NM.DeviceEthernet, **kwargs) -> None:
        super().__init__(**kwargs)
        self._client: NM.Client = client
        self._device: NM.DeviceEthernet = device

        for names in (
            "active-connection",
            "icon-name",
            "internet",
            "speed",
            "state",
        ):
            self._device.connect(f"notify::{names}", lambda *_: self.notifier(names))

        self._device.connect("notify::speed", lambda *_: print(_))

    def notifier(self, names):
        self.notify(names)
        self.emit("changed")


class NetworkService(Service):
    """A service to manage network devices"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @Signal
    def device_ready(self) -> None: ...

    def __init__(self, **kwargs):
        self._client: NM.Client | None = None
        self.wifi_device: Wifi | None = None
        self.ethernet_device: Ethernet | None = None
        super().__init__(**kwargs)
        NM.Client.new_async(
            cancellable=None,
            callback=self._init_network_client,
            **kwargs,
        )

    def _init_network_client(self, client: NM.Client, task: Gio.Task, **kwargs):
        self._client = client
        wifi_device: NM.DeviceWifi | None = self._get_device(NM.DeviceType.WIFI)  # type: ignore
        ethernet_device: NM.DeviceEthernet | None = self._get_device(
            NM.DeviceType.ETHERNET
        )

        if wifi_device:
            self.wifi_device = Wifi(self._client, wifi_device)
            self.emit("device-ready")

        if ethernet_device:
            self.ethernet_device = Ethernet(client=self._client, device=ethernet_device)
            self.emit("device-ready")

        self.notify("primary-device")

    def _get_device(self, device_type) -> Any:
        devices: list[NM.Device] = self._client.get_devices()  # type: ignore
        return next(
            (x for x in devices if x.get_device_type() == device_type),
            None,
        )

    def _get_primary_device(self) -> Literal["wifi", "wired"] | None:
        if not self._client:
            return None

        if self._client.get_primary_connection() is None:
            return "wifi"
        return (
            "wifi"
            if "wireless"
            in str(self._client.get_primary_connection().get_connection_type())
            else "wired"
            if "ethernet"
            in str(self._client.get_primary_connection().get_connection_type())
            else None
        )

    @Property(str, "readable")
    def primary_device(self) -> Literal["wifi", "wired"] | None:
        return self._get_primary_device()
