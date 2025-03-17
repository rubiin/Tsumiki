import importlib
from time import sleep
from typing import Literal

import psutil
from fabric import Fabricator
from fabric.utils import bulk_connect
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scale import ScaleMark
from gi.repository import Gdk, GLib

from shared import AnimatedScale
from utils.functions import uptime

from .config import widget_config
from .icons import brightness_text_icons, icons, volume_text_icons


# Function to get the system stats using psutil
def stats_poll(fabricator):
    storage_config = widget_config["storage"]
    while True:
        yield {
            "cpu_usage": f"{round(psutil.cpu_percent())}%",
            "cpu_freq": psutil.cpu_freq(),
            "temperature": psutil.sensors_temperatures(),
            "ram_usage": f"{round(psutil.virtual_memory().percent)}%",
            "memory": psutil.virtual_memory(),
            "disk": psutil.disk_usage(storage_config["path"]),
            "user": psutil.users()[0][0],
            "uptime": uptime(),
        }
        sleep(1)


# Function to setup cursor hover
def setup_cursor_hover(
    widget, cursor_name: Literal["pointer", "crosshair", "grab"] = "pointer"
):
    display = Gdk.Display.get_default()

    def on_enter_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, cursor_name)
        widget.get_window().set_cursor(cursor)

    def on_leave_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, "default")
        widget.get_window().set_cursor(cursor)

    bulk_connect(
        widget,
        {
            "enter-notify-event": on_enter_notify_event,
            "leave-notify-event": on_leave_notify_event,
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
                    image_file=app_icon[7:],
                    size=size,
                )
            case str(x) if len(x) > 0 and x[0] == "/":
                return Image(
                    name="app-icon",
                    image_file=app_icon,
                    size=size,
                )
            case _:
                return Image(
                    name="app-icon",
                    icon_name=app_icon
                    if app_icon
                    else icons["fallback"]["notification"],
                    icon_size=icon_size,
                )
    except GLib.GError:
        return Image(
            name="app-icon",
            icon_name=icons["fallback"]["notification"],
            icon_size=icon_size,
        )


def lazy_load_widget(widget_name, widgets_list):
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
def text_icon(icon: str, size: str = "16px", props=None):
    label_props = {
        "label": str(icon),  # Directly use the provided icon name
        "name": "nerd-icon",
        "style": f"font-size: {size}; ",
        "h_align": "center",  # Align horizontally
        "v_align": "center",  # Align vertically
    }

    if props:
        label_props.update(props)

    return Label(**label_props)


# Function to get the brightness icons
def get_brightness_icon_name(level: int) -> dict[Literal["icon_text", "icon"], str]:
    if level <= 0:
        return {
            "text_icon": brightness_text_icons["off"],
            "icon": "display-brightness-off-symbolic",
        }

    if level <= 32:
        return {
            "text_icon": brightness_text_icons["low"],
            "icon": "display-brightness-low-symbolic",
        }
    if level <= 66:
        return {
            "text_icon": brightness_text_icons["medium"],
            "icon": "display-brightness-medium-symbolic",
        }
    # level > 66
    return {
        "text_icon": brightness_text_icons["high"],
        "icon": "display-brightness-high-symbolic",
    }


# Create a scale widget
def create_scale(
    marks=None,
    value=70,
    min_value=0,
    max_value=100,
    increments=(1, 1),
    orientation="h",
    h_expand=True,
    h_align="center",
    style_classes="",
) -> AnimatedScale:
    if marks is None:
        marks = (ScaleMark(value=i) for i in range(1, 100, 10))

    return AnimatedScale(
        marks=marks,
        value=value,
        min_value=min_value,
        max_value=max_value,
        increments=increments,
        orientation=orientation,
        h_expand=h_expand,
        h_align=h_align,
        style_classes=style_classes,
    )


# Function to get the volume icons
def get_audio_icon_name(
    volume: int, is_muted: bool
) -> dict[Literal["icon_text", "icon"], str]:
    if volume <= 0 or is_muted:
        return {
            "text_icon": volume_text_icons["low"],
            "icon": "audio-volume-muted-symbolic",
        }
    if volume > 0 and volume < 32:
        return {
            "text_icon": volume_text_icons["low"],
            "icon": "audio-volume-low-symbolic",
        }
    if volume > 32 and volume < 66:
        return {
            "text_icon": volume_text_icons["medium"],
            "icon": "audio-volume-medium-symbolic",
        }
    if volume >= 66 and volume <= 100:
        return {
            "text_icon": volume_text_icons["high"],
            "icon": "audio-volume-high-symbolic",
        }
    else:
        return {
            "text_icon": volume_text_icons["overamplified"],
            "icon": "audio-volume-overamplified-symbolic",
        }


# Create a fabricator to poll the system stats
util_fabricator = Fabricator(poll_from=stats_poll, stream=True)
