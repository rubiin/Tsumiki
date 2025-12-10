import importlib

from fabric import Application
from fabric.utils import exec_shell_command_async, logger
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GLib

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

    def __bool__(self) -> bool:
        """Return True if there are any widget paths defined."""
        return bool(self._paths)

    def __len__(self) -> int:
        """Return the number of widget paths defined."""
        return len(self._paths)

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
    "settings": "widgets.settings.SettingsWidget",
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

        # Auto-hide configuration
        self._auto_hide = bar_config.get("auto_hide", False)
        self._auto_hide_timeout = bar_config.get("auto_hide_timeout", 3000)
        self._hide_timer_id = None
        self._is_hovered = False

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
        location = bar_config.get("location", "top")

        # Only use revealer/eventbox if auto-hide is enabled
        if self._auto_hide:
            # Determine transition type based on bar location
            transition_type = "slide-down" if location == "top" else "slide-up"

            # Create revealer for auto-hide functionality
            self.revealer = Revealer(
                child=self.box,
                transition_type=transition_type,
                transition_duration=300,
                reveal_child=True,
            )

            # Create a hover zone that remains visible even when bar is hidden
            # This allows the user to hover at the edge to reveal the bar
            hover_zone = Box(style="min-height: 5px;")

            # Stack the revealer and hover zone
            if location == "top":
                container = Box(
                    orientation="v",
                    children=[self.revealer, hover_zone],
                )
            else:
                container = Box(
                    orientation="v",
                    children=[hover_zone, self.revealer],
                )

            # Wrap in event box to detect mouse hover
            child = EventBox(
                events=["enter-notify", "leave-notify"],
                child=container,
                on_enter_notify_event=self._on_enter_notify,
                on_leave_notify_event=self._on_leave_notify,
            )
        else:
            self.revealer = None
            child = self.box

        super().__init__(
            name="panel",
            layer=bar_config.get("layer", "overlay"),
            anchor=anchor,
            pass_through=False,
            exclusivity="auto",
            visible=True,
            all_visible=False,
            child=child,
            **kwargs,
        )

        # Start auto-hide timer if enabled
        if self._auto_hide:
            self._start_hide_timer()

        if options["check_updates"]:
            exec_shell_command_async(
                f"{ASSETS_DIR}/scripts/barupdate.sh",
                lambda _: None,
            )

    def _on_enter_notify(self, *_):
        """Handle mouse entering the bar area."""
        self._is_hovered = True
        self._cancel_hide_timer()
        self.revealer.set_reveal_child(True)
        return False

    def _on_leave_notify(self, *_):
        """Handle mouse leaving the bar area."""
        self._is_hovered = False
        if self._auto_hide:
            self._start_hide_timer()
        return False

    def _start_hide_timer(self):
        """Start the timer to hide the bar after inactivity."""
        self._cancel_hide_timer()
        self._hide_timer_id = GLib.timeout_add(self._auto_hide_timeout, self._hide_bar)

    def _cancel_hide_timer(self):
        """Cancel any pending hide timer."""
        if self._hide_timer_id is not None:
            GLib.source_remove(self._hide_timer_id)
            self._hide_timer_id = None

    def _hide_bar(self):
        """Hide the bar if not hovered."""
        if not self._is_hovered:
            self.revealer.set_reveal_child(False)
        self._hide_timer_id = None
        return False  # Don't repeat the timeout

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
                logger.exception("Error removing old bar during hotplug handling")

        # Create new
        bars.clear()
        new_bars = StatusBar._create_multi_monitor_bars(config)
        bars.extend(new_bars)

        for bar in bars:
            app.add_window(bar)
