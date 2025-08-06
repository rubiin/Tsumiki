from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from shared.collapsible_group import CollapsibleGroupWidget
from shared.custom_button import CustomButtonWidget
from shared.widget_container import WidgetGroup
from widgets.battery import BatteryWidget
from widgets.bluetooth import BlueToothWidget
from widgets.brightness import BrightnessWidget
from widgets.cava import CavaWidget
from widgets.click_counter import ClickCounterWidget
from widgets.cliphist import ClipHistoryWidget
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
from widgets.wallpaper import WallpaperWidget
from widgets.weather import WeatherWidget
from widgets.window_count import WindowCountWidget
from widgets.window_title import WindowTitleWidget
from widgets.workspaces import WorkSpacesWidget
from widgets.world_clock import WorldClockWidget


class StatusBar(Window):
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
            "wallpaper": WallpaperWidget,
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

        anchor = f"left {bar_config.get('location', 'center')} right"

        super().__init__(
            name="panel",
            layer=bar_config.get("layer", "overlay"),
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
                    group_config = self._get_group_config(
                        widget_name, "widget_groups", config
                    )
                    if group_config:
                        group = WidgetGroup.from_config(
                            group_config,
                            self.widgets_list,
                        )
                        layout[key].append(group)
                elif widget_name.startswith("@collapsible:"):
                    # Handle collapsible groups
                    group_config = self._get_group_config(
                        widget_name, "collapsible_groups", config
                    )
                    if group_config:
                        collapsible_group = CollapsibleGroupWidget()

                        # Configure the collapsible group using the new method
                        collapsible_group.update_config(group_config)
                        collapsible_group.widgets_config = group_config.get(
                            "widgets", []
                        )
                        # Set widgets list for lazy initialization
                        collapsible_group.set_widgets(self.widgets_list)
                        # Add button to layout
                        layout[key].append(collapsible_group)
                elif widget_name.startswith("@custom_button:"):
                    # Handle individual custom buttons
                    button_index_str = widget_name.replace("@custom_button:", "", 1)
                    if button_index_str.isdigit():
                        button_index = int(button_index_str)
                        # Get buttons from custom_button_group config
                        custom_button_config = config.get("widgets", {}).get(
                            "custom_button_group", {}
                        )
                        buttons = custom_button_config.get("buttons", [])

                        if 0 <= button_index < len(buttons):
                            button_config = buttons[button_index]

                            # Create individual button
                            button = CustomButtonWidget(
                                widget_name=f"custom_button_{button_index}",
                                config=button_config,
                            )
                            layout[key].append(button)
                else:
                    # Handle regular widgets
                    if widget_name in self.widgets_list:
                        widget_class = self.widgets_list[widget_name]
                        layout[key].append(widget_class())

        return layout

    def _get_group_config(self, widget_name, config_key, config):
        """Helper method to extract group configuration by index.

        Args:
            widget_name: The full widget name (e.g., "@group:0" or "@collapsible:1")
            config_key: The config key to look up ("widget_groups" or
                        "collapsible_groups")
            config: The configuration dictionary to look up groups from

        Returns:
            The group configuration dict if found, None otherwise
        """
        # Extract group index from widget name
        if config_key == "widget_groups":
            group_idx = widget_name.replace("@group:", "", 1)
        else:  # collapsible_groups
            group_idx = widget_name.replace("@collapsible:", "", 1)

        if not group_idx.isdigit():
            return None

        idx = int(group_idx)
        groups = config.get(config_key, [])

        if isinstance(groups, list) and 0 <= idx < len(groups):
            return groups[idx]

        return None
