from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient
from fabric.powerprofiles import PowerProfiles

from .custom_notification import CustomNotifications

# Fabric services
audio_service = Audio()
notification_service = CustomNotifications()
bluetooth_service = BluetoothClient()
power_pfl_service = PowerProfiles()
