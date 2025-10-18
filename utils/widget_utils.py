import importlib
from numbers import Number
from time import sleep
from typing import Literal

import cairo  # For rendering the drag preview
import gi
import psutil
from fabric import Fabricator
from fabric.utils import bulk_connect
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scale import ScaleMark
from fabric.widgets.widget import Widget
from gi.repository import Gdk, GdkPixbuf, GLib

from shared.animated.scale import AnimatedScale

from .config import widget_config
from .icons import symbolic_icons, text_icons

storage_config = widget_config.get("widgets", {}).get("storage", {})


gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GdkPixbuf": "2.0"})


# Function to get the system stats using psutil
def stats_poll(fabricator):
    while True:
        yield {
            "cpu_usage": round(psutil.cpu_percent(), 1),
            "cpu_freq": psutil.cpu_freq(),
            "temperature": psutil.sensors_temperatures(),
            "ram_usage": round(psutil.virtual_memory().percent, 1),
            "memory": psutil.virtual_memory(),
            "disk": psutil.disk_usage(storage_config.get("path", "/")),
        }
        sleep(1)


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
        "label": str(icon),  # Directly use the provided icon name
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
            "icon_text": text_icons["brightness"]["off"],
            "icon": symbolic_icons["brightness"]["off"],
        }

    if level <= 32:
        return {
            "icon_text": text_icons["brightness"]["low"],
            "icon": symbolic_icons["brightness"]["low"],
        }
    if level <= 66:
        return {
            "icon_text": text_icons["brightness"]["medium"],
            "icon": symbolic_icons["brightness"]["medium"],
        }
    return {
        "icon_text": text_icons["brightness"]["high"],
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
        "icon_text": text_icons["volume"][level],
        "icon": symbolic_icons["audio"]["volume"][level],
    }


# Create a fabricator to poll the system stats
util_fabricator = Fabricator(poll_from=stats_poll, stream=True)
