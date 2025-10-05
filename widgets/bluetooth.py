from fabric.bluetooth import BluetoothClient
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon


class BlueToothWidget(ButtonWidget):
    """A widget to display the Bluetooth status."""

    def __init__(self, **kwargs):
        super().__init__(name="bluetooth", **kwargs)
        self.bluetooth_client = BluetoothClient()

        self.icons = text_icons["bluetooth"]

        self.bluetooth_icon = nerd_font_icon(
            icon=self.icons["enabled"],
            props={"style_classes": ["panel-font-icon"]},
        )

        self.container_box.add(
            self.bluetooth_icon,
        )

        if self.config.get("label", True):
            self.bt_label = Label(label="On", style_classes=["panel-text"])
            self.container_box.add(self.bt_label)

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        self.update_bluetooth_status()

    def update_bluetooth_status(self, *_):
        bt_status = "on" if self.bluetooth_client.enabled else "off"

        icon = self.icons["enabled"] if bt_status == "on" else self.icons["disabled"]

        self.bluetooth_icon.set_label(icon)

        if self.config.get("label", True):
            self.bt_label.set_text(bt_status.capitalize())

        if self.config.get("tooltip", False):
            self.set_tooltip_text(f"Bluetooth is {bt_status}")
