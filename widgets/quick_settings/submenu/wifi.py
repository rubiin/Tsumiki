import gi
from fabric.utils import GObject, Gtk, bulk_connect, logger
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services.network import NetworkService, Wifi
from shared.buttons import QSChevronButton, ScanButton
from shared.list import ListBox
from shared.submenu import QuickSubMenu
from utils.exceptions import NetworkManagerNotFoundError
from utils.icons import get_text_icon, network_icon_to_text_icons
from widgets.quick_settings.components import QuickSettingsIconLabelRow

try:
    gi.require_version("NM", "1.0")
    from gi.repository import NM
except ValueError:
    raise NetworkManagerNotFoundError()


class WifiSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = NetworkService()
        self.wifi_device = None
        self._wifi_connected = None

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
            title="network",
            title_icon=get_text_icon("wifi.generic"),
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
        if not self.wifi_device or self._wifi_connected == self.wifi_device:
            return

        bulk_connect(
            self.wifi_device,
            {
                "scanning": self.on_scan,
                "changed": lambda *_: self.refresh_wifi_list(),
            },
        )
        self._wifi_connected = self.wifi_device

    def build_wifi_options(self):
        self.refresh_wifi_list()

    def _prompt_for_password(self, ssid: str) -> str | None:
        dialog = Gtk.Dialog(
            title=f"Connect to {ssid}",
            modal=True,
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Connect", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        prompt_label = Gtk.Label(label=f"Enter password for {ssid}")
        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        password_entry.set_activates_default(True)

        # GTK3 uses pack_start, GTK4 uses append.
        if hasattr(content, "append"):
            content.append(prompt_label)
            content.append(password_entry)
        else:
            content.pack_start(prompt_label, False, False, 4)
            content.pack_start(password_entry, False, False, 4)

        dialog.show_all()
        response = dialog.run()
        password = password_entry.get_text().strip()
        dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return None

        return password

    def make_button_from_ap(self, ap: NM.AccessPoint) -> Button:
        ssid = ap.get("ssid")
        icon_name = ap.get("icon-name")
        is_secured = ap.get("secured")
        security_label = get_text_icon("ui.lock") if is_secured else ""

        ap_container = CenterBox(
            orientation="h",
            spacing=10,
            h_expand=True,
        )

        ap_row = QuickSettingsIconLabelRow(
            icon=network_icon_to_text_icons.get(
                icon_name,
                get_text_icon("wifi.generic"),
            ),
            label=ssid,
            icon_size=16,
            row_classes=["wifi-ap-main"],
        )

        ap_container.start_children = (ap_row,)

        # Use BSSID for active AP check, fallback to SSID if needed
        ap_bssid = ap.get("bssid")
        is_active = (
            self.wifi_device.state == "activated"
            and self.wifi_device.is_active_ap(ap_bssid)
        )
        if is_active:
            security_label = f"{get_text_icon('ui.tick')} {security_label}"
            ap_row.add_style_class("active")

        wifi_item = Gtk.ListBoxRow(visible=True)

        ap_container.end_children = Label(
            markup=f"<b>{security_label}</b>",
            style_classes="wifi-ap-status-label",
            v_align="center",
        )

        ap_btn_container = Button(
            child=ap_container,
            h_expand=True,
            style_classes="wifi-ap-button",
        )

        wifi_item.add(ap_btn_container)
        return wifi_item

    def on_disconnect_clicked(self, ap: NM.AccessPoint):
        ssid = ap.get("ssid")
        if self.wifi_device:
            self.wifi_device.disconnect_network(ssid)

    def on_connect_clicked(self, ap: NM.AccessPoint):
        ssid = ap.get("ssid")
        if not self.wifi_device:
            return

        if ap.get("secured"):
            password = self._prompt_for_password(ssid)
            if password is None:
                return
            if not password:
                logger.warning("[WifiService] Empty password, aborting connection")
                return

            self.wifi_device.connect_network(ssid, password=password)
            return

        # Open network, attempt direct connection.
        self.wifi_device.connect_network(ssid)


class WifiToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=get_text_icon("wifi.generic"),
            action_label=" Wifi Disabled",
            submenu=submenu,
            **kwargs,
        )
        self.client = NetworkService()
        self._bound_wifi = None
        self.client.connect("device-ready", self.update_action_button)

        self.connect("action-clicked", self.on_action)

    def update_action_button(self, client: NetworkService):
        wifi = client.wifi_device

        if wifi:
            if self._bound_wifi != wifi:
                bulk_connect(
                    wifi,
                    {
                        "notify::enabled": lambda *_: self.set_active_style(
                            wifi.get_property("enabled")
                        ),
                        "changed": self.update_status,
                    },
                )
                self._bound_wifi = wifi

            self.action_icon.set_label(
                network_icon_to_text_icons.get(
                    wifi.get_property("icon-name"),
                    get_text_icon("wifi.generic"),
                ),
            )

            wifi.bind_property(
                "icon-name",
                self.action_icon,
                "label",
                GObject.BindingFlags.DEFAULT,
                lambda _, x: network_icon_to_text_icons.get(
                    x,
                    get_text_icon("wifi.generic"),
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
            network_icon_to_text_icons.get(
                wifi.get_property("icon-name"),
                get_text_icon("wifi.generic"),
            ),
        )
