import contextlib

from fabric.widgets.wayland import WaylandWindow
from gi.repository import Gtk, GtkLayerShell

from utils.monitors import HyprlandWithMonitors


class PopOverWindow(WaylandWindow):
    """A simple popover window that can point to a widget."""

    def __init__(
        self,
        parent: WaylandWindow,
        pointing_to: Gtk.Widget | None = None,
        margin: tuple[int, ...] | str = "0px 0px 0px 0px",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.exclusivity = "none"
        self._is_centered = False
        self._parent = parent
        self._pointing_widget = pointing_to
        self._hyprland = HyprlandWithMonitors()
        self._base_margin = self.extract_margin(margin)
        self.margin = self._base_margin.values()

        self.connect("notify::visible", self.do_update_handlers)

    def get_coords_for_widget(self, widget: Gtk.Widget) -> tuple[int, int]:
        if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):  # type: ignore
            return 0, 0
        allocation = widget.get_allocation()
        x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
            0,
            0,
        )
        return round(x / 2), round(y / 2)

    def set_pointing_to(self, widget: Gtk.Widget | None):
        if self._pointing_widget:
            with contextlib.suppress(Exception):
                self._pointing_widget.disconnect_by_func(self.do_handle_size_allocate)
        self._pointing_widget = widget
        return self.do_update_handlers()

    def do_update_handlers(self, *_):
        if not self._pointing_widget:
            return

        if not self.get_visible():
            try:
                self._pointing_widget.disconnect_by_func(self.do_handle_size_allocate)
                self.disconnect_by_func(self.do_handle_size_allocate)
            except Exception:
                pass
            return

        self._pointing_widget.connect("size-allocate", self.do_handle_size_allocate)
        self.connect("size-allocate", self.do_handle_size_allocate)

        return self.do_handle_size_allocate()

    def do_handle_size_allocate(self, *_):
        return self.do_reposition(self.do_calculate_edges())

    def do_calculate_edges(self):
        move_axe = "x"
        parent_anchor = self._parent.anchor

        if len(parent_anchor) != 3:
            self.anchor = "left bottom"
            self._is_centered = True
            return move_axe

        if (
            GtkLayerShell.Edge.LEFT in parent_anchor
            and GtkLayerShell.Edge.RIGHT in parent_anchor
        ):
            # horizontal -> move on x-axies
            move_axe = "x"
            if GtkLayerShell.Edge.TOP in parent_anchor:
                self.anchor = "left top"
            else:
                self.anchor = "left bottom"
        elif (
            GtkLayerShell.Edge.TOP in parent_anchor
            and GtkLayerShell.Edge.BOTTOM in parent_anchor
        ):
            # vertical -> move on y-axies
            move_axe = "y"
            if GtkLayerShell.Edge.RIGHT in parent_anchor:
                self.anchor = "top right"
            else:
                self.anchor = "top left"

        self._is_centered = False
        return move_axe

    def do_reposition(self, move_axe: str):
        parent_margin = self._parent.margin
        parent_x_margin, parent_y_margin = parent_margin[0], parent_margin[3]

        height = self.get_allocated_height()
        width = self.get_allocated_width()

        if self._pointing_widget:
            coords = self.get_coords_for_widget(self._pointing_widget)
            coords_centered = (
                round(coords[0] + self._pointing_widget.get_allocated_width() / 2),
                round(coords[1] + self._pointing_widget.get_allocated_height() / 2),
            )
        else:
            coords_centered = (
                round(self._parent.get_allocated_width() / 2),
                round(self._parent.get_allocated_height() / 2),
            )

        if self._is_centered:
            self.margin = tuple(
                a + b
                for a, b in zip(
                    (
                        (
                            0,
                            0,
                            0,
                            (
                                (
                                    (
                                        self._hyprland.display.get_monitor(
                                            self._hyprland.get_current_gdk_monitor_id()
                                        )
                                    )
                                    .get_geometry()
                                    .width
                                    / 2
                                    - self._parent.get_allocated_width() / 2
                                )
                                - width / 2
                            )
                            + coords_centered[0],
                        )
                    ),
                    self._base_margin.values(),
                )
            )
            return

        self.margin = tuple(
            a + b
            for a, b in zip(
                (
                    (
                        0,
                        0,
                        0,
                        round((parent_x_margin + coords_centered[0]) - (width / 2)),
                    )
                    if move_axe == "x"
                    else (
                        round((parent_y_margin + coords_centered[1]) - (height / 2)),
                        0,
                        0,
                        0,
                    )
                ),
                self._base_margin.values(),
            )
        )
