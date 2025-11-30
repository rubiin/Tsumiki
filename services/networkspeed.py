import re

# Pre-compiled regex patterns for interface filtering
_FIELDS_RE = re.compile(r"\W+")
_VIRTUAL_IFACE_RE = re.compile(r"^(ifb|lxdbr|virbr|br|vnet|tun|tap)[0-9]+$")


class NetworkSpeed:
    """A service to monitor network speed."""

    __slots__ = ("interval", "last_total_down_bytes", "last_total_up_bytes")

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "interval"):
            return  # Already initialized
        self.interval = 1000
        self.last_total_down_bytes = 0
        self.last_total_up_bytes = 0

    def get_network_speed(self):
        # Read /proc/net/dev directly instead of spawning subprocess
        try:
            with open("/proc/net/dev", "r") as f:
                lines = f.readlines()
        except OSError:
            return {"download": 0.0, "upload": 0.0}

        total_down_bytes = 0
        total_up_bytes = 0

        for line in lines:
            fields = _FIELDS_RE.split(line.strip())
            if len(fields) <= 2:
                continue

            interface = fields[0]
            try:
                current_interface_down_bytes = int(fields[1])
                current_interface_up_bytes = int(fields[9])
            except (ValueError, IndexError):
                continue

            # Skip loopback and virtual interfaces or interfaces with invalid byte counts
            if (
                interface == "lo"
                or _VIRTUAL_IFACE_RE.match(interface)
                or current_interface_down_bytes < 0
                or current_interface_up_bytes < 0
            ):
                continue

            total_down_bytes += current_interface_down_bytes
            total_up_bytes += current_interface_up_bytes

        # Compute the speeds
        if self.last_total_down_bytes == 0:
            self.last_total_down_bytes = total_down_bytes
        if self.last_total_up_bytes == 0:
            self.last_total_up_bytes = total_up_bytes

        download_speed = (total_down_bytes - self.last_total_down_bytes) / self.interval
        upload_speed = (total_up_bytes - self.last_total_up_bytes) / self.interval

        self.last_total_down_bytes = total_down_bytes
        self.last_total_up_bytes = total_up_bytes

        return {"download": download_speed, "upload": upload_speed}
