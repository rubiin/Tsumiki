import os

from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import GLib, Gtk

import utils.functions as helpers
from services import Brightness, MprisPlayerManager, audio_service, network_service
from shared import (
    ButtonWidget,
    CircleImage,
    Dialog,
    HoverButton,
    Popover,
    QSChevronButton,
)
from utils import BarConfig
from utils.icons import icons
from utils.widget_utils import (
    get_audio_icon_name,
    get_brightness_icon_name,
    util_fabricator,
)

from ..media import PlayerBoxStack
from .shortcuts import ShortcutsContainer
from .sliders import AudioSlider, BrightnessSlider, MicrophoneSlider
from .submenu import (
    AudioSubMenu,
    BluetoothSubMenu,
    BluetoothToggle,
    PowerProfileSubMenu,
    PowerProfileToggle,
    WifiSubMenu,
    WifiToggle,
)
from .submenu.mic import MicroPhoneSubMenu
from .togglers import (
    HyprIdleQuickSetting,
    HyprSunsetQuickSetting,
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

        self.grid = Gtk.Grid(
            visible=True,
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

        self.hypr_idle = HyprIdleQuickSetting()
        self.hypr_sunset = HyprSunsetQuickSetting()
        self.notification_btn = NotificationQuickSetting()

        self.grid.attach(self.wifi_toggle, 1, 1, 1, 1)

        self.grid.attach_next_to(
            self.bluetooth_toggle, self.wifi_toggle, Gtk.PositionType.RIGHT, 1, 1
        )

        self.grid.attach_next_to(
            self.power_pfl, self.wifi_toggle, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.hypr_sunset, self.bluetooth_toggle, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.hypr_idle, self.power_pfl, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.grid.attach_next_to(
            self.notification_btn, self.hypr_idle, Gtk.PositionType.RIGHT, 1, 1
        )

        self.wifi_toggle.connect("reveal-clicked", self.set_active_submenu)
        self.bluetooth_toggle.connect("reveal-clicked", self.set_active_submenu)
        self.power_pfl.connect("reveal-clicked", self.set_active_submenu)

        self.add(self.grid)
        self.add(self.wifi_toggle.submenu)
        self.add(self.bluetooth_toggle.submenu)
        self.add(self.power_pfl.submenu)

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

        self.user_box = Gtk.Grid(
            column_spacing=10,
            name="user-box-grid",
            visible=True,
            hexpand=True,
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
                            icon_name=icons["powermenu"]["reboot"], icon_size=16
                        ),
                        v_align="center",
                        on_clicked=lambda *_: (
                            self.get_parent().set_visible(False),
                            Dialog(
                                "restart", "Do you really want to restart?"
                            ).toggle_popup(),
                        ),
                    ),
                    HoverButton(
                        image=Image(
                            icon_name=icons["powermenu"]["shutdown"], icon_size=16
                        ),
                        v_align="center",
                        on_clicked=lambda *_: (
                            self.get_parent().set_visible(False),
                            Dialog(
                                "shutdown", "Do you really want to shutdown?"
                            ).toggle_popup(),
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
        sliders_grid = Gtk.Grid(
            visible=True,
            row_spacing=10,
            column_spacing=10,
            column_homogeneous=True,
            row_homogeneous=False,
            valign="center",
            hexpand=True,
            vexpand=True,
        )

        # Add audio submenu
        self.audio_submenu = AudioSubMenu()
        self.mic_submenu = MicroPhoneSubMenu()

        # TODO: check gtk_adjustment_set_value: assertion 'GTK_IS_ADJUSTMENT, microphone

        # Create center box with sliders and shortcuts if configured
        center_box = Box(
            orientation="h", spacing=10, style_classes="section-box", h_expand=True
        )

        main_grid = Gtk.Grid(
            visible=True, column_spacing=10, hexpand=True, column_homogeneous=False
        )
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
            children=(sliders_grid, self.audio_submenu, self.mic_submenu),
            h_expand=True,
        )

        for index, slider in enumerate(self.config["controls"]["sliders"]):
            if slider == "brightness":
                sliders_grid.attach(
                    BrightnessSlider(),
                    0,
                    index,
                    1,
                    1,
                )
            elif slider == "volume":
                sliders_grid.attach(
                    AudioSlider(),
                    0,
                    index,
                    1,
                    1,
                )
            else:
                sliders_grid.attach(
                    MicrophoneSlider(),
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

        util_fabricator.connect(
            "changed",
            lambda _, value: (uptime_label.set_label(f" {value.get('uptime')}"),),
        )


class QuickSettingsButtonWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(
            widget_config["quick_settings"], name="quick_settings", **kwargs
        )

        self.panel_icon_size = 16
        self.audio = audio_service

        self._timeout_id = None

        self.network = network_service

        # Initialize the audio service
        self.brightness_service = Brightness()

        self.audio.connect("notify::speaker", self.on_speaker_changed)
        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

        popup = Popover(
            content_factory=lambda: QuickSettingsMenu(config=self.config),
            point_to=self,
        )

        self.audio_icon = Image(style_classes="panel-icon")

        self.network_icon = Image(
            style_classes="panel-icon",
        )

        self.brightness_icon = Image(
            style_classes="panel-icon",
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
            lambda *_: (popup.open()),
        )

    def start_timeout(self):
        self.stop_timeout()
        self._timeout_id = GLib.timeout_add(2000, self.close_notification)

    def stop_timeout(self):
        if self._timeout_id is not None:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None

        def get_network_icon(*_):
            if self.network.primary_device == "wifi":
                wifi = self.network.wifi_device

                if wifi:
                    self.network_icon.set_from_icon_name(
                        wifi.get_icon_name(),
                        self.panel_icon_size,
                    )
                else:
                    self.network_icon.set_from_icon_name(
                        icons["network"]["wifi"]["disconnected"],
                        self.panel_icon_size,
                    )

            else:
                ethernet = self.network.ethernet_device
                if ethernet:
                    self.network_icon.set_from_icon_name(
                        ethernet.get_icon_name(),
                        self.panel_icon_size,
                    )
                else:
                    self.network_icon.set_from_icon_name(
                        icons["network"]["wifi"]["disconnected"],
                        self.panel_icon_size,
                    )

        self.network.connect("notify::primary-device", get_network_icon)

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio.speaker:
            return

        self.audio.speaker.connect("notify::volume", self.update_volume)
        self.update_volume()

    def update_volume(self, *_):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)

            self.audio_icon.set_from_icon_name(
                get_audio_icon_name(volume, self.audio.speaker.muted)["icon"],
                self.panel_icon_size,
            )

    def on_brightness_changed(self, *_):
        self.update_brightness()

    def update_brightness(self, *_):
        """Update the brightness icon."""
        try:
            # Convert brightness to percentage (0-100)

            normalized_brightness = helpers.convert_to_percent(
                self.brightness_service.screen_brightness,
                self.brightness_service.max_screen,
            )

            icon_info = get_brightness_icon_name(normalized_brightness)
            if icon_info:
                self.brightness_icon.set_from_icon_name(
                    icon_info["icon"],
                    self.panel_icon_size,
                )
            else:
                # Fallback icon if something goes wrong
                self.brightness_icon.set_from_icon_name(
                    icons["brightness"]["indicator"],
                    self.panel_icon_size,
                )
        except Exception as e:
            print(f"Error updating brightness icon: {e}")
            # Fallback icon if something goes wrong
            self.brightness_icon.set_from_icon_name(
                icons["brightness"]["indicator"],
                self.panel_icon_size,
            )
