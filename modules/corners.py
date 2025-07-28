from typing import Iterable

from fabric.widgets.box import Box
from fabric.widgets.shapes import Corner
from fabric.widgets.wayland import WaylandWindow as Window

from shared.widget_container import BaseWidget


class SideCorner(Box):
    """A container for a corner shape."""

    def __init__(self, corner: Iterable[int] | int, size):
        super().__init__(
            name="corner-container",
            children=Corner(
                name="corner",
                orientation=corner,
                size=size,
            ),
        )


class ScreenCorners(Window, BaseWidget):
    """A window that displays all four corners."""

    def __init__(self, config, **kwargs):
        self.config = config["modules"]["screen_corners"]

        size = self.config.get("size", 20)
        super().__init__(
            name="corners",
            layer="top",
            anchor="top bottom left right",
            exclusivity="normal",
            pass_through=True,
            visible=False,
            all_visible=False,
            **kwargs,
        )

        self.all_corners = Box(
            name="all-corners",
            orientation="v",
            h_expand=True,
            v_expand=True,
            h_align="fill",
            v_align="fill",
            children=[
                Box(
                    name="top-corners",
                    orientation="h",
                    h_align="fill",
                    children=[
                        SideCorner("top-left", size),
                        Box(h_expand=True),
                        SideCorner("top-right", size),
                    ],
                ),
                Box(v_expand=True),
                Box(
                    name="bottom-corners",
                    orientation="h",
                    h_align="fill",
                    children=[
                        SideCorner("bottom-left", size),
                        Box(h_expand=True),
                        SideCorner("bottom-right", size),
                    ],
                ),
            ],
        )

        self.add(self.all_corners)

        self.show_all()
