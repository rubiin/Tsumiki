from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from shared.widget_container import BaseWidget, WidgetGroup
from widgets.battery import BatteryWidget
from widgets.bluetooth import BlueToothWidget
from widgets.brightness import BrightnessWidget
from widgets.cava import CavaWidget
from widgets.click_counter import ClickCounterWidget
from widgets.cliphist import ClipHistoryWidget
from widgets.collapsible_group import CollapsibleGroupWidget
from widgets.datetime_menu import DateTimeWidget
from widgets.emoji_picker import EmojiPickerWidget
from widgets.hypridle import HyprIdleWidget
from widgets.hyprpicker import HyprPickerWidget
from widgets.hyprsunset import HyprSunsetWidget
from widgets.kanban import KanbanWidget
from widgets.keyboard_layout import KeyboardLayoutWidget
from widgets.language import LanguageWidget
from widgets.microphone import MicrophoneIndicatorWidget
from widgets.mpris import MprisWidget
from widgets.ocr import OCRWidget
from widgets.overview import OverviewWidget
from widgets.power_button import PowerWidget
from widgets.quick_settings.quick_settings import QuickSettingsButtonWidget
from widgets.recorder import RecorderWidget
from widgets.screenshot import ScreenShotWidget
from widgets.stats import (
    CpuWidget,
    GpuWidget,
    MemoryWidget,
    NetworkUsageWidget,
    StorageWidget,
)
from widgets.stopwatch import StopWatchWidget
from widgets.submap import SubMapWidget
from widgets.system_tray import SystemTrayWidget
from widgets.taskbar import TaskBarWidget
from widgets.theme import ThemeSwitcherWidget
from widgets.updates import UpdatesWidget
from widgets.utility_widgets import DividerWidget, SpacingWidget
from widgets.volume import VolumeWidget
from widgets.weather import WeatherWidget
from widgets.window_count import WindowCountWidget
from widgets.window_title import WindowTitleWidget
from widgets.workspaces import WorkSpacesWidget
from widgets.world_clock import WorldClockWidget


class StatusBar(Window, BaseWidget):
    """A widget to display the status bar panel."""

    def __init__(self, config, **kwargs):
        self.widgets_list = {
            "battery": BatteryWidget,
            "bluetooth": BlueToothWidget,
            "world_clock": WorldClockWidget,
            "brightness": BrightnessWidget,
            "cava": CavaWidget,
            "cliphist": ClipHistoryWidget,
            "gpu": GpuWidget,
            "kanban": KanbanWidget,
            "emoji_picker": EmojiPickerWidget,
            "click_counter": ClickCounterWidget,
            "cpu": CpuWidget,
            "date_time": DateTimeWidget,
            "hypridle": HyprIdleWidget,
            "hyprpicker": HyprPickerWidget,
            "hyprsunset": HyprSunsetWidget,
            "keyboard": KeyboardLayoutWidget,
            "language": LanguageWidget,
            "memory": MemoryWidget,
            "microphone": MicrophoneIndicatorWidget,
            "mpris": MprisWidget,
            "network_usage": NetworkUsageWidget,
            "ocr": OCRWidget,
            "overview": OverviewWidget,
            "power": PowerWidget,
            "recorder": RecorderWidget,
            "screenshot": ScreenShotWidget,
            "storage": StorageWidget,
            "system_tray": SystemTrayWidget,
            "taskbar": TaskBarWidget,
            "theme_switcher": ThemeSwitcherWidget,
            "updates": UpdatesWidget,
            "volume": VolumeWidget,
            "submap": SubMapWidget,
            "weather": WeatherWidget,
            "window_title": WindowTitleWidget,
            "workspaces": WorkSpacesWidget,
            "spacing": SpacingWidget,
            "stopwatch": StopWatchWidget,
            "divider": DividerWidget,
            "quick_settings": QuickSettingsButtonWidget,
            "window_count": WindowCountWidget,
            "collapsible_group": CollapsibleGroupWidget,
        }

        options = config["general"]
        bar_config = config["modules"]["bar"]
        layout = self.make_layout(config)

        # Main bar content (back to original CenterBox layout)
        self.box = CenterBox(
            name="panel-inner",
            start_children=Box(
                spacing=4,
                orientation="h",
                children=layout["left_section"],
            ),
            center_children=Box(
                spacing=4,
                orientation="h",
                children=layout["middle_section"],
            ),
            end_children=Box(
                spacing=4,
                orientation="h",
                children=layout["right_section"],
            ),
        )

        anchor = f"left {bar_config['location']} right"

        super().__init__(
            name="panel",
            layer=bar_config["layer"],
            anchor=anchor,
            pass_through=False,
            exclusivity="auto",
            visible=True,
            all_visible=False,
            child=self.box,
            **kwargs,
        )

        if options["check_updates"]:
            exec_shell_command_async(
                get_relative_path("../assets/scripts/barupdate.sh"),
                lambda _: None,
            )

    def make_layout(self, config):
        """assigns the three sections their respective widgets"""

        layout = {"left_section": [], "middle_section": [], "right_section": []}

        for key in layout:
            for widget_name in config["layout"][key]:
                if widget_name.startswith("@group:"):
                    # Handle widget groups - using index-based lookup
                    group_name = widget_name.replace("@group:", "", 1)
                    group_config = None

                    if group_name.isdigit():
                        idx = int(group_name)
                        groups = config.get("widget_groups", [])
                        if isinstance(groups, list) and 0 <= idx < len(groups):
                            group_config = groups[idx]

                    if group_config:
                        group = WidgetGroup.from_config(
                            group_config,
                            self.widgets_list,
                        )
                        layout[key].append(group)
                elif widget_name.startswith("@collapsible:"):
                    # Handle collapsible groups
                    group_name = widget_name.replace("@collapsible:", "", 1)
                    group_config = None

                    if group_name.isdigit():
                        idx = int(group_name)
                        groups = config.get("collapsible_groups", [])
                        if isinstance(groups, list) and 0 <= idx < len(groups):
                            group_config = groups[idx]

                    if group_config:
                        collapsible_group = CollapsibleGroupWidget()

                        # Configure the collapsible group
                        collapsible_group.config.update(group_config)
                        collapsible_group.widgets_config = group_config.get(
                            "widgets", []
                        )
                        # Set widgets list for lazy initialization
                        collapsible_group.set_widgets(self.widgets_list)

                        # Add button to layout
                        layout[key].append(collapsible_group)
                else:
                    # Handle regular widgets
                    if widget_name in self.widgets_list:
                        widget_class = self.widgets_list[widget_name]
                        layout[key].append(widget_class())

        return layout
