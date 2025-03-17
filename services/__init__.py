# ruff: noqa: F403,F405
from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient

from .battery import *
from .brightness import *
from .custom_notification import *
from .mpris import *
from .network import *
from .networkspeed import *
from .power_profile import *
from .screen_record import *
from .weather import *

# Fabric services
audio_service = Audio()
notification_service = CustomNotifications()
bluetooth_service = BluetoothClient()
network_service = NetworkClient()
battery_service = BatteryService.get_default()
network_speed = NetworkSpeed.get_default()
