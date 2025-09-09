# ruff: noqa: F401

import math
import mimetypes
import os
import re
import subprocess
from collections.abc import Iterable
from functools import partial, reduce
from typing import Literal, cast

import cairo
import fabric
import gi
from fabric import Builder, Fabricator, Property, Service, Signal
from fabric.audio.service import Audio
from fabric.bluetooth.service import BluetoothClient, BluetoothDevice
from fabric.hyprland.widgets import (
    HyprlandActiveWindow as ActiveWindow,
)
from fabric.hyprland.widgets import (
    HyprlandLanguage as Language,
)
from fabric.hyprland.widgets import (
    HyprlandWorkspaces as Workspaces,
)
from fabric.notifications import Notification, Notifications
from fabric.system_tray.widgets import SystemTray
from fabric.utils import (
    DesktopApp,
    FormattedString,
    bulk_connect,
    bulk_replace,
    exec_shell_command,
    exec_shell_command_async,
    get_desktop_applications,
    get_relative_path,
    idle_add,
    invoke_repeater,
    monitor_file,
    remove_handler,
    truncate,
)
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.datetime import DateTime
from fabric.widgets.entry import Entry
from fabric.widgets.eventbox import EventBox
from fabric.widgets.fixed import Fixed
from fabric.widgets.flowbox import FlowBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.revealer import Revealer
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.separator import Separator
from fabric.widgets.shapes import Corner
from fabric.widgets.stack import Stack
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget
from loguru import logger

gi.require_versions(
    {"Gtk": "3.0", "Gdk": "3.0", "GdkPixbuf": "2.0", "Playerctl": "2.0"}
)
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, Gtk, Playerctl  # noqa: E402
