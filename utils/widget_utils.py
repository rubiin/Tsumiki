import contextlib
import importlib
from numbers import Number
from time import sleep
from typing import Literal

import psutil
from fabric.utils import Gdk, GdkPixbuf, GLib, bulk_connect, cairo
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scale import ScaleMark
from fabric.widgets.widget import Widget

from shared.animated.circularprogress import AnimatedCircularProgressBar
from shared.animated.scale import AnimatedScale

from .config import widget_config
from .icons import get_text_icon, symbolic_icons

storage_config = widget_config.get("widgets", {}).get("storage", {})

UTIL_FAST_POLL_SECONDS = 1
UTIL_SLOW_POLL_TICKS = 5

# Lazy-loaded stats fabricator - only created when first stat widget is used
_util_fabricator = None
_util_polling_enabled = False
_util_subscribers = 0
_util_changed_handler_ids: set[int] = set()


# Function to get the system stats using psutil
def stats_poll(*_):
    cpu_freq = None
    temperature = {}
    disk = psutil.disk_usage(storage_config.get("path", "/"))
    ticks = 0

    while _util_polling_enabled:
        if ticks % UTIL_SLOW_POLL_TICKS == 0:
            cpu_freq = psutil.cpu_freq()
            temperature = psutil.sensors_temperatures()
            disk = psutil.disk_usage(storage_config.get("path", "/"))

        virtual_memory = psutil.virtual_memory()
        yield {
            "cpu_usage": round(psutil.cpu_percent(), 1),
            "cpu_freq": cpu_freq,
            "temperature": temperature,
            "ram_usage": round(virtual_memory.percent, 1),
            "memory": virtual_memory,
            "disk": disk,
        }
        ticks += 1
        sleep(UTIL_FAST_POLL_SECONDS)


def _stop_util_fabricator() -> None:
    global _util_fabricator, _util_polling_enabled, _util_subscribers

    _util_polling_enabled = False

    if _util_fabricator is not None:
        destroy = getattr(_util_fabricator, "destroy", None)
        if callable(destroy):
            destroy()

    _util_fabricator = None
    _util_subscribers = 0
    _util_changed_handler_ids.clear()


def get_util_fabricator():
    """Get the stats fabricator, creating it on first access."""
    global _util_fabricator, _util_polling_enabled
    if _util_fabricator is None:
        from fabric import Fabricator

        _util_polling_enabled = True
        _util_fabricator = Fabricator(poll_from=stats_poll, stream=True)
    return _util_fabricator


def connect_util_fabricator_changed(callback) -> int:
    """Connect to util fabricator changed signal with lifecycle tracking."""
    global _util_subscribers

    handler_id = get_util_fabricator().connect("changed", callback)
    _util_changed_handler_ids.add(handler_id)
    _util_subscribers += 1
    return handler_id


def disconnect_util_fabricator_changed(handler_id: int | None) -> None:
    """Disconnect a changed signal handler and stop poller when unused."""
    global _util_subscribers

    if handler_id is None:
        return

    fabricator = _util_fabricator
    if fabricator is not None:
        with contextlib.suppress(KeyError, AttributeError, TypeError):
            fabricator.disconnect(handler_id)

    if handler_id in _util_changed_handler_ids:
        _util_changed_handler_ids.discard(handler_id)
        _util_subscribers = max(0, _util_subscribers - 1)

    if _util_subscribers == 0:
        _stop_util_fabricator()


# Backward compatibility - lazy proxy for util_fabricator
class _LazyFabricator:
    """Proxy that creates the fabricator on first use."""

    def __getattr__(self, name):
        return getattr(get_util_fabricator(), name)

    def __setattr__(self, name, value):
        setattr(get_util_fabricator(), name, value)


util_fabricator = _LazyFabricator()


def on_enter_notify_event(cursor, widget: Widget):
    widget.get_window().set_cursor(cursor)


def on_leave_notify_event(cursor, widget: Widget):
    widget.get_window().set_cursor(cursor)


# Function to setup cursor hover
def setup_cursor_hover(
    widget, cursor_name: Literal["pointer", "crosshair", "grab"] = "pointer"
):
    display = Gdk.Display.get_default()
    cursor = Gdk.Cursor.new_from_name(display, cursor_name)

    bulk_connect(
        widget,
        {
            "enter-notify-event": lambda *_: on_enter_notify_event(cursor, widget),
            "leave-notify-event": lambda *_: on_leave_notify_event(cursor, widget),
        },
    )


# Function to get the system stats using
def get_icon(app_icon, size=25) -> Image:
    icon_size = size - 5
    try:
        match app_icon:
            case str(x) if "file://" in x:
                return Image(
                    name="app-icon",
                    pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(
                        app_icon[7:], size, size
                    ),
                    size=size,
                )
            case str(x) if len(x) > 0 and x[0] == "/":
                return Image(
                    name="app-icon",
                    pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(app_icon, size, size),
                    size=size,
                )
            case _:
                return Image(
                    name="app-icon",
                    icon_name=app_icon
                    if app_icon
                    else symbolic_icons["fallback"]["notification"],
                    icon_size=icon_size,
                )
    except GLib.GError:
        return Image(
            name="app-icon",
            icon_name=symbolic_icons["fallback"]["notification"],
            icon_size=icon_size,
        )


# Function to get the widget class dynamically
def lazy_load_widget(widget_name: str, widgets_list):
    if widget_name in widgets_list:
        # Get the full module path (e.g., "widgets.BatteryWidget")
        class_path = widgets_list[widget_name]

        # Dynamically import the module
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)

        # Get the class from the module
        widget_class = getattr(module, class_name)

        return widget_class
    else:
        raise KeyError(f"Widget {widget_name} not found in the dictionary.")


# Function to create a text icon label
def nerd_font_icon(icon: str, props=None, name="nerd-icon") -> Label:
    label_props = {
        "markup": str(icon),  # Directly use the provided icon name
        "name": name,
        "h_align": "center",  # Align horizontally
        "v_align": "center",  # Align vertically
    }

    if props:
        label_props.update(props)

    return Label(**label_props)


# Function to create a surface from a widget
def create_surface_from_widget(
    widget: Widget, color=(0, 0, 0, 0)
) -> cairo.ImageSurface:
    alloc = widget.get_allocation()
    surface = cairo.ImageSurface(cairo.Format.ARGB32, alloc.width, alloc.height)
    cr = cairo.Context(surface)
    # Use a transparent background.
    cr.set_source_rgba(*color)
    cr.rectangle(0, 0, alloc.width, alloc.height)
    cr.fill()
    widget.draw(cr)
    return surface


# Function to get the bar graph representation
def get_bar_graph(usage: Number | str) -> str:
    if isinstance(usage, str):
        usage = int(usage)

    if usage <= 10:
        return "▁"
    if usage <= 30:
        return "▂"
    if usage <= 40:
        return "▃"
    if usage <= 50:
        return "▄"
    if usage <= 60:
        return "▅"
    if usage <= 70:
        return "▆"
    if usage <= 80:
        return "▇"
    return "█"


# Function to get the brightness icons
def get_brightness_icon_name(level: int) -> dict[Literal["icon_text", "icon"], str]:
    if level <= 0:
        return {
            "icon_text": get_text_icon("brightness.off"),
            "icon": symbolic_icons["brightness"]["off"],
        }

    if level <= 32:
        return {
            "icon_text": get_text_icon("brightness.low"),
            "icon": symbolic_icons["brightness"]["low"],
        }
    if level <= 66:
        return {
            "icon_text": get_text_icon("brightness.medium"),
            "icon": symbolic_icons["brightness"]["medium"],
        }
    return {
        "icon_text": get_text_icon("brightness.high"),
        "icon": symbolic_icons["brightness"]["high"],
    }


# Create a scale widget
def create_scale(
    name,
    marks=None,
    value=0,
    min_value: float = 0,
    max_value: float = 100,
    increments=(1, 1),
    curve=(0.34, 1.56, 0.64, 1.0),
    orientation="h",
    h_expand=True,
    h_align="center",
    style_classes=[""],
    duration=0.8,
    **kwargs,
) -> AnimatedScale:
    if marks is None:
        marks = (ScaleMark(value=i) for i in range(1, 100, 10))

    return AnimatedScale(
        name=name,
        marks=marks,
        value=value,
        min_value=min_value,
        max_value=max_value,
        increments=increments,
        orientation=orientation,
        curve=curve,
        h_expand=h_expand,
        h_align=h_align,
        duration=duration,
        style_classes=style_classes,
        **kwargs,
    )


# Function to get the volume icons
def get_audio_icon_name(
    volume: int, is_muted: bool
) -> dict[Literal["icon_text", "icon"], str]:
    if is_muted or volume == 0:
        level = "muted"
    elif volume <= 32:
        level = "low"
    elif volume <= 66:
        level = "medium"
    elif volume <= 100:
        level = "high"
    else:
        level = "overamplified"

    return {
        "icon_text": get_text_icon(f"volume.{level}"),
        "icon": symbolic_icons["audio"]["volume"][level],
    }


def create_progress(
    value=0,
    start_angle=150,
    end_angle=390,
    child=None,
    size=(22, 20),
    line_width=2,
    name="circular-progress",
    **kwargs,
):

    return AnimatedCircularProgressBar(
        name=name,
        style_classes=["stat-circle"],
        line_style="round",
        line_width=line_width,
        start_angle=start_angle,
        end_angle=end_angle,
        child=child,
        size=size,
        value=value,
        **kwargs,
    )
