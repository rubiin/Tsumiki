from fabric.utils import (
    exec_shell_command_async,
    get_relative_path,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from shared.collapsible_group import CollapsibleGroupWidget
from widgets.app_launcher_button import AppLauncherButton
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
            "app_launcher_button": AppLauncherButton,
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

        anchor = f"left {bar_config.get('location', 'top')} right"

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
        from utils.widget_factory import WidgetResolver

        layout = {"left_section": [], "middle_section": [], "right_section": []}

        # Create a single resolver for all widgets - now truly unified!
        resolver = WidgetResolver(self.widgets_list)
        context = {"config": config}

        for key in layout:
            for widget_name in config["layout"][key]:
                # Use unified widget resolver for ALL widget types
                widget = resolver.resolve_widget(widget_name, context)
                if widget:
                    layout[key].append(widget)

        return layout

    @staticmethod
    def create_bars(app, config):
        multi_monitor = config["general"].get("multi_monitor", False)
        bars = (
            StatusBar._create_multi_monitor_bars(config)
            if multi_monitor
            else [StatusBar(config)]
        )

        for bar in bars:
            app.add_window(bar)

        if multi_monitor:
            StatusBar._setup_hotplug(app, config, bars)

        return bars

    @staticmethod
    def _create_multi_monitor_bars(config):
        from utils.monitors import HyprlandWithMonitors

        monitor_util = HyprlandWithMonitors()
        monitor_names = monitor_util.get_monitor_names()

        if not monitor_names:
            return [StatusBar(config)]

        bars = []
        for monitor_name in monitor_names:
            monitor_id = monitor_util.get_gdk_monitor_id_from_name(monitor_name)
            if monitor_id is not None:
                bars.append(StatusBar(config, monitor=monitor_id))

        return bars if bars else [StatusBar(config)]

    @staticmethod
    def _setup_hotplug(app, config, bars):
        from utils.monitors import MonitorWatcher

        watcher = MonitorWatcher()

        def recreate():
            # Remove old
            for bar in bars:
                try:
                    app.remove_window(bar)
                    bar.destroy()
                except Exception:
                    pass

            # Create new
            bars.clear()
            new_bars = StatusBar._create_multi_monitor_bars(config)
            bars.extend(new_bars)

            for bar in bars:
                app.add_window(bar)

        watcher.add_callback(recreate)
        watcher.start_watching()
