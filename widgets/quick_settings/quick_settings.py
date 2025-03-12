import os

from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import Gtk

import utils.functions as helpers
from services import audio_service, network_service
from services.brightness import Brightness
from services.mpris import MprisPlayerManager
from shared.circle_image import CircleImage
from shared.dialog import Dialog
from shared.pop_over import PopOverWindow
from shared.submenu import QuickSubToggle
from shared.widget_container import ButtonWidget, HoverButton
from utils.widget_settings import BarConfig
from utils.widget_utils import (
    get_audio_icon_name,
    get_brightness_icon_name,
    util_fabricator,
)
from widgets.media import PlayerBoxStack
from widgets.quick_settings.shortcuts import ShortcutsContainer
from widgets.quick_settings.togglers import (
    HyprIdleQuickSetting,
    HyprSunsetQuickSetting,
    NotificationQuickSetting,
)

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


class DialogBox(Gtk.Dialog):
    """A dialog box to display additional information."""

    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_size_request(20, 20)

        label = Gtk.Label(label="This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


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

    def set_active_submenu(self, btn: QuickSubToggle):
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

        username_label = Label(
            label="User", v_align="center", h_align="start", style_classes="user"
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
            size=70,
        )

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
                        image=Image(icon_name="system-restart-symbolic", icon_size=16),
                        v_align="center",
                        on_clicked=lambda *_: (
                            self.get_parent().set_visible(False),
                            Dialog(
                                "restart", "Do you really want to restart?"
                            ).toggle_popup(),
                        ),
                    ),
                    HoverButton(
                        image=Image(icon_name="system-shutdown-symbolic", icon_size=16),
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
            hexpand=True,
            vexpand=True,
        )

        # Add audio submenu
        self.audio_submenu = AudioSubMenu()

        # Add sliders to the grid in a single column
        sliders_grid.attach(BrightnessSlider(), 0, 0, 1, 1)
        sliders_grid.attach(AudioSlider(), 0, 1, 1, 1)
        sliders_grid.attach(MicrophoneSlider(), 0, 2, 1, 1)

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
            children=(sliders_grid, self.audio_submenu),
            h_expand=True,
        )

        if self.config.get("shortcuts"):
            shortcuts_box = Box(
                orientation="v",
                spacing=10,
                style_classes=["section-box", "shortcuts-box"],
                children=(
                    ShortcutsContainer(
                        shortcuts_config=self.config["shortcuts"],
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
            end_children=(
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
            ),
        )

        self.add(box)

        util_fabricator.connect(
            "changed",
            lambda _, value: (
                username_label.set_label(
                    f"{helpers.get_distro_icon()} {value.get('user')}"
                ),
                uptime_label.set_label(f" {value.get('uptime')}"),
            ),
        )


class QuickSettingsButtonWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="quick-settings-button", **kwargs)

        self.config = widget_config["quick_settings"]
        self.panel_icon_size = 16
        self.audio = audio_service

        self.network = network_service

        self.brightness_service = Brightness().get_default()

        self.audio.connect("notify::speaker", self.on_speaker_changed)
        self.brightness_service.connect("screen", self.on_brightness_changed)

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(QuickSettingsMenu(config=self.config),),
            visible=False,
            all_visible=False,
            margin="-18px 0 0 0",
        )

        self.audio_icon = Image(style_classes="panel-icon")

        self.network_icon = Image(
            style_classes="panel-icon",
        )

        self.brightness_icon = Image(
            style_classes="panel-icon",
        )

        self.update_brightness()

        popup.set_pointing_to(self)

        self.children = Box(
            children=(
                self.network_icon,
                self.audio_icon,
                self.brightness_icon,
            )
        )
        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )

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
                        "network-offline-symbolic",
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
                        "network-offline-symbolic",
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
            normalized_brightness = int(
                (
                    self.brightness_service.screen_brightness
                    / self.brightness_service.max_screen
                )
                * 100
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
                    "display-brightness-symbolic",
                    self.panel_icon_size,
                )
        except Exception as e:
            print(f"Error updating brightness icon: {e}")
            # Fallback icon if something goes wrong
            self.brightness_icon.set_from_icon_name(
                "display-brightness-symbolic",
                self.panel_icon_size,
            )
