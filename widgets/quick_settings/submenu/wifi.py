from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import Gtk

from services import NetworkService, Wifi
from shared.buttons import QSChevronButton, ScanButton
from shared.list import ListBox
from shared.submenu import QuickSubMenu
from utils.icons import symbolic_icons


class WifiSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = NetworkService()

        self.client.connect("device-ready", self.on_device_ready)

        self.available_networks_listbox = ListBox(
            visible=True, name="available-networks-listbox"
        )

        self.scan_button = ScanButton()

        self.scan_button.set_sensitive(False)

        self.scan_button.connect("clicked", self.start_new_scan)

        self.child = ScrolledWindow(
            min_content_size=(-1, 190),
            max_content_size=(-1, 190),
            propagate_width=True,
            propagate_height=True,
            child=self.available_networks_listbox,
        )

        super().__init__(
            title="Network",
            title_icon=symbolic_icons["network"]["wifi"]["generic"],
            scan_button=self.scan_button,
            child=self.child,
            **kwargs,
        )

    def on_scan(self, _, value, *args):
        """Called when the scan is complete."""

        if value:
            self.scan_button.play_animation()
        else:
            self.scan_button.stop_animation()

    def start_new_scan(self, *_):
        self.wifi_device.scan()
        self.build_wifi_options()
        self.scan_button.play_animation()

    def on_device_ready(self, client: NetworkService):
        self.wifi_device = client.wifi_device
        if self.wifi_device:
            self.scan_button.set_sensitive(True)
            self.start_new_scan(None)
            self.wifi_device.connect("changed", self.start_new_scan)

    def build_wifi_options(self):
        self.available_networks_listbox.remove_all()
        for ap in self.wifi_device.access_points:
            if ap.get("ssid") != "Unknown":
                wifi_item = self.make_button_from_ap(ap)
                self.available_networks_listbox.add(wifi_item)

    def make_button_from_ap(self, ap) -> Button:
        security_label = ""

        ap_container = Box(
            style="padding: 5px;",
            orientation="h",
            spacing=4,
            tooltip_markup=ap.get("ssid"),
            children=[
                Image(
                    icon_name=ap.get("icon-name"),
                    icon_size=18,
                ),
                Label(
                    label=ap.get("ssid"),
                    style_classes="submenu-item-label",
                    ellipsization="end",
                    v_align="center",
                    h_align="start",
                    h_expand=True,
                ),
            ],
        )

        wifi_item = Gtk.ListBoxRow(visible=True)

        if self.wifi_device.state == "activated" and self.wifi_device.is_active_ap(
            ap.get("ssid")
        ):
            security_label = " " + security_label

            if self.wifi_device.get_ap_security(ap.get("active-ap")) != "unsecured":
                security_label = security_label + ""

        ap_container.add(
            Label(
                markup=f"<b>{security_label}</b>",
                style="font-size: 14px",
                v_align="center",
            )
        )

        wifi_item.add(ap_container)
        return wifi_item


class WifiToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=symbolic_icons["network"]["wifi"]["generic"],
            action_label=" Wifi Disabled",
            submenu=submenu,
            **kwargs,
        )
        self.client = NetworkService()
        self.client.connect("device-ready", self.update_action_button)

        self.connect("action-clicked", self.on_action)

    def update_action_button(self, client: NetworkService):
        wifi = client.wifi_device

        if wifi:
            wifi.connect(
                "notify::enabled",
                lambda *_: self.set_active_style(wifi.get_property("enabled")),  # type: ignore
            )
            wifi.connect("changed", self.update_status)

            self.action_icon.set_from_icon_name(
                wifi.get_property("icon-name") + "-symbolic", self.pixel_size
            )
            wifi.bind_property("icon-name", self.action_icon, "icon-name")

            self.action_label.set_label(wifi.get_property("ssid"))
            wifi.bind_property("ssid", self.action_label, "label")

        else:
            self.action_button.set_sensitive(False)
            self.action_label.set_label("Wi-Fi device not available.")

    def on_action(self, btn):
        wifi: Wifi | None = self.client.wifi_device
        if wifi:
            wifi.toggle_wifi()

    def update_status(self, wifi: Wifi):
        self.action_icon.set_from_icon_name(
            wifi.icon_name,
            self.pixel_size,
        )
