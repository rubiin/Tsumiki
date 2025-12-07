# Define the type
from typing import Literal, get_args

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

Orientation = Literal["vertical", "horizontal"]

Dock_Behavior = Literal["always_show", "intellihide"]

Bar_Location = Literal["top", "bottom"]

Data_Unit = Literal["kb", "mb", "gb", "tb"]

Return_Type = Literal["plain", "json"]

Osd_Type = Literal["brightness", "volume", "microphone"]

Slider_Type = Literal["brightness", "volume", "microphone"]

Title_Fallback = Literal["class", "title"]


# Helper function to extract values from Literal types
def get_literal_values(literal_type) -> list[str]:
    """Extract the string values from a Literal type."""
    return list(get_args(literal_type))
