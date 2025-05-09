import os
import re
import shutil
import time
from datetime import datetime
from functools import lru_cache
from typing import Dict, List, Literal, Optional

import psutil
from fabric.utils import (
    cooldown,
    exec_shell_command,
    exec_shell_command_async,
    get_relative_path,
)
from gi.repository import Gdk, Gio, GLib, Gtk
from loguru import logger

from .colors import Colors
from .constants import named_colors
from .icons import text_icons
from .thread import run_in_thread


# Function to escape the markup
def parse_markup(text):
    return text


# support for multiple monitors
def for_monitors(widget):
    n = Gdk.Display.get_default().get_n_monitors() if Gdk.Display.get_default() else 1
    return [widget(i) for i in range(n)]


# Function to ttl lru cache
def ttl_lru_cache(seconds_to_live: int, maxsize: int = 128):
    def wrapper(func):
        @lru_cache(maxsize)
        def inner(__ttl, *args, **kwargs):
            return func(*args, **kwargs)

        return lambda *args, **kwargs: inner(
            time.time() // seconds_to_live, *args, **kwargs
        )

    return wrapper


@run_in_thread
def copy_theme(theme: str):
    destination_file = get_relative_path("../styles/theme.scss")
    source_file = get_relative_path(f"../styles/themes/{theme}.scss")

    if not os.path.exists(source_file):
        logger.warning(
            f"{Colors.WARNING}Warning: The theme file '{theme}.scss' was not found. Using default theme."  # noqa: E501
        )
        source_file = get_relative_path("../styles/themes/catpuccin-mocha.scss")

    try:
        shutil.copyfile(source_file, destination_file)

    except FileNotFoundError:
        logger.error(
            f"{Colors.ERROR}Error: The theme file '{source_file}' was not found."
        )
        exit(1)


# Function to convert celsius to fahrenheit
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9 / 5) + 32
    return fahrenheit


# Merge the parsed data with the default configuration
def merge_defaults(data: dict, defaults: dict):
    return {**defaults, **data}


## Function to execute a shell command asynchronously
def kill_process(process_name: str):
    exec_shell_command_async(f"pkill {process_name}", lambda *_: None)
    return True


# Function to flatten a dictionary
def flatten_dict(d, parent_key="", sep="-"):
    """Flatten a nested dictionary into a single level."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):  # If the value is a dictionary, recurse
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Validate the widgets
def validate_widgets(parsed_data, default_config):
    """Validates the widgets defined in the layout configuration.

    Args:
        parsed_data (dict): The parsed configuration data
        default_config (dict): The default configuration data

    Raises:
        ValueError: If an invalid widget is found in the layout
    """
    layout = parsed_data["layout"]
    for section in layout:
        for widget in layout[section]:
            if widget.startswith("@group:"):
                # Handle module groups
                group_idx = widget.replace("@group:", "", 1)
                if not group_idx.isdigit():
                    raise ValueError(
                        "Invalid module group index "
                        f"'{group_idx}' in section {section}. Must be a number."
                    )
                idx = int(group_idx)
                groups = parsed_data.get("module_groups", [])
                if not isinstance(groups, list):
                    raise ValueError(
                        "module_groups must be an array when using @group references"
                    )
                if not (0 <= idx < len(groups)):
                    raise ValueError(
                        "Module group index "
                        f"{idx} is out of range. Available indices: 0-{len(groups) - 1}"
                    )
                # Validate widgets inside the group
                group = groups[idx]
                if not isinstance(group, dict) or "widgets" not in group:
                    raise ValueError(
                        f"Invalid module group at index {idx}. "
                        "Must be an object with 'widgets' array."
                    )
                for group_widget in group["widgets"]:
                    if group_widget not in default_config:
                        raise ValueError(
                            f"Invalid widget '{group_widget}' found in "
                            f"module group {idx}. Please check the widget name."
                        )
            elif widget not in default_config:
                raise ValueError(
                    f"Invalid widget '{widget}' found in section {section}. "
                    "Please check the widget name."
                )


# Function to exclude keys from a dictionary        )
def exclude_keys(d: Dict, keys_to_exclude: List[str]) -> Dict:
    return {k: v for k, v in d.items() if k not in keys_to_exclude}


# Function to format time in hours and minutes
def format_time(secs: int):
    mm, _ = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d h %02d min" % (hh, mm)


# Function to convert bytes to kilobytes, megabytes, or gigabytes
def convert_bytes(bytes: int, to: Literal["kb", "mb", "gb"], format_spec=".1f"):
    multiplier = 1

    if to == "mb":
        multiplier = 2
    elif to == "gb":
        multiplier = 3

    return f"{format(bytes / (1024**multiplier), format_spec)}{to.upper()}"


def check_if_day(sunrise_time, sunset_time, current_time: str | None = None) -> str:
    time_format = "%I:%M %p"

    if current_time is None:
        current_time = datetime.now().strftime(time_format)

    current_time_obj = datetime.strptime(current_time, time_format)
    sunrise_time_obj = datetime.strptime(sunrise_time, time_format)
    sunset_time_obj = datetime.strptime(sunset_time, time_format)

    # Compare current time with sunrise and sunset
    return sunrise_time_obj <= current_time_obj < sunset_time_obj

    # wttr.in time are in 300,400...2100 format , we need to convert it to 4:00...21:00


def convert_to_12hr_format(time: str) -> str:
    time = int(time)
    hour = time // 100  # Get the hour (e.g., 1200 -> 12)
    minute = time % 100  # Get the minutes (e.g., 1200 -> 00)

    # Convert to 12-hour format
    period = "AM" if hour < 12 else "PM"

    # Adjust hour for 12-hour format
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12

    # Format the time as a string
    return f"{hour}:{minute:02d} {period}"


# Function to get the system uptime
def uptime():
    boot_time = psutil.boot_time()
    now = datetime.now()

    diff = now.timestamp() - boot_time

    # Convert the difference in seconds to hours and minutes
    hours, remainder = divmod(diff, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{int(hours):02}:{int(minutes):02}"


# Function to convert seconds to milliseconds
def convert_seconds_to_milliseconds(seconds: int):
    return seconds * 1000


# Function to check if an icon exists, otherwise use a fallback icon
def check_icon_exists(icon_name: str, fallback_icon: str) -> str:
    if Gtk.IconTheme.get_default().has_icon(icon_name):
        return icon_name
    return fallback_icon


# Function to play sound
@cooldown(1)
@run_in_thread
def play_sound(file: str):
    exec_shell_command_async(f"pw-play {file}", lambda *_: None)
    return True


# Function to get the distro icon
@ttl_lru_cache(600, 10)
def get_distro_icon():
    distro_id = GLib.get_os_info("ID")

    # Search for the icon in the list
    return text_icons["distro"].get(distro_id, "")


# Function to check if an executable exists
@ttl_lru_cache(600, 10)
def executable_exists(executable_name):
    executable_path = shutil.which(executable_name)
    return bool(executable_path)


# Function to send a notification
@cooldown(1)
def send_notification(
    title: str,
    body: str,
    urgency: Literal["low", "normal", "critical"] = "normal",
    icon: Optional[str] = None,
    app_name: str = "Application",
):
    # Create a notification with the title
    notification = Gio.Notification.new(title)
    notification.set_body(body)

    # Set the urgency level if provided
    if urgency in ["low", "normal", "critical"]:
        notification.set_urgent(urgency)

    # Set the icon if provided
    if icon:
        notification.set_icon(Gio.ThemedIcon.new(icon))

    # Optionally, set the application name
    notification.set_title(app_name)

    application = Gio.Application.get_default()

    # Send the notification to the application
    application.send_notification(None, notification)
    return True


# Function to get the relative time
def get_relative_time(mins: int) -> str:
    # Seconds
    if mins == 0:
        return "now"

    # Minutes
    if mins < 60:
        return f"{mins} minute{'s' if mins > 1 else ''} ago"

    # Hours
    if mins < 1440:
        hours = mins // 60
        return f"{hours} hour{'s' if hours > 1 else ''} ago"

    # Days
    days = mins // 1440
    return f"{days} day{'s' if days > 1 else ''} ago"


# Function to get the percentage of a value
def convert_to_percent(
    current: int | float, max: int | float, is_int=True
) -> int | float:
    if is_int:
        return int((current / max) * 100)
    else:
        return (current / max) * 100


# Function to ensure the file exists
def ensure_file(path: str) -> None:
    file = Gio.File.new_for_path(path)
    parent = file.get_parent()

    if parent and not parent.query_exists(None):
        parent.make_directory_with_parents(None)

    if not file.query_exists(None):
        file.create(Gio.FileCreateFlags.NONE, None)


# Function to ensure the directory exists
def ensure_directory(path: str) -> None:
    if not GLib.file_test(path, GLib.FileTest.EXISTS):
        Gio.File.new_for_path(path).make_directory_with_parents(None)


# Function to unique list
def unique_list(lst) -> List:
    return list(set(lst))


# Function to check if an app is running
def is_app_running(app_name: str) -> bool:
    return len(exec_shell_command(f"pidof {app_name}")) != 0


# Function to check if a color is valid
def is_valid_gjs_color(color: str) -> bool:
    color_lower = color.strip().lower()

    if color_lower in named_colors:
        return True

    hex_color_regex = r"^#(?:[a-fA-F0-9]{3,4}|[a-fA-F0-9]{6,8})$"
    rgb_regex = r"^rgb\(\s*(\d{1,3}%?\s*,\s*){2}\d{1,3}%?\s*\)$"
    rgba_regex = r"^rgba\(\s*(\d{1,3}%?\s*,\s*){3}(0|1|0?\.\d+)\s*\)$"

    if re.match(hex_color_regex, color):
        return True

    return bool(re.match(rgb_regex, color_lower) or re.match(rgba_regex, color_lower))
