from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow

from shared import ModuleGroup
from utils import HyprlandWithMonitors
from utils.functions import run_in_thread
from utils.widget_utils import lazy_load_widget


class StatusBar(WaylandWindow):
    """A widget to display the status bar panel."""

    @run_in_thread
    def check_for_bar_updates(self):
        exec_shell_command_async(
            get_relative_path("../assets/scripts/barupdate.sh"),
            lambda _: None,
        )
        return True

    def __init__(self, config, **kwargs):
        self.widgets_list = {
            "battery": "widgets.BatteryWidget",
            "bluetooth": "widgets.BlueToothWidget",
            "brightness": "widgets.BrightnessWidget",
            "cava": "widgets.CavaWidget",
            "click_counter": "widgets.ClickCounterWidget",
            "cpu": "widgets.CpuWidget",
            "date_time": "widgets.DateTimeWidget",
            "hypr_idle": "widgets.HyprIdleWidget",
            "hypr_picker": "widgets.HyprPickerWidget",
            "hypr_sunset": "widgets.HyprSunsetWidget",
            "keyboard": "widgets.KeyboardLayoutWidget",
            "language": "widgets.LanguageWidget",
            "memory": "widgets.MemoryWidget",
            "microphone": "widgets.MicrophoneIndicatorWidget",
            "mpris": "widgets.Mpris",
            "network_usage": "widgets.NetworkUsageWidget",
            "ocr": "widgets.OCRWidget",
            "overview": "widgets.OverviewWidget",
            "power": "widgets.PowerWidget",
            "recorder": "widgets.RecorderWidget",
            "storage": "widgets.StorageWidget",
            "system_tray": "widgets.SystemTrayWidget",
            "task_bar": "widgets.TaskBarWidget",
            "theme_switcher": "widgets.ThemeSwitcherWidget",
            "updates": "widgets.UpdatesWidget",
            "volume": "widgets.VolumeWidget",
            "submap": "widgets.SubMapWidget",
            "weather": "widgets.WeatherWidget",
            "window_title": "widgets.WindowTitleWidget",
            "workspaces": "widgets.WorkSpacesWidget",
            "spacing": "widgets.SpacingWidget",
            "stop_watch": "widgets.StopWatchWidget",
            "divider": "widgets.DividerWidget",
            "quick_settings": "widgets.QuickSettingsButtonWidget",
        }

        options = config["general"]
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
            self.box.add_style_class(options["bar_style"])

        if options["check_updates"]:
            self.check_for_bar_updates()

    def make_layout(self, widget_config):
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
                            widget_config=widget_config,
                        )
                        layout[key].append(group)
                else:
                    # Handle regular widgets
                    if widget_name in self.widgets_list:
                        widget_class = lazy_load_widget(widget_name, self.widgets_list)
                        layout[key].append(widget_class(widget_config, bar=self))

        return layout
