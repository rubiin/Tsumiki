# ruff: noqa: F403,F405
from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient

from .brightness import *
from .custom_notification import *
from .mpris import *
from .network import NetworkClient
from .power_profile import *
from .screen_record import *
from .battery import *
from .weather import *

# Fabric services
audio_service = Audio()
notification_service = CustomNotifications()
bluetooth_service = BluetoothClient()
network_service = NetworkClient()
