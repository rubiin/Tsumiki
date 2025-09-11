from typing import Literal

from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget
from gi.repository import Gdk, GLib

from utils.monitors import HyprlandWithMonitors
from utils.types import Anchor, Keyboard_Mode, Layer


class Padding(EventBox):
    """A widget to add padding around the child widget."""

    def __init__(self, name: str | None = None, style: str = "", **kwargs):
        super().__init__(
            name=name,
            h_expand=True,
            v_expand=True,
            child=Box(style=style, h_expand=True, v_expand=True),
            events=["button-press"],
            **kwargs,
        )
        self.set_can_focus(False)


class PopupRevealer(EventBox):
    """A widget to reveal a popup window."""

    def __init__(
        self,
        popup_window: Window,
        decorations: str = "padding: 1px;",
        name: str | None = None,
        child: Widget | None = None,
        transition_type: Literal[
            "none",
            "crossfade",
            "slide-right",
            "slide-left",
            "slide-up",
            "slide-down",
        ] = "slide-down",
        transition_duration: int = 400,
    ):
        self.revealer: Revealer = Revealer(
            name=name,
            child=child,
            transition_type=transition_type,
            transition_duration=transition_duration,
            notify_child_revealed=lambda revealer, _: [
                revealer.hide(),
                popup_window.set_visible(False),
            ]
            if not revealer.fully_revealed
            else None,
            notify_reveal_child=lambda revealer, _: [
                popup_window.set_visible(True),
            ]
            if revealer.child_revealed
            else None,
        )
        super().__init__(
            style=decorations,
            child=self.revealer,
        )


def make_layout(anchor: str, name: str, popup: PopupRevealer, **kwargs) -> Box:
    match anchor:
        case "center-left":
            return Box(
                children=[
                    Box(
                        orientation="vertical",
                        children=[
                            Padding(name=name, **kwargs),
                            popup,
                            Padding(name=name, **kwargs),
                        ],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )

        case "center":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        orientation="vertical",
                        children=[
                            Padding(name=name, **kwargs),
                            popup,
                            Padding(name=name, **kwargs),
                        ],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "center-right":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        orientation="vertical",
                        children=[
                            Padding(name=name, **kwargs),
                            popup,
                            Padding(name=name, **kwargs),
                        ],
                    ),
                ]
            )
        case "top":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        orientation="vertical",
                        children=[popup, Padding(name=name, **kwargs)],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "top-right":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        h_expand=False,
                        orientation="vertical",
                        children=[popup, Padding(name=name, **kwargs)],
                    ),
                ]
            )
        case "top-center":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        h_expand=False,
                        orientation="vertical",
                        children=[popup, Padding(name=name, **kwargs)],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "top-left":
            return Box(
                children=[
                    Box(
                        h_expand=False,
                        orientation="vertical",
                        children=[popup, Padding(name=name, **kwargs)],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "bottom-left":
            return Box(
                children=[
                    Box(
                        h_expand=False,
                        orientation="vertical",
                        children=[Padding(name=name, **kwargs), popup],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "bottom-center":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        h_expand=False,
                        orientation="vertical",
                        children=[Padding(name=name, **kwargs), popup],
                    ),
                    Padding(name=name, **kwargs),
                ]
            )
        case "bottom-right":
            return Box(
                children=[
                    Padding(name=name, **kwargs),
                    Box(
                        h_expand=True,
                        orientation="vertical",
                        children=[Padding(name=name, **kwargs), popup],
                    ),
                ]
            )
        case _:
            return None


class PopupWindow(Window):
    """A popup window to display a message."""

    def __init__(
        self,
        layer: Layer = "overlay",
        name="popup-window",
        decorations="padding: 1px;",
        child: Widget | None = None,
        transition_type: Literal[
            "none",
            "crossfade",
            "slide-right",
            "slide-left",
            "slide-up",
            "slide-down",
        ]
        | None = None,
        transition_duration=100,
        popup_visible: bool = False,
        anchor: Anchor = "top-right",
        enable_inhibitor: bool = False,
        keyboard_mode: Keyboard_Mode = "on-demand",
        timeout: int = 1000,
    ):
        self._layer = layer
        self.timeout = timeout
        self.current_timeout = 0
        self.popup_running = False

        self.popup_visible = popup_visible

        self.enable_inhibitor = enable_inhibitor

        self.monitor_number: int | None = None
        self.hyprland_monitor = HyprlandWithMonitors()

        self.reveal_child = PopupRevealer(
            popup_window=self,
            child=child,
            transition_type=transition_type,
            transition_duration=transition_duration,
            decorations=decorations,
            name=name,
        )

        super().__init__(
            name=name,
            layer=self._layer,
            keyboard_mode=keyboard_mode,
            visible=False,
            exclusivity="normal",
            anchor="top bottom right left",
            child=make_layout(
                anchor=anchor,
                name=name,
                popup=self.reveal_child,
                on_button_press_event=self.on_inhibit_click,
            ),
            on_key_release_event=self.on_key_release,
        )

    def on_key_release(self, _, event_key: Gdk.EventKey):
        if event_key.keyval == Gdk.KEY_Escape:
            self.popup_visible = False
            self.reveal_child.revealer.set_reveal_child(self.popup_visible)

    def on_inhibit_click(self, *_):
        self.popup_visible = False
        self.reveal_child.revealer.set_reveal_child(self.popup_visible)

    def toggle_popup(self, monitor: bool = False):
        if monitor:
            curr_monitor = self.hyprland_monitor.get_current_gdk_monitor_id()
            self.monitor = curr_monitor
            if self.monitor_number != curr_monitor and self.popup_visible:
                self.monitor_number = curr_monitor
                return

            self.monitor_number = curr_monitor

        if not self.popup_visible:
            self.reveal_child.revealer.set_visible(True)

        self.set_property("pass-through", not self.enable_inhibitor)
        self.popup_visible = not self.popup_visible
        self.reveal_child.revealer.set_reveal_child(self.popup_visible)

    def popup_timeout(self):
        curr_monitor = self.hyprland_monitor.get_current_gdk_monitor_id()
        self.monitor = curr_monitor

        if not self.popup_visible:
            self.reveal_child.revealer.set_visible(True)
        if self.popup_running:
            self.current_timeout = 0
            return
        self.popup_visible = True
        self.reveal_child.revealer.set_reveal_child(self.popup_visible)
        self.popup_running = True

        def popup_func():
            if self.current_timeout >= self.timeout:
                self.popup_visible = False
                self.reveal_child.revealer.set_reveal_child(self.popup_visible)
                self.current_timeout = 0
                self.popup_running = False
                return False
            self.current_timeout += 500
            return True

        self.set_property("pass-through", not self.enable_inhibitor)
        GLib.timeout_add(500, popup_func)
