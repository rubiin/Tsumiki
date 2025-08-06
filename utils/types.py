# Define the type
from typing import Literal

Layer = Literal["background", "bottom", "top", "overlay"]


Anchor = Literal[
    "center-left",
    "center",
    "center-right",
    "top",
    "top-right",
    "top-center",
    "top-left",
    "bottom-left",
    "bottom-center",
    "bottom-right",
]


Temperature_Unit = Literal["celsius", "fahrenheit"]

Wind_Speed_Unit = Literal["mph", "kmh"]

Keyboard_Mode = Literal["none", "exclusive", "on-demand"]


Power_Options = Literal["shutdown", "reboot", "hibernate", "suspend", "lock", "logout"]

Widget_Mode = Literal["circular", "graph", "label"]


Reveal_Animations = Literal[
    "none", "crossfade", "slide-right", "slide-left", "slide-up", "slide-down"
]
