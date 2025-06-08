from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from shared.widget_container import ToggleableWidget, WidgetGroup
from utils.monitors import HyprlandWithMonitors
from utils.widget_utils import lazy_load_widget


class StatusBar(Window, ToggleableWidget):
    """A widget to display the status bar panel."""

    def __init__(self, config, **kwargs):
        self.widgets_list = {
            "battery": "widgets.BatteryWidget",
            "bluetooth": "widgets.BlueToothWidget",
            "world_clock": "widgets.WorldClockWidget",
            "brightness": "widgets.BrightnessWidget",
            "cava": "widgets.CavaWidget",
            "cliphist": "widgets.ClipHistoryWidget",
            "kanban": "widgets.KanbanWidget",
            "emoji_picker": "widgets.EmojiPickerWidget",
            "click_counter": "widgets.ClickCounterWidget",
            "cpu": "widgets.CpuWidget",
            "date_time": "widgets.DateTimeWidget",
            "hypridle": "widgets.HyprIdleWidget",
            "hyprpicker": "widgets.HyprPickerWidget",
            "hyprsunset": "widgets.HyprSunsetWidget",
            "keyboard": "widgets.KeyboardLayoutWidget",
            "language": "widgets.LanguageWidget",
            "memory": "widgets.MemoryWidget",
            "microphone": "widgets.MicrophoneIndicatorWidget",
            "mpris": "widgets.MprisWidget",
            "network_usage": "widgets.NetworkUsageWidget",
            "ocr": "widgets.OCRWidget",
            "overview": "widgets.OverviewWidget",
            "power": "widgets.PowerWidget",
            "recorder": "widgets.RecorderWidget",
            "screenshot": "widgets.ScreenShotWidget",
            "storage": "widgets.StorageWidget",
            "system_tray": "widgets.SystemTrayWidget",
            "taskbar": "widgets.TaskBarWidget",
            "theme_switcher": "widgets.ThemeSwitcherWidget",
            "updates": "widgets.UpdatesWidget",
            "volume": "widgets.VolumeWidget",
            "submap": "widgets.SubMapWidget",
            "weather": "widgets.WeatherWidget",
            "window_title": "widgets.WindowTitleWidget",
            "workspaces": "widgets.WorkSpacesWidget",
            "spacing": "widgets.SpacingWidget",
            "stopwatch": "widgets.StopWatchWidget",
            "divider": "widgets.DividerWidget",
            "quick_settings": "widgets.QuickSettingsButtonWidget",
            "window_count": "widgets.WindowCountWidget",
        }

        options = config["general"]
        bar_config = config["modules"]["bar"]
        layout = self.make_layout(config)

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
            monitor=HyprlandWithMonitors().get_current_gdk_monitor_id(),
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
                else:
                    # Handle regular widgets
                    if widget_name in self.widgets_list:
                        widget_class = lazy_load_widget(widget_name, self.widgets_list)
                        layout[key].append(widget_class())

        return layout
