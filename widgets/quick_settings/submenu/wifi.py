import gi
from fabric.utils import logger
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GObject, Gtk

from services.network import NetworkService, Wifi
from shared.buttons import QSChevronButton, ScanButton
from shared.list import ListBox
from shared.submenu import QuickSubMenu
from utils.exceptions import NetworkManagerNotFoundError
from utils.icons import text_icons
from utils.widget_utils import nerd_font_icon

try:
    gi.require_version("NM", "1.0")
    from gi.repository import NM
except ValueError:
    raise NetworkManagerNotFoundError()


gi.require_versions({"Gtk": "3.0", "GObject": "2.0"})


icon_to_text_icons = {
    "network-wireless-signal-excellent-symbolic": text_icons["wifi"]["strength_4"],
    "network-wireless-signal-good-symbolic": text_icons["wifi"]["strength_3"],
    "network-wireless-signal-ok-symbolic": text_icons["wifi"]["strength_2"],
    "network-wireless-signal-weak-symbolic": text_icons["wifi"]["strength_1"],
    "network-wireless-signal-none-symbolic": text_icons["wifi"]["strength_0"],
}


class WifiSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = NetworkService()

        self.available_networks_listbox = ListBox(
            visible=True, name="available-networks-listbox"
        )
        self.client.connect("device-ready", self.on_device_ready)

        self.scan_button = ScanButton(
            on_clicked=self.start_new_scan,
            sensitive=False,
        )

        self.child = ScrolledWindow(
            min_content_size=(-1, 190),
            max_content_size=(-1, 190),
            propagate_width=True,
            propagate_height=True,
            v_expand=True,
            v_scrollbar_policy="automatic",
            h_scrollbar_policy="never",
            child=self.available_networks_listbox,
        )

        super().__init__(
            title="Network",
            title_icon=text_icons["wifi"]["generic"],
            scan_button=self.scan_button,
            child=self.child,
            **kwargs,
        )

        if self.child:
            adjustment = self.child.get_vadjustment()

            adjustment.connect("value-changed", self.on_scroll)

        self.revealer.connect(
            "notify::child-revealed",
            self.start_new_scan,
        )

    def on_child_revealed(self, *_):
        self.scan_button.set_sensitive(False)
        self.start_new_scan()
        self.scan_button.set_sensitive(True)

    def _load_next_batch(self, aps):
        if self.loading or self.items_loaded >= self.max_items:
            return

        self.loading = True

        items_to_add = min(self.batch_size, self.max_items - self.items_loaded)

        for i in range(self.items_loaded, self.items_loaded + items_to_add):
            notification_item = self.make_button_from_ap(aps[i])
            self.available_networks_listbox.add(notification_item)

        self.items_loaded += items_to_add
        self.loading = False

    def on_scroll(self, adjustment: Gtk.Adjustment):
        value = adjustment.get_value()
        upper = adjustment.get_upper()
        page_size = adjustment.get_page_size()

        if value + page_size >= upper - 50:
            self._load_next_batch(self.wifi_device.access_points)

    def on_scan(self, _, value, *args):
        """Called when the scan is complete."""
        if value:
            logger.info("[WifiService]Scan complete, updating available networks...")
            self.refresh_wifi_list()
            self.scan_button.set_sensitive(True)

    def refresh_wifi_list(self):
        # Always clear and rebuild the list
        self.items_loaded = 0
        self.batch_size = 7
        self.loading = False
        self.max_items = len(self.wifi_device.access_points) if self.wifi_device else 0
        self.available_networks_listbox.remove_all()
        if self.wifi_device:
            self._load_next_batch(self.wifi_device.access_points)

    def start_new_scan(self, *_):
        self.wifi_device.scan()
        self.scan_button.play_animation()

    def on_device_ready(self, client: NetworkService):
        self.wifi_device = client.wifi_device
        if self.wifi_device:
            self.wifi_device.connect("scanning", self.on_scan)
            self.wifi_device.connect("changed", lambda *_: self.refresh_wifi_list())

    def build_wifi_options(self):
        self.refresh_wifi_list()

    def make_button_from_ap(self, ap: NM.AccessPoint) -> Button:
        security_label = ""
        ssid = ap.get("ssid")
        icon_name = ap.get("icon-name")

        ap_container = Box(
            style="padding: 5px;",
            orientation="h",
            spacing=4,
            tooltip_markup=ssid,
        )
        ap_container.add(
            nerd_font_icon(
                icon=icon_to_text_icons.get(
                    icon_name,
                    text_icons["wifi"]["generic"],
                ),
                props={
                    "style_classes": ["panel-font-icon"],
                    "style": "font-size: 16px;",
                },
            )
        )
        ssid_button = Button(
            label=ssid,
            style_classes=["submenu-item-label", "wifi-ssid-button"],
            v_align="center",
            h_align="start",
            ellipsization="end",
            h_expand=True,
            on_clicked=lambda btn: self.on_connect_clicked(ap),
        )
        ap_container.add(ssid_button)

        # Use BSSID for active AP check, fallback to SSID if needed
        ap_bssid = ap.get("bssid")
        is_active = (
            self.wifi_device.state == "activated"
            and self.wifi_device.is_active_ap(ap_bssid)
        )
        if is_active:
            ap_container.add(
                Button(
                    label="-",
                    style_classes=["wifi-disconnect-button"],
                    v_align="center",
                    h_align="end",
                    on_clicked=lambda btn: self.on_disconnect_clicked(ap),
                )
            )

        wifi_item = Gtk.ListBoxRow(visible=True)

        if is_active:
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

    def on_disconnect_clicked(self, ap: NM.AccessPoint):
        ssid = ap.get("ssid")
        if self.wifi_device:
            self.wifi_device.disconnect_network(ssid)

    def on_connect_clicked(self, ap: NM.AccessPoint):
        ssid = ap.get("ssid")
        # Optionally, prompt for password if needed (not implemented here)
        # For now, try to connect without password
        if self.wifi_device:
            self.wifi_device.connect_network(ssid)


class WifiToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=text_icons["wifi"]["generic"],
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

            self.action_icon.set_label(
                icon_to_text_icons.get(
                    wifi.get_property("icon-name"),
                    text_icons["wifi"]["generic"],
                ),
            )

            wifi.bind_property(
                "icon-name",
                self.action_icon,
                "label",
                GObject.BindingFlags.DEFAULT,
                lambda _, x: icon_to_text_icons.get(
                    x,
                    text_icons["wifi"]["generic"],
                ),
            )

            self.action_label.set_label(wifi.get_property("ssid"))
            wifi.bind_property("ssid", self.action_label, "label")

        else:
            self.action_button.set_sensitive(False)
            self.action_label.set_label("Wi-Fi device not available.")

    def on_action(self, _):
        wifi: Wifi | None = self.client.wifi_device
        if wifi:
            wifi.toggle_wifi()

    def update_status(self, wifi: Wifi):
        self.action_icon.set_label(
            icon_to_text_icons.get(
                wifi.get_property("icon-name"),
                text_icons["wifi"]["generic"],
            ),
        )
