from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services import NetworkClient, Wifi, network_service
from shared import Animator, CircleImage, HoverButton, QuickSubMenu, QuickSubToggle


class WifiSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = network_service
        self.wifi_device = self.client.wifi_device
        self.client.connect("device-ready", self.on_device_ready)

        self.available_networks_box = Box(orientation="v", spacing=4, h_expand=True)

        self.scan_image = CircleImage(
            image_file=get_relative_path("../../../assets/icons/refresh.png"),
            size=24,
        )

        self.scan_animator = Animator(
            bezier_curve=(0, 0, 1, 1),
            duration=4,
            min_value=0,
            max_value=360,
            tick_widget=self,
            repeat=False,
            notify_value=lambda p, *_: self.scan_image.set_angle(p.value),
        )

        self.scan_button = HoverButton(
            style_classes="submenu-button",
            name="scan-button",
            image=self.scan_image,
        )
        self.scan_button.connect("clicked", self.start_new_scan)

        self.child = ScrolledWindow(
            min_content_size=(-1, 190),
            max_content_size=(-1, 190),
            propagate_width=True,
            propagate_height=True,
            child=self.available_networks_box,
        )

        super().__init__(
            title="Network",
            title_icon="network-wireless-symbolic",
            scan_button=self.scan_button,
            child=Box(orientation="v", children=[self.child]),
            **kwargs,
        )

    def start_new_scan(self, _):
        self.client.wifi_device.scan() if self.client.wifi_device else None
        self.build_wifi_options()
        self.scan_animator.play()

    def on_device_ready(self, client: NetworkClient):
        self.wifi_device = client.wifi_device
        self.build_wifi_options()

    def build_wifi_options(self):
        self.available_networks_box.children = []
        if not self.wifi_device:
            return
        for ap in self.wifi_device.access_points:
            if ap.get("ssid") != "Unknown":
                btn = self.make_button_from_ap(ap)
                self.available_networks_box.add(btn)

    def make_button_from_ap(self, ap) -> Button:
        ap_button = Button(style_classes="submenu-button", name="wifi-ap-button")
        ap_button.add(
            Box(
                style="padding: 5px;",
                children=[
                    Image(
                        icon_name=ap.get("icon-name"),
                        icon_size=18,
                    ),
                    Label(label=ap.get("ssid"), style_classes="submenu-item-label"),
                ],
            )
        )
        ap_button.connect(
            "clicked", lambda _: self.client.connect_wifi_bssid(ap.get("bssid"))
        )
        return ap_button


class WifiToggle(QuickSubToggle):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon="network-wireless-disabled-symbolic",
            action_label=" Wifi Disabled",
            submenu=submenu,
            **kwargs,
        )
        self.client = network_service
        self.client.connect("device-ready", self.update_action_button)

        self.connect("action-clicked", self.on_action)

    def update_action_button(self, client: NetworkClient):
        wifi = client.wifi_device

        if wifi:
            wifi.connect(
                "notify::enabled",
                lambda *args: self.set_active_style(wifi.get_property("enabled")),  # type: ignore
            )

            self.action_icon.set_from_icon_name(
                wifi.get_property("icon-name") + "-symbolic", 18
            )
            wifi.bind_property("icon-name", self.action_icon, "icon-name")

            self.action_label.set_label(wifi.get_property("ssid"))
            wifi.bind_property("ssid", self.action_label, "label")

    def on_action(self, btn):
        wifi: Wifi | None = self.client.wifi_device
        if wifi:
            wifi.toggle_wifi()
