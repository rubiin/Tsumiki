import importlib

from fabric import Application
from fabric.utils import (
    exec_shell_command_async,
)
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from utils.constants import ASSETS_DIR
from utils.widget_settings import BarConfig


class LazyWidgetDict(dict):
    """A dictionary that lazily imports widget classes on first access.

    This speeds up startup by only importing widgets that are actually used
    in the user's layout configuration.
    """

    def __init__(self, widget_paths: dict[str, str]):
        super().__init__()
        self._paths = widget_paths
        self._cache = {}

    def __getitem__(self, key: str):
        # Return cached class if already imported
        if key in self._cache:
            return self._cache[key]

        # Check if we have a path for this widget
        if key not in self._paths:
            raise KeyError(f"Widget '{key}' not found")

        # Dynamically import the widget class
        class_path = self._paths[key]
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        widget_class = getattr(module, class_name)

        # Cache and return
        self._cache[key] = widget_class
        return widget_class

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: str) -> bool:
        return key in self._paths

    def keys(self):
        return self._paths.keys()

    def items(self):
        # For iteration, import all (used by WidgetGroup)
        for key in self._paths:
            yield key, self[key]


# Lazy widget loading - widgets are imported on-demand to speed up startup
# Format: "widget_name": "module.path.ClassName"
LAZY_WIDGETS_LIST = {
    "app_launcher_button": "widgets.app_launcher_button.AppLauncherButton",
    "battery": "widgets.battery.BatteryWidget",
    "bluetooth": "widgets.bluetooth.BlueToothWidget",
    "brightness": "widgets.brightness.BrightnessWidget",
    "cava": "widgets.cava.CavaWidget",
    "click_counter": "widgets.click_counter.ClickCounterWidget",
    "cliphist": "widgets.cliphist.ClipHistoryWidget",
    "collapsible_group": "shared.collapsible_group.CollapsibleGroupWidget",
    "cpu": "widgets.stats.CpuWidget",
    "custom_module": "widgets.custom_module.CustomModuleWidget",
    "date_time": "widgets.datetime_menu.DateTimeWidget",
    "divider": "widgets.utility_widgets.DividerWidget",
    "emoji_picker": "widgets.emoji_picker.EmojiPickerWidget",
    "gpu": "widgets.stats.GpuWidget",
    "hypridle": "widgets.hypridle.HyprIdleWidget",
    "hyprpicker": "widgets.hyprpicker.HyprPickerWidget",
    "hyprsunset": "widgets.hyprsunset.HyprSunsetWidget",
    "kanban": "widgets.kanban.KanbanWidget",
    "keyboard": "widgets.keyboard_layout.KeyboardLayoutWidget",
    "language": "widgets.language.LanguageWidget",
    "memory": "widgets.stats.MemoryWidget",
    "microphone": "widgets.microphone.MicrophoneIndicatorWidget",
    "mpris": "widgets.mpris.MprisWidget",
    "network_usage": "widgets.stats.NetworkUsageWidget",
    "ocr": "widgets.ocr.OCRWidget",
    "overview_button": "widgets.overview_button.OverviewButtonWidget",
    "power": "widgets.power_button.PowerWidget",
    "quick_settings": "widgets.quick_settings.quick_settings.QuickSettingsButtonWidget",
    "recorder": "widgets.recorder.RecorderWidget",
    "screenshot": "widgets.screenshot.ScreenShotWidget",
    "spacing": "widgets.utility_widgets.SpacingWidget",
    "stopwatch": "widgets.stopwatch.StopWatchWidget",
    "storage": "widgets.stats.StorageWidget",
    "submap": "widgets.submap.SubMapWidget",
    "system_tray": "widgets.system_tray.SystemTrayWidget",
    "taskbar": "widgets.taskbar.TaskBarWidget",
    "theme_switcher": "widgets.theme.ThemeSwitcherWidget",
    "updates": "widgets.updates.UpdatesWidget",
    "volume": "widgets.volume.VolumeWidget",
    "wallpaper": "widgets.wallpaper.WallpaperWidget",
    "weather": "widgets.weather.WeatherWidget",
    "window_count": "widgets.window_count.WindowCountWidget",
    "window_title": "widgets.window_title.WindowTitleWidget",
    "workspaces": "widgets.workspaces.WorkSpacesWidget",
    "world_clock": "widgets.world_clock.WorldClockWidget",
}


class StatusBar(Window):
    """A widget to display the status bar panel."""

    def __init__(self, config: BarConfig, **kwargs):
        # Use lazy widget loading - classes are imported on first use
        self.widgets_list = LazyWidgetDict(LAZY_WIDGETS_LIST)

        options = config.get("general", {})
        bar_config = config.get("modules", {}).get("bar", {})
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
                f"{ASSETS_DIR}/scripts/barupdate.sh",
                lambda _: None,
            )

    def make_layout(self, config: BarConfig):
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
    def create_bars(app: Application, config: BarConfig) -> list:
        multi_monitor = config.get("general", {}).get("multi_monitor", False)
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
    def _create_multi_monitor_bars(config: BarConfig):
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
    def _setup_hotplug(app: Application, config: BarConfig, bars: list):
        from utils.monitors import MonitorWatcher

        watcher = MonitorWatcher()

        watcher.add_callback(lambda: StatusBar._recreate_bars(app, config, bars))
        watcher.start_watching()

    @staticmethod
    def _recreate_bars(app: Application, config: BarConfig, bars: list):
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
