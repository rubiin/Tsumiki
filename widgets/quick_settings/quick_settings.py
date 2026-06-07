from fabric.utils import GLib, Gtk, bulk_connect, invoke_repeater, logger, os
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label

import utils.functions as helpers
from services import (
    audio_service,
)
from services.brightness import BrightnessService
from services.mpris import MprisPlayerManager
from services.network import NetworkService, Wifi
from shared.buttons import HoverButton, QSChevronButton
from shared.circle_image import CircularImage
from shared.dialog import Dialog
from shared.media import PlayerBoxStack
from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from utils.constants import ASSETS_DIR
from utils.functions import safe_disconnect
from utils.icons import get_text_icon, network_icon_to_text_icons
from utils.widget_utils import (
    get_audio_icon_name,
    get_brightness_icon_name,
    nerd_font_icon,
)
from widgets.quick_settings.submenu.hyprsunset import (
    HyprSunsetSubMenu,
    HyprSunsetToggle,
)

from .shortcuts import ShortcutsContainer
from .submenu.bluetooth import BluetoothSubMenu, BluetoothToggle
from .submenu.power_profiles import PowerProfileSubMenu, PowerProfileToggle
from .submenu.wifi import WifiSubMenu, WifiToggle
from .togglers import (
    HyprIdleQuickSetting,
    NotificationQuickSetting,
)


class QuickSettingsButtonBox(Box):
    """A box to display the quick settings buttons."""

    def close_all_submenus(self, *_):
        if self.active_submenu is not None:
            self.active_submenu._reveal(False)
            self.active_submenu = None

    def __init__(self, popup, **kwargs):
        super().__init__(
            orientation="v",
            name="quick-settings-button-box",
            spacing=4,
            h_align="start",
            v_align="start",
            v_expand=True,
            **kwargs,
        )

        self.grid = Grid(
            row_spacing=10,
            column_spacing=10,
            column_homogeneous=True,
            row_homogeneous=True,
        )

        self.active_submenu = None

        # Bluetooth
        self.bluetooth_toggle = BluetoothToggle(
            submenu=BluetoothSubMenu(),
        )

        # Wifi
        self.wifi_toggle = WifiToggle(
            submenu=WifiSubMenu(),
        )

        self.power_pfl = PowerProfileToggle(submenu=PowerProfileSubMenu(), popup=popup)

        self.hyprsunset = HyprSunsetToggle(submenu=HyprSunsetSubMenu(), popup=popup)
        self.hypridle = HyprIdleQuickSetting(popup=popup)
        self.notification_btn = NotificationQuickSetting(popup=popup)

        self.grid.attach(self.wifi_toggle, 1, 1, 1, 1)

        self.grid.attach_next_to(
            self.bluetooth_toggle, self.wifi_toggle, Gtk.PositionType.RIGHT, 1, 1
        )

        self.grid.attach_next_to(
            self.power_pfl, self.wifi_toggle, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.hyprsunset, self.bluetooth_toggle, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.hypridle, self.power_pfl, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.notification_btn, self.hypridle, Gtk.PositionType.RIGHT, 1, 1
        )

        self.wifi_toggle.connect("reveal-clicked", self.set_active_submenu)
        self.bluetooth_toggle.connect("reveal-clicked", self.set_active_submenu)
        self.power_pfl.connect("reveal-clicked", self.set_active_submenu)
        self.hyprsunset.connect("reveal-clicked", self.set_active_submenu)

        self.children = (
            self.grid,
            self.wifi_toggle.submenu,
            self.bluetooth_toggle.submenu,
            self.power_pfl.submenu,
            self.hyprsunset.submenu,
        )

        self.connect("unmap", self.close_all_submenus)

    def set_active_submenu(self, btn: QSChevronButton):
        if btn.submenu != self.active_submenu and self.active_submenu is not None:
            self.active_submenu._reveal(False)

        self.active_submenu = btn.submenu
        self.active_submenu.toggle_reveal() if self.active_submenu else None


class QuickSettingsMenu(Box):
    """A menu to display the quick settings information."""

    def __init__(self, config: dict, popup, **kwargs):
        super().__init__(
            name="quicksettings-menu", orientation="v", all_visible=True, **kwargs
        )

        self.config = config
        self.popup = popup

        user_config = self.config.get("user", {})
        shortcuts_config = self.config.get("shortcuts", {})
        controls_config = self.config.get("controls", {})

        raw_avatar_path = user_config.get("avatar", "$HOME/.face")
        avatar_path = os.path.expanduser(os.path.expandvars(raw_avatar_path))
        default_image = f"{ASSETS_DIR}/images/banner.jpg"
        user_image = avatar_path if os.path.exists(avatar_path) else default_image
        if user_image == default_image:
            logger.warning(f"Avatar not found: {avatar_path}")

        username = user_config.get("name", "system")
        username_label = GLib.get_user_name() if username == "system" else username

        if user_config.get("distro_icon", True):
            username_label = f"{helpers.get_distro_icon()} {username_label}"

        username_label = Label(
            label=username_label,
            v_align="center",
            h_align="start",
            style_classes=["user"],
        )

        uptime_label = Label(
            label=f"{get_text_icon('hourglass')} {helpers.uptime()}",
            style_classes=["uptime"],
            v_align="center",
            h_align="start",
            tooltip_text="System Uptime",
        )

        self.user_box = Grid(
            column_spacing=10,
            name="user-box-grid",
            h_expand=True,
        )

        avatar = CircularImage(
            image_file=user_image,
            size=65,
        )

        avatar.set_size_request(65, 65)

        self.user_box.attach(
            avatar,
            0,
            0,
            2,
            2,
        )

        button_box = Box(
            orientation="h",
            h_align="start",
            v_align="center",
            name="button-box",
            h_expand=True,
            v_expand=True,
        )

        button_box.pack_end(
            Box(
                orientation="h",
                children=(
                    HoverButton(
                        child=nerd_font_icon(
                            icon=get_text_icon("power_menu.reboot"),
                            props={"style_classes": ["panel-font-icon"]},
                        ),
                        v_align="center",
                        on_clicked=lambda *_: self.show_dialog(
                            title="reboot",
                            body="Do you really want to reboot?",
                            command="reboot",
                        ),
                    ),
                    HoverButton(
                        child=nerd_font_icon(
                            icon=get_text_icon("power_menu.shutdown"),
                            props={"style_classes": ["panel-font-icon"]},
                        ),
                        v_align="center",
                        on_clicked=lambda *_: self.show_dialog(
                            title="shutdown",
                            body="Do you really want to shutdown?",
                            command="shutdown",
                        ),
                    ),
                ),
            ),
            False,
            False,
            0,
        )

        self.user_box.attach_next_to(
            username_label, avatar, Gtk.PositionType.RIGHT, 1, 1
        )

        self.user_box.attach_next_to(
            uptime_label, username_label, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.user_box.attach_next_to(
            button_box,
            username_label,
            Gtk.PositionType.RIGHT,
            4,
            4,
        )

        # Create sliders grid
        sliders_grid = Grid(
            row_spacing=10,
            v_align="center",
            h_expand=True,
            v_expand=True,
        )

        # Create center box with sliders and shortcuts if configured
        center_box = Box(
            orientation="h", spacing=10, style_classes=["section-box"], h_expand=True
        )

        main_grid = Grid(
            column_spacing=10,
            h_expand=True,
        )
        center_box.add(main_grid)

        # Set up grid columns
        for i in range(3):
            main_grid.insert_column(i)

        # Determine slider box class based on number of shortcuts
        shortcuts_enabled = shortcuts_config.get("enabled", False)
        shortcuts_items = shortcuts_config.get("items", [])
        if shortcuts_enabled:
            num_shortcuts = len(shortcuts_items)
            if 2 < num_shortcuts <= 4:
                slider_class = "slider-box-shorter"
            elif 0 < num_shortcuts <= 2:
                slider_class = "slider-box-short"
            else:
                slider_class = "slider-box-long"
        else:
            slider_class = "slider-box-long"

        sliders_box = Box(
            orientation="v",
            spacing=10,
            style_classes=[slider_class],
            children=(sliders_grid,),
            h_expand=True,
        )

        slider_factory = {
            "brightness": lambda: __import__(
                "widgets.quick_settings.sliders.brightness",
                fromlist=["BrightnessSlider"],
            ).BrightnessSlider(),
            "volume": lambda: __import__(
                "widgets.quick_settings.sliders.audio",
                fromlist=["AudioSlider"],
            ).AudioSlider(),
        }

        for index, slider in enumerate(controls_config.get("sliders", [])):
            factory = slider_factory.get(slider)
            if factory:
                sliders_grid.attach(factory(), 0, index, 1, 1)

        if shortcuts_enabled:
            shortcuts_box = Box(
                orientation="v",
                spacing=10,
                style_classes=["section-box", "shortcuts-box"],
                children=(
                    ShortcutsContainer(
                        shortcuts_config=shortcuts_items,
                        style_classes=["shortcuts-grid"],
                        v_align="start",
                        h_align="fill",
                    ),
                ),
                h_expand=False,
                v_expand=True,
            )

            main_grid.attach(sliders_box, 0, 0, 2, 1)
            main_grid.attach(shortcuts_box, 2, 0, 1, 1)
        else:
            main_grid.attach(sliders_box, 0, 0, 3, 1)

        # Create main layout box
        box = CenterBox(
            orientation="v",
            style_classes=["quick-settings-box"],
            start_children=Box(
                orientation="v",
                spacing=10,
                v_align="center",
                style_classes=["section-box"],
                children=(self.user_box, QuickSettingsButtonBox(popup=popup)),
            ),
            center_children=center_box,
        )

        if self.config.get("media", {}).get("enabled", False):
            box.end_children = (
                Box(
                    orientation="v",
                    spacing=10,
                    style_classes=["section-box"],
                    children=(
                        PlayerBoxStack(
                            MprisPlayerManager(), config=self.config.get("media", {})
                        ),
                    ),
                ),
            )

        self.add(box)

        invoke_repeater(
            1000,
            lambda *_: uptime_label.set_label(f" {helpers.uptime()}"),
        )

    def show_dialog(self, title: str, body: str, command: str):
        """Show a dialog with the given title and body."""
        self.get_parent().set_visible(False)
        self.popup.hide_popover()

        Dialog().add_content(
            title=title,
            body=body,
            command=command,
        ).toggle_popup()


class QuickSettingsButtonWidget(ButtonWidget, PopoverMixin):
    """A button to display the date and time."""

    def __init__(self, **kwargs):
        super().__init__(name="quick_settings", **kwargs)

        self._timeout_id = None
        self._active_wifi = None
        self._wifi_changed_handler_id = None
        self._active_speaker = None
        self._speaker_volume_handler_id = None
        self.panel_icon_size = 16

        self.audio_service = audio_service

        self.network_service = NetworkService()

        self.brightness_service = BrightnessService()

        self.brightness_service.connect("brightness_changed", self.update_brightness)

        self.network_service.connect("device-ready", self._get_network_icon)

        self.popup = None

        self.audio_icon = nerd_font_icon(
            icon=get_text_icon("volume.medium"),
            props={"style_classes": ["panel-font-icon"]},
        )

        self.network_icon = nerd_font_icon(
            icon=get_text_icon("wifi.connected"),
            props={"style_classes": ["panel-font-icon"]},
        )

        self.brightness_icon = nerd_font_icon(
            icon=get_text_icon("brightness.medium"),
            props={"style_classes": ["panel-font-icon"]},
        )

        self.update_brightness()

        self.children = Box(
            children=(
                self.network_icon,
                self.audio_icon,
                self.brightness_icon,
            )
        )

        bulk_connect(
            self.audio_service,
            {
                "notify::speaker": self.on_speaker_changed,
                "changed": self.check_mute,
            },
        )

        self.setup_popover(
            lambda: QuickSettingsMenu(config=self.config, popup=self._popup),
            connect_clicked=True,
            on_close_callback=lambda *_: self.remove_style_class("active"),
        )

    def _get_network_icon(self, *_):
        # Check if the network service is ready
        if self.network_service.primary_device == "wifi":
            wifi = self.network_service.wifi_device
            if wifi:
                self.network_icon.set_label(
                    network_icon_to_text_icons.get(
                        wifi.get_property("icon-name"),
                        get_text_icon("wifi.generic"),
                    ),
                )
                if (
                    self._active_wifi
                    and self._wifi_changed_handler_id is not None
                    and self._active_wifi != wifi
                ):
                    safe_disconnect(self._active_wifi, self._wifi_changed_handler_id)
                    self._wifi_changed_handler_id = None

                if self._wifi_changed_handler_id is None:
                    self._wifi_changed_handler_id = wifi.connect(
                        "changed", self.update_wifi_status
                    )
                    self._active_wifi = wifi
        else:
            ethernet = self.network_service.ethernet_device
            if self._active_wifi and self._wifi_changed_handler_id is not None:
                safe_disconnect(self._active_wifi, self._wifi_changed_handler_id)
                self._wifi_changed_handler_id = None
                self._active_wifi = None
            if ethernet:
                self.network_icon.set_label(
                    get_text_icon("ethernet"),
                )

    def update_wifi_status(self, wifi: Wifi):
        self.network_icon.set_label(
            network_icon_to_text_icons.get(
                wifi.get_property("icon-name"),
                get_text_icon("wifi.generic"),
            )
        )

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        speaker = self.audio_service.speaker
        if not speaker:
            return

        if (
            self._active_speaker
            and self._speaker_volume_handler_id is not None
            and self._active_speaker != speaker
        ):
            safe_disconnect(self._active_speaker, self._speaker_volume_handler_id)
            self._speaker_volume_handler_id = None

        if self._speaker_volume_handler_id is None:
            self._speaker_volume_handler_id = speaker.connect(
                "notify::volume", self.update_volume
            )
            self._active_speaker = speaker

        self.update_volume()

    def check_mute(self, *_):
        if not self.audio_service.speaker:
            return
        self.audio_icon.set_label(
            get_audio_icon_name(
                self.audio_service.speaker.volume, self.audio_service.speaker.muted
            )["icon_text"]
        )

    def update_volume(self, *_):
        if self.audio_service.speaker:
            volume = round(self.audio_service.speaker.volume)

            self.audio_icon.set_label(
                get_audio_icon_name(volume, self.audio_service.speaker.muted)[
                    "icon_text"
                ]
            )

    def update_brightness(self, *_):
        """Update the brightness icon."""
        try:
            normalized_brightness = self.brightness_service.screen_brightness_percentage
            icon_info = get_brightness_icon_name(normalized_brightness)["icon_text"]
            if icon_info:
                self.brightness_icon.set_label(
                    icon_info,
                )
            else:
                # Fallback icon if something goes wrong
                self.brightness_icon.set_label(get_text_icon("brightness.medium"))
        except Exception as e:
            logger.exception(f"Error updating brightness icon: {e}")
            # Fallback icon if something goes wrong
            self.brightness_icon.set_label(get_text_icon("brightness.medium"))

    def destroy(self):
        if self._active_wifi and self._wifi_changed_handler_id is not None:
            safe_disconnect(self._active_wifi, self._wifi_changed_handler_id)
            self._wifi_changed_handler_id = None
        self._active_wifi = None

        if self._active_speaker and self._speaker_volume_handler_id is not None:
            safe_disconnect(self._active_speaker, self._speaker_volume_handler_id)
            self._speaker_volume_handler_id = None
        self._active_speaker = None

        return super().destroy()
