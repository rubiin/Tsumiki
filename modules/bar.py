from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
    invoke_repeater,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow

from shared.module_group import ModuleGroup
from utils.config import widget_config
from utils.functions import convert_seconds_to_milliseconds
from utils.monitors import HyprlandWithMonitors
from widgets import (
    BatteryWidget,
    BlueToothWidget,
    BrightnessWidget,
    CavaWidget,
    ClickCounterWidget,
    CpuWidget,
    DateTimeWidget,
    DividerWidget,
    HyprIdleWidget,
    HyprSunsetWidget,
    KeyboardLayoutWidget,
    LanguageWidget,
    MemoryWidget,
    MicrophoneIndicatorWidget,
    Mpris,
    NetworkUsageWidget,
    OverviewWidget,
    PowerWidget,
    QuickSettingsButtonWidget,
    RecorderWidget,
    SpacingWidget,
    StopWatchWidget,
    StorageWidget,
    SubMapWidget,
    SystemTrayWidget,
    TaskBarWidget,
    ThemeSwitcherWidget,
    UpdatesWidget,
    VolumeWidget,
    WeatherWidget,
    WindowTitleWidget,
    WorkSpacesWidget,
)


class StatusBar(WaylandWindow):
    """A widget to display the status bar panel."""

    def check_for_bar_updates(self):
        exec_shell_command_async(
            get_relative_path("../assets/scripts/barupdate.sh"),
            lambda _: None,
        )
        return True

    def __init__(self, **kwargs):
        self.widgets_list = {
            "battery": BatteryWidget,
            "bluetooth": BlueToothWidget,
            "brightness": BrightnessWidget,
            "cava": CavaWidget,
            "click_counter": ClickCounterWidget,
            "cpu": CpuWidget,
            "date_time": DateTimeWidget,
            "hypr_idle": HyprIdleWidget,
            "hypr_sunset": HyprSunsetWidget,
            "keyboard": KeyboardLayoutWidget,
            "language": LanguageWidget,
            "memory": MemoryWidget,
            "microphone": MicrophoneIndicatorWidget,
            "mpris": Mpris,
            "network_usage": NetworkUsageWidget,
            "overview": OverviewWidget,
            "power": PowerWidget,
            "recorder": RecorderWidget,
            "storage": StorageWidget,
            "system_tray": SystemTrayWidget,
            "task_bar": TaskBarWidget,
            "theme_switcher": ThemeSwitcherWidget,
            "updates": UpdatesWidget,
            "volume": VolumeWidget,
            "submap": SubMapWidget,
            "weather": WeatherWidget,
            "window_title": WindowTitleWidget,
            "workspaces": WorkSpacesWidget,
            "spacing": SpacingWidget,
            "stop_watch": StopWatchWidget,
            "divider": DividerWidget,
            "quick_settings": QuickSettingsButtonWidget,
        }

        layout = self.make_layout()

        options = widget_config["general"]

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

        anchor = f"left {options['location']} right"
        super().__init__(
            name="panel",
            layer=options["layer"],
            anchor=anchor,
            pass_through=False,
            monitor=HyprlandWithMonitors().get_current_gdk_monitor_id(),
            exclusivity="auto",
            visible=True,
            all_visible=False,
            child=self.box,
            **kwargs,
        )

        if options["bar_style"] and options["bar_style"] != "default":
            self.box.add_style_class("floating-bar")

        if options["check_updates"]:
            invoke_repeater(
                convert_seconds_to_milliseconds(3600),
                self.check_for_bar_updates,
                initial_call=True,
            )

    def make_layout(self):
        """assigns the three sections their respective widgets"""

        layout = {"left_section": [], "middle_section": [], "right_section": []}

        for key in layout:
            for widget_name in widget_config["layout"][key]:
                if widget_name.startswith("@group:"):
                    # Handle module groups - using index-based lookup
                    group_name = widget_name.replace("@group:", "", 1)
                    group_config = None

                    if group_name.isdigit():
                        idx = int(group_name)
                        groups = widget_config.get("module_groups", [])
                        if isinstance(groups, list) and 0 <= idx < len(groups):
                            group_config = groups[idx]

                    if group_config:
                        group = ModuleGroup.from_config(
                            group_config,
                            self.widgets_list,
                            bar=self,
                            widget_config=widget_config
                        )
                        layout[key].append(group)
                else:
                    # Handle regular widgets
                    if widget_name in self.widgets_list:
                        widget_class = self.widgets_list[widget_name]
                        layout[key].append(
                            widget_class(widget_config, bar=self)
                        )

        return layout
