from time import monotonic

import psutil
from fabric.utils import re

# Pre-compiled regex pattern for interface filtering
_VIRTUAL_IFACE_RE = re.compile(r"^(ifb|lxdbr|virbr|br|vnet|tun|tap)[0-9]+$")


class NetworkSpeed:
    """A service to monitor network speed."""

    __slots__ = (
        "last_sample_time",
        "last_total_down_bytes",
        "last_total_up_bytes",
    )

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "last_sample_time"):
            return  # Already initialized
        self.last_total_down_bytes = 0
        self.last_total_up_bytes = 0
        self.last_sample_time = 0.0

    def get_network_speed(self):
        # Read counters from psutil for all interfaces.
        try:
            interface_counters = psutil.net_io_counters(pernic=True)
        except Exception:
            return {"download": 0.0, "upload": 0.0}

        total_down_bytes = 0
        total_up_bytes = 0

        for interface, counters in interface_counters.items():
            current_interface_down_bytes = int(counters.bytes_recv)
            current_interface_up_bytes = int(counters.bytes_sent)

            # Skip loopback and virtual interfaces or interfaces with invalid byte count
            if (
                interface == "lo"
                or _VIRTUAL_IFACE_RE.match(interface)
                or current_interface_down_bytes < 0
                or current_interface_up_bytes < 0
            ):
                continue

            total_down_bytes += current_interface_down_bytes
            total_up_bytes += current_interface_up_bytes

        # Prime baseline on first sample to avoid a fake spike.
        now = monotonic()
        if self.last_sample_time == 0.0:
            self.last_total_down_bytes = total_down_bytes
            self.last_total_up_bytes = total_up_bytes
            self.last_sample_time = now
            return {"download": 0.0, "upload": 0.0}

        elapsed = max(now - self.last_sample_time, 1e-6)
        down_delta = max(total_down_bytes - self.last_total_down_bytes, 0)
        up_delta = max(total_up_bytes - self.last_total_up_bytes, 0)

        # Return bytes per second, matching common network-rate conventions.
        download_speed = down_delta / elapsed
        upload_speed = up_delta / elapsed

        self.last_total_down_bytes = total_down_bytes
        self.last_total_up_bytes = total_up_bytes
        self.last_sample_time = now

        return {"download": download_speed, "upload": upload_speed}
