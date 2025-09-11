import ctypes
import html
import json
import os
import re
import shutil
import subprocess
import threading
import time
from collections import Counter
from datetime import datetime
from functools import lru_cache
from io import BytesIO
from typing import Any, Callable, Iterable, Literal, Optional

import gi
import psutil
import qrcode
from fabric import Application
from fabric.utils import (
    FormattedString,
    cooldown,
    exec_shell_command,
    exec_shell_command_async,
    get_relative_path,
    invoke_repeater,
)
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, Gtk
from loguru import logger
from PIL import Image

from .colors import Colors
from .constants import NAMED_COLORS
from .exceptions import ExecutableNotFoundError
from .icons import text_icons
from .thread import run_in_thread, thread

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GdkPixbuf": "2.0"})


# Function to execute a shell command synchronously with formatted string
def formatted_exec_shell_command(
    unformatted_cmd: str, **kwargs
) -> str | Literal[False]:
    return exec_shell_command(FormattedString(unformatted_cmd).format(**kwargs))


# Function to execute a shell command asynchronously with formatted string
def formatted_exec_shell_command_async(
    unformatted_cmd: str, **kwargs
) -> tuple[Gio.Subprocess | None, Gio.DataInputStream]:
    return exec_shell_command_async(FormattedString(unformatted_cmd).format(**kwargs))


# Function to convert RGB to hex format
def rgb_to_hex(rgb) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


# Function to set the process name
def set_process_name(name: str):
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(15, name.encode("utf-8"), 0, 0, 0)  # 15 = PR_SET_NAME


# Function to convert RGB to CSS rgb format
def rgb_to_css(rgb) -> str:
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


# Function to mix two RGB colors, with a ratio of 0.5 by default.
def mix_colors(color1, color2, ratio=0.5) -> tuple[int, int, int]:
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)


# Function to tint a color by mixing it with white
def tint_color(color, tint_factor=1) -> tuple[int, int, int]:
    # tint_factor: 0 means original color, 1 means full white
    white = (255, 255, 255)
    return mix_colors(color, white, tint_factor)


def _pillow_worker(image_path, callback, color_count, resize):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.thumbnail((resize, resize), Image.LANCZOS)  # Fast, in-place resize
            pixels = img.getdata()

            most_common = Counter(pixels).most_common(color_count)
            palette = [color for color, _ in most_common]

            GLib.idle_add(callback, palette)
    except Exception as e:
        print(f"[ColorExtractor] Failed: {e}")
        GLib.idle_add(callback, None)


# Function to get a simple color palette from an image using threading
def get_simple_palette_threaded(
    image_path: str,
    callback: Callable[[Optional[list[tuple[int, int, int]]]], None],
    color_count: int = 4,
    resize: int = 64,
):
    threading.Thread(
        target=_pillow_worker,
        args=(image_path, callback, color_count, resize),
        daemon=True,
    ).start()


# Function to escape the markup
def parse_markup(text: str) -> str:
    return html.escape(text.replace("\n", " "))


def read_json_file(file_path: str) -> Optional[dict | list]:
    if not os.path.exists(file_path):
        logger.exception(f"JSON file {file_path} does not exist.")
        return None

    with open(file_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            logger.exception(f"Failed to read JSON file {file_path}: {e}")
            return None


def read_toml_file(file_path: str) -> dict:
    import pytomlpp as toml

    if not os.path.exists(file_path):
        logger.exception(f"TOML file {file_path} does not exist.")
        return None

    logger.info(f"[Config] Reading TOML config from {file_path}")
    try:
        with open(file_path, "r") as file:
            return toml.load(file)
    except Exception as e:
        logger.exception(f"Failed to read TOML file {file_path}: {e}")
        return None


# support for multiple monitors
def for_monitors(widget: Gtk.Widget) -> list[Gtk.Widget]:
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


# Function to copy the selected theme to the main styles directory
@run_in_thread
def copy_theme(theme: str):
    theme_dir = get_relative_path("../styles")
    destination_file = f"{theme_dir}/theme.scss"
    source_file = f"{theme_dir}/themes/{theme}.scss"

    if not os.path.exists(source_file):
        logger.warning(
            f"{Colors.WARNING}Warning: The theme file '{theme}.scss' was not found. Using default theme."  # noqa: E501
        )
        source_file = f"{theme_dir}/themes/catpuccin-mocha.scss"

    try:
        shutil.copyfile(source_file, destination_file)

    except FileNotFoundError:
        logger.exception(
            f"{Colors.ERROR}Error: The theme file '{source_file}' was not found."
        )
        exit(1)


# Function to update the theme configuration
def update_theme_config(theme_name: str):
    """Update the theme.json file with the new theme name."""
    try:
        theme_config_file = get_relative_path("../theme.json")

        # Read current theme config
        config = read_json_file(theme_config_file)

        if config is None:
            return

        # Update the theme name
        config["name"] = theme_name

        # Write back to file

        write_json_file(config, theme_config_file)

        logger.info(f"{Colors.INFO}[Theme] Updated theme config to {theme_name}")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error updating theme config: {e}")


def _apply_css_to_app():
    try:
        app = Application.get_default()
        if app:
            app.set_stylesheet_from_file(get_relative_path("../dist/main.css"))
            logger.info(f"{Colors.INFO}[Theme] CSS applied to application")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error applying CSS to app: {e}")


def _compile_css():
    """Compile SCSS in background thread."""
    try:
        check_executable_exists("sass")
        logger.info(f"{Colors.INFO}[Theme] Recompiling CSS")
        output = exec_shell_command(
            "sass styles/main.scss dist/main.css --no-source-map"
        )

        if output == "":
            logger.info(f"{Colors.INFO}[Theme] CSS recompiled successfully")
            GLib.idle_add(_apply_css_to_app)
        else:
            logger.exception(f"{Colors.ERROR}[Theme] Failed to compile sass!")
            logger.exception(f"{Colors.ERROR}[Theme] {output}")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error recompiling CSS: {e}")


# Function to recompile SCSS and apply the new CSS
def recompile_and_apply_css():
    """Recompile SCSS and apply the new CSS to the application."""

    # Run compilation in background thread
    thread(_compile_css)


# Function to convert celsius to fahrenheit
def celsius_to_fahrenheit(celsius: float) -> float:
    return (celsius * 9 / 5) + 32


# Merge the parsed data with the default configuration
def deep_merge(data: dict, target: dict) -> dict:
    """
    Recursively update a nested dictionary with values from another dictionary.
    """
    merged = target.copy()
    for key, user_value in data.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(user_value, dict)
        ):
            merged[key] = deep_merge(user_value, merged[key])
        else:
            merged[key] = user_value
    return merged


# Function to flatten a dictionary
def flatten_dict(d: dict, parent_key: str = "", sep: str = "-") -> dict:
    """Flatten a nested dictionary into a single level."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):  # If the value is a dictionary, recurse
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Function to exclude keys from a dictionary
def exclude_keys(d: dict, keys_to_exclude: list[str]) -> dict:
    return {k: v for k, v in d.items() if k not in keys_to_exclude}


# Function to format time in hours and minutes
def format_seconds_to_hours_minutes(secs: int) -> str:
    mm, _ = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d h %02d min" % (hh, mm)


# Function to convert bytes to kilobytes, megabytes, or gigabytes
def convert_bytes(
    bytes: int, to: Literal["kb", "mb", "gb", "tb"], format_spec=".1f"
) -> str:
    factor = {"kb": 1, "mb": 2, "gb": 3, "tb": 4}.get(to, 1)
    return f"{format(bytes / (1024**factor), format_spec)}{to.upper()}"


# Function to check if the current time is between sunrise and sunset
def check_if_day(sunrise_time, sunset_time, current_time: str | None = None) -> str:
    time_format = "%I:%M %p"

    if current_time is None:
        current_time = datetime.now().strftime(time_format)

    current_time_obj = datetime.strptime(current_time, time_format)
    sunrise_time_obj = datetime.strptime(sunrise_time, time_format)
    sunset_time_obj = datetime.strptime(sunset_time, time_format)

    # Compare current time with sunrise and sunset
    if sunrise_time_obj <= sunset_time_obj:
        return sunrise_time_obj <= current_time_obj < sunset_time_obj

    return current_time_obj >= sunrise_time_obj or current_time_obj < sunset_time_obj


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


# Function to unique list
def unique_list(lst: list[Any]) -> list[Any]:
    """Return a list with unique elements."""
    return list(set(lst))


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
    if max == 0:
        return 0
    if is_int:
        return int((current / max) * 100)
    else:
        return (current / max) * 100


# Function to check if a color is valid
def is_valid_gjs_color(color: str) -> bool:
    color_lower = color.strip().lower()

    if color_lower in NAMED_COLORS:
        return True

    hex_color_regex = r"^#(?:[a-fA-F0-9]{3,4}|[a-fA-F0-9]{6,8})$"
    rgb_regex = r"^rgb\(\s*(\d{1,3}%?\s*,\s*){2}\d{1,3}%?\s*\)$"
    rgba_regex = r"^rgba\(\s*(\d{1,3}%?\s*,\s*){3}(0|1|0?\.\d+)\s*\)$"

    if re.match(hex_color_regex, color):
        return True

    return bool(re.match(rgb_regex, color_lower) or re.match(rgba_regex, color_lower))


# Function to get the system uptime
def uptime() -> str:
    boot_time = psutil.boot_time()
    now = datetime.now()

    diff = now.timestamp() - boot_time

    # Convert the difference in seconds to hours and minutes
    hours, remainder = divmod(diff, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{int(hours):02}:{int(minutes):02}"


# Function to convert seconds to milliseconds
def convert_seconds_to_milliseconds(seconds: int) -> int:
    return seconds * 1000


# Function to check if an icon exists, otherwise use a fallback icon
def check_icon_exists(icon_name: str, fallback_icon: str) -> str:
    if Gtk.IconTheme.get_default().has_icon(icon_name):
        return icon_name
    return fallback_icon


# Set the scale's adjustment
def set_scale_adjustment(
    scale, min_value: float = 0, max_value: float = 100, steps: float = 1
):
    adj = scale.get_adjustment()
    if adj.get_upper() == adj.get_lower():
        scale.set_adjustment(
            Gtk.Adjustment(
                lower=min_value,
                upper=max_value,
                step_increment=steps,
                page_increment=0,
                page_size=0,
            )
        )


# Function to toggle a shell command
def toggle_command(command: str, full_command: str):
    if is_app_running(command):
        kill_process(command)
    else:
        subprocess.Popen(
            full_command.split(" "),
            stdin=subprocess.DEVNULL,  # No input stream
            stdout=subprocess.DEVNULL,  # Optionally discard the output
            stderr=subprocess.DEVNULL,  # Optionally discard the error output
            start_new_session=True,  # This prevents the process from being killed
        )


## Function to execute a shell command asynchronously
def kill_process(process_name: str):
    exec_shell_command_async(f"pkill {process_name}", lambda *_: None)


def add_style_class_lazy(widget: Gtk.Widget, class_name: str | Iterable[str]) -> int:
    return invoke_repeater(
        50, lambda: widget.add_style_class(class_name), initial_call=False
    )


def _get_config_collection(parsed_data: dict, widget_type: str) -> list:
    """Get collection for widget type - DRY principle."""
    collections = {
        "custom_button": lambda: (
            parsed_data.get("widgets", {})
            .get("custom_button_group", {})
            .get("buttons", [])
        ),
        "group": lambda: parsed_data.get("widget_groups", []),
        "collapsible": lambda: parsed_data.get("collapsible_groups", []),
    }
    getter = collections.get(widget_type, lambda: [])
    return getter()


def _validate_indexed_reference(
    identifier: str, collection: list, collection_name: str, section: str
) -> int:
    """Helper function to validate indexed references (groups, buttons, etc.).

    Args:
        identifier: String identifier that should be a digit
        collection: List to validate against
        collection_name: Name of collection for error messages
        section: Section name for error reporting

    Returns:
        Validated index

    Raises:
        ValueError: If validation fails
    """
    if not identifier.isdigit():
        raise ValueError(
            f"Invalid {collection_name} index '{identifier}' in section {section}. "
            "Must be a number."
        )

    idx = int(identifier)

    if not isinstance(collection, list):
        raise ValueError(f"{collection_name} must be an array")

    if not (0 <= idx < len(collection)):
        raise ValueError(
            f"{collection_name.title()} index {idx} is out of range "
            f"in section {section}. Available indices: 0-{len(collection) - 1}"
        )

    return idx


def _validate_special_widget(
    widget_type: str, identifier: str, parsed_data: dict, section: str
) -> None:
    """Unified validation for special widget types - DRY principle."""
    collection = _get_config_collection(parsed_data, widget_type)
    collection_names = {
        "custom_button": "custom button",
        "group": "widget group",
        "collapsible": "collapsible group",
    }
    collection_name = collection_names.get(widget_type, widget_type)
    _validate_indexed_reference(identifier, collection, collection_name, section)


def _validate_regular_widget(
    widget_spec: str, default_config: dict, section: str
) -> None:
    """Validate regular widget reference."""
    widgets_list = default_config.get("widgets", {})
    if widget_spec not in widgets_list:
        raise ValueError(
            f"Invalid widget '{widget_spec}' in section {section}. "
            "Please check the widget name."
        )


def validate_widget_reference(
    widget_spec: str, parsed_data: dict, default_config: dict, section: str = "layout"
):
    """Unified validation for any widget reference using dispatcher pattern.

    Args:
        widget_spec: Widget specification to validate
        parsed_data: Parsed configuration data
        default_config: Default configuration for widget names
        section: Section name for error reporting

    Raises:
        ValueError: If widget specification is invalid
    """
    # Handle special references
    if widget_spec.startswith("@"):
        if ":" not in widget_spec:
            raise ValueError(
                f"Invalid reference format '{widget_spec}' in section {section}"
            )

        widget_type, identifier = widget_spec[1:].split(":", 1)

        # Unified validation for all special widget types
        if widget_type in ["custom_button", "group", "collapsible"]:
            _validate_special_widget(widget_type, identifier, parsed_data, section)
        else:
            raise ValueError(
                f"Unknown widget type '{widget_type}' in section {section}"
            )
    else:
        # Regular widget validation
        _validate_regular_widget(widget_spec, default_config, section)


def validate_widgets(parsed_data, default_config):
    """Validates the widgets defined in the layout configuration.

    Args:
        parsed_data (dict): The parsed configuration data
        default_config (dict): The default configuration data

    Raises:
        ValueError: If an invalid widget is found in the layout
    """
    layout = parsed_data.get("layout", {})

    # Validate widgets in all sections
    for section_name, widgets in layout.items():
        if isinstance(widgets, list):
            for widget in widgets:
                validate_widget_reference(
                    widget, parsed_data, default_config, section_name
                )

    # Validate widgets inside groups
    for group_type in ["widget_groups", "collapsible_groups"]:
        groups = parsed_data.get(group_type, [])
        if isinstance(groups, list):
            for idx, group in enumerate(groups):
                if isinstance(group, dict) and "widgets" in group:
                    for widget in group["widgets"]:
                        validate_widget_reference(
                            widget, parsed_data, default_config, f"{group_type}[{idx}]"
                        )


# Function to generate a QR code image
@ttl_lru_cache(3600, 10)
def make_qrcode(text: str, size: int = 200) -> GdkPixbuf.Pixbuf:
    # Generate QR Code image
    qr = qrcode.make(text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Load into GTK Pixbuf
    loader = GdkPixbuf.PixbufLoader.new_with_type("png")
    loader.write(buffer.read())
    loader.close()
    pixbuf = loader.get_pixbuf()

    # Scale Pixbuf to the desired size
    scaled_pixbuf = pixbuf.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)

    return scaled_pixbuf


# Function to play sound
@cooldown(1)
def play_sound(file: str):
    exec_shell_command_async(f"pw-play {file}", lambda *_: None)


# Function to get the distro icon
@ttl_lru_cache(600, 10)
def get_distro_icon() -> str:
    distro_id = GLib.get_os_info("ID")

    # Search for the icon in the list
    return text_icons["distro"].get(distro_id, "")


# Function to check if an executable exists
@ttl_lru_cache(600, 10)
def check_executable_exists(executable_name):
    executable_path = GLib.find_program_in_path(executable_name)
    if not executable_path:
        raise ExecutableNotFoundError(
            executable_name
        )  # Raise an error if the executable is not found and exit the application


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


# Function to write a JSON file
@run_in_thread
def write_json_file(data: dict, path: str):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Failed to write json: {e}")


# Function to ensure the file exists
@run_in_thread
def ensure_file(path: str):
    file = Gio.File.new_for_path(path)
    parent = file.get_parent()

    try:
        if parent and not parent.query_exists(None):
            parent.make_directory_with_parents(None)

        if not file.query_exists(None):
            file.create(Gio.FileCreateFlags.NONE, None)
    except GLib.Error as e:
        print(f"Failed to ensure file '{path}': {e.message}")


# Function to ensure the directory exists
@run_in_thread
def ensure_directory(path: str):
    if not GLib.file_test(path, GLib.FileTest.EXISTS):
        try:
            Gio.File.new_for_path(path).make_directory_with_parents(None)
        except GLib.Error as e:
            print(f"Failed to create directory {path}: {e.message}")


# Function to check if an app is running
def is_app_running(app_name: str) -> bool:
    return len(exec_shell_command(f"pidof {app_name}")) != 0


# Function to take a memory snapshot
def take_snapshot():
    import tracemalloc

    tracemalloc.start()
    # Later in code
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    print("stats", tracemalloc.get_traced_memory())

    print("[Top 10 Memory Lines]")
    for stat in top_stats[:10]:
        print(stat)

    return True  # Keep the timeout active


# Function to set a debug logger for GLib
def set_debug_logger():
    def log_handler(domain, level, message):
        import traceback

        level_name = {
            GLib.LogLevelFlags.LEVEL_ERROR: "ERROR",
            GLib.LogLevelFlags.LEVEL_CRITICAL: "CRITICAL",
            GLib.LogLevelFlags.LEVEL_WARNING: "WARNING",
            GLib.LogLevelFlags.LEVEL_MESSAGE: "MESSAGE",
            GLib.LogLevelFlags.LEVEL_INFO: "INFO",
            GLib.LogLevelFlags.LEVEL_DEBUG: "DEBUG",
        }.get(
            GLib.LogLevelFlags(
                level
                & ~GLib.LogLevelFlags.FLAG_FATAL
                & ~GLib.LogLevelFlags.FLAG_RECURSION
            ),
            f"UNKNOWN({level})",
        )
        print(f"\n[{domain or 'Default'}] {level_name}: {message}")
        traceback.print_stack()

    # Set log levels
    log_levels = (
        GLib.LogLevelFlags.LEVEL_ERROR
        | GLib.LogLevelFlags.LEVEL_CRITICAL
        | GLib.LogLevelFlags.LEVEL_WARNING
        | GLib.LogLevelFlags.LEVEL_MESSAGE
        | GLib.LogLevelFlags.LEVEL_INFO
        | GLib.LogLevelFlags.LEVEL_DEBUG
    )

    # Common GTK/GLib and related log domains
    domains = [
        None,  # Default domain
        "Gtk",  # GTK (Graphical Toolkit)
        "Gdk",  # GDK (Windowing Abstraction Layer)
        "GLib",  # GLib (Core utility library)
        "GLib-GObject",  # GObject (Object system and signals)
        "Pango",  # Pango (Text layout/rendering)
        "Atk",  # ATK (Accessibility Toolkit)
        "GIO",  # GIO (I/O and VFS abstraction)
        "GStreamer",  # GStreamer (Multimedia framework)
        "Gst",  # GStreamer (sometimes abbreviated domain)
        "Soup",  # libsoup (HTTP library)
        "GVfs",  # GNOME Virtual File System
        "GWeather",  # GNOME Weather library
        "WebKit",  # WebKitGTK (Web rendering engine)
        "Vte",  # Virtual Terminal Emulator (GNOME Terminal)
        "Cogl",  # Cogl (GPU rendering abstraction)
        "NM",  # NetworkManager
        "BlueZ",  # Bluetooth stack for Linux
        "ModemManager",  # Manages mobile broadband connections
    ]

    for domain in domains:
        GLib.log_set_handler(domain, log_levels, log_handler)
