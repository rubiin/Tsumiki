import os

from fabric.utils import bulk_connect, get_relative_path, invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.grid import Grid
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import GLib, Gtk
from loguru import logger

import utils.functions as helpers
from services import (
    audio_service,
)
from services.brightness import BrightnessService
from services.mpris import MprisPlayerManager
from services.network import NetworkService, Wifi
from shared.buttons import HoverButton, QSChevronButton
from shared.circle_image import CircleImage
from shared.dialog import Dialog
from shared.popover import Popover
from shared.widget_container import ButtonWidget
from utils.icons import symbolic_icons
from utils.widget_utils import (
    get_audio_icon_name,
    get_brightness_icon_name,
)
from widgets.quick_settings.submenu.hyprsunset import (
    HyprSunsetSubMenu,
    HyprSunsetToggle,
)

from ..media import PlayerBoxStack
from .shortcuts import ShortcutsContainer
from .submenu.bluetooth import BluetoothSubMenu, BluetoothToggle
from .submenu.power import PowerProfileSubMenu, PowerProfileToggle
from .submenu.wifi import WifiSubMenu, WifiToggle
from .togglers import (
    HyprIdleQuickSetting,
    NotificationQuickSetting,
)


class QuickSettingsButtonBox(Box):
    """A box to display the quick settings buttons."""

    def __init__(self, **kwargs):
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

        self.power_pfl = PowerProfileToggle(submenu=PowerProfileSubMenu())

        self.hyprsunset = HyprSunsetToggle(submenu=HyprSunsetSubMenu())
        self.hypridle = HyprIdleQuickSetting()
        self.notification_btn = NotificationQuickSetting()

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

        self.add(self.grid)
        self.add(self.wifi_toggle.submenu)
        self.add(self.bluetooth_toggle.submenu)
        self.add(self.power_pfl.submenu)
        self.add(self.hyprsunset.submenu)

    def set_active_submenu(self, btn: QSChevronButton):
        if btn.submenu != self.active_submenu and self.active_submenu is not None:
            self.active_submenu.do_reveal(False)

        self.active_submenu = btn.submenu
        self.active_submenu.toggle_reveal() if self.active_submenu else None


class QuickSettingsMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, config, **kwargs):
        super().__init__(
            name="quicksettings-menu", orientation="v", all_visible=True, **kwargs
        )

        self.config = config

        user_image = (
            get_relative_path("../../assets/images/banner.jpg")
            if not os.path.exists(os.path.expandvars("$HOME/.face"))
            else os.path.expandvars("$HOME/.face")
        )

        username = (
            GLib.get_user_name()
            if self.config["user"]["name"] == "system"
            else self.config["user"]["name"]
        )

        if self.config["user"]["distro_icon"]:
            username = f"{helpers.get_distro_icon()} {username}"

        username_label = Label(
            label=username, v_align="center", h_align="start", style_classes="user"
        )

        uptime_label = Label(
            label=helpers.uptime(),
            style_classes="uptime",
            v_align="center",
            h_align="start",
        )

        self.user_box = Grid(
            column_spacing=10,
            name="user-box-grid",
            h_expand=True,
        )

        avatar = CircleImage(
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
                        image=Image(
                            icon_name=symbolic_icons["powermenu"]["reboot"],
                            icon_size=16,
                        ),
                        v_align="center",
                        on_clicked=lambda *_: self.show_dialog(
                            title="reboot",
                            body="Do you really want to reboot?",
                            command="reboot",
                        ),
                    ),
                    HoverButton(
                        image=Image(
                            icon_name=symbolic_icons["powermenu"]["shutdown"],
                            icon_size=16,
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
            column_spacing=10,
            column_homogeneous=True,
            row_homogeneous=False,
            v_align="center",
            h_expand=True,
            v_expand=True,
        )

        # TODO: check gtk_adjustment_set_value: assertion 'GTK_IS_ADJUSTMENT, microphone

        # TODO: add the submenu on slider add

        # Create center box with sliders and shortcuts if configured
        center_box = Box(
            orientation="h", spacing=10, style_classes="section-box", h_expand=True
        )

        main_grid = Grid(column_spacing=10, h_expand=True, column_homogeneous=False)
        center_box.add(main_grid)

        # Set up grid columns
        for i in range(3):
            main_grid.insert_column(i)

        # Determine slider box class based on number of shortcuts
        if self.config.get("shortcuts"):
            num_shortcuts = len(self.config["shortcuts"])
            if num_shortcuts > 2:
                slider_class = "slider-box-shorter"
            else:
                slider_class = "slider-box-short"
        else:
            slider_class = "slider-box-long"

        sliders_box = Box(
            orientation="v",
            spacing=10,
            style_classes=[slider_class],
            children=(sliders_grid),
            h_expand=True,
        )

        for index, slider in enumerate(self.config["controls"]["sliders"]):
            if slider == "brightness":
                from .sliders.brightness import BrightnessSlider

                sliders_grid.attach(
                    BrightnessSlider(),
                    0,
                    index,
                    1,
                    1,
                )
            elif slider == "volume":
                from .sliders.audio import AudioSlider

                sliders_grid.attach(
                    AudioSlider(),
                    0,
                    index,
                    1,
                    1,
                )

        if self.config.get("shortcuts")["enabled"]:
            shortcuts_box = Box(
                orientation="v",
                spacing=10,
                style_classes=["section-box", "shortcuts-box"],
                children=(
                    ShortcutsContainer(
                        shortcuts_config=self.config["shortcuts"]["items"],
                        style_classes="shortcuts-grid",
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
            style_classes="quick-settings-box",
            start_children=Box(
                orientation="v",
                spacing=10,
                v_align="center",
                style_classes="section-box",
                children=(self.user_box, QuickSettingsButtonBox()),
            ),
            center_children=center_box,
        )

        if self.config["media"]["enabled"]:
            box.end_children = (
                Box(
                    orientation="v",
                    spacing=10,
                    style_classes="section-box",
                    children=(
                        PlayerBoxStack(
                            MprisPlayerManager(), config=self.config["media"]
                        ),
                    ),
                ),
            )

        self.add(box)

        invoke_repeater(
            1000,
            lambda *_: uptime_label.set_label(helpers.uptime()),
        )

    def show_dialog(self, title, body, command):
        """Show a dialog with the given title and body."""
        self.get_parent().set_visible(False)

        Dialog().add_content(
            title=title,
            body=body,
            command=command,
        ).toggle_popup()


class QuickSettingsButtonWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, **kwargs):
        super().__init__(name="quick_settings", **kwargs)

        self._timeout_id = None
        self.panel_icon_size = 16

        self.audio_service = audio_service

        self.network_service = NetworkService()

        self.brightness_service = BrightnessService()

        bulk_connect(
            self.audio_service,
            {
                "notify::speaker": self.on_speaker_changed,
                "changed": self.check_mute,
            },
        )

        self.brightness_service.connect("brightness_changed", self.update_brightness)

        self.network_service.connect("device-ready", self._get_network_icon)

        self.popup = None

        self.audio_icon = Image(style_classes="panel-font-icon")

        self.network_icon = Image(
            style_classes="panel-font-icon",
        )

        self.brightness_icon = Image(
            style_classes="panel-font-icon",
        )

        self.update_brightness()

        self.children = Box(
            children=(
                self.network_icon,
                self.audio_icon,
                self.brightness_icon,
            )
        )

        self.connect(
            "clicked",
            self.show_popover,
        )

    def show_popover(self, *_):
        """Show the popover."""
        if self.popup is None:
            self.popup = Popover(
                content=QuickSettingsMenu(config=self.config),
                point_to=self,
            )
        self.popup.open()

    def _get_network_icon(self, *_):
        # Check if the network service is ready
        if self.network_service.primary_device == "wifi":
            wifi = self.network_service.wifi_device

            self.network_icon.set_from_icon_name(
                wifi.icon_name,
                self.panel_icon_size,
            )
            wifi.connect("changed", self.update_wifi_status)

        else:
            ethernet = self.network_service.ethernet_device
            self.network_icon.set_from_icon_name(
                ethernet.icon_name,
                self.panel_icon_size,
            )

    def update_wifi_status(self, wifi: Wifi):
        self.network_icon.set_from_icon_name(
            wifi.icon_name,
            self.panel_icon_size,
        )

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio_service.speaker:
            return

        self.audio_service.speaker.connect("notify::volume", self.update_volume)

    def check_mute(self, audio):
        if not self.audio_service.speaker:
            return
        self.audio_icon.set_from_icon_name(
            get_audio_icon_name(
                self.audio_service.speaker.volume, self.audio_service.speaker.muted
            )["icon"],
            self.panel_icon_size,
        )

    def update_volume(self, *_):
        if self.audio_service.speaker:
            volume = round(self.audio_service.speaker.volume)

            self.audio_icon.set_from_icon_name(
                get_audio_icon_name(volume, self.audio_service.speaker.muted)["icon"],
                self.panel_icon_size,
            )

    def update_brightness(self, *_):
        """Update the brightness icon."""
        try:
            normalized_brightness = self.brightness_service.screen_brightness_percentage
            icon_info = get_brightness_icon_name(normalized_brightness)["icon"]
            if icon_info:
                self.brightness_icon.set_from_icon_name(
                    icon_info,
                    self.panel_icon_size,
                )
            else:
                # Fallback icon if something goes wrong
                self.brightness_icon.set_from_icon_name(
                    symbolic_icons["brightness"]["indicator"],
                    self.panel_icon_size,
                )
        except Exception as e:
            logger.exception(f"Error updating brightness icon: {e}")
            # Fallback icon if something goes wrong
            self.brightness_icon.set_from_icon_name(
                symbolic_icons["brightness"]["indicator"],
                self.panel_icon_size,
            )
