import contextlib

import gi
from fabric.widgets.wayland import WaylandWindow
from gi.repository import Gdk, Gtk, GtkLayerShell

gi.require_version("GtkLayerShell", "0.1")


class PopOverWindow(WaylandWindow):
    """Window that displays content in a popover style"""

    def __init__(
        self,
        parent: WaylandWindow,
        pointing_to: Gtk.Widget | None = None,
        margin: tuple[int, ...] | str = "0 0 0 0",
        **kwargs,
    ):
        super().__init__(
            style_classes="popover",
            **kwargs,
        )
        self.exclusivity = "none"
        self._parent = parent
        self._pointing_widget = pointing_to
        self._base_margin = self.extract_margin(margin)
        self.margin = self._base_margin.values()
        self.display = Gdk.Display.get_default()

        self.connect("notify::visible", self.do_update_handlers)

    def get_coords_for_widget(self, widget: Gtk.Widget) -> tuple[int, int]:
        if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):
            return 0, 0
        allocation = widget.get_allocation()
        x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
            0,
            0,
        )
        return round(x / 2), round(y / 2)

    def get_monitor_geometry(self) -> Gdk.Rectangle | None:
        screen = self.display.get_default_screen()

        if self._pointing_widget:
            window = self._pointing_widget.get_window()
            if window:
                monitor_num = screen.get_monitor_at_window(window)
                return screen.get_monitor_geometry(monitor_num)

        window = self._parent.get_window()
        if window:
            monitor_num = screen.get_monitor_at_window(window)
            return screen.get_monitor_geometry(monitor_num)

        return None

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
            return move_axe

        if (
            GtkLayerShell.Edge.LEFT in parent_anchor
            and GtkLayerShell.Edge.RIGHT in parent_anchor
        ):
            move_axe = "x"
            if GtkLayerShell.Edge.TOP in parent_anchor:
                self.anchor = "left top"
            else:
                self.anchor = "left bottom"
        elif (
            GtkLayerShell.Edge.TOP in parent_anchor
            and GtkLayerShell.Edge.BOTTOM in parent_anchor
        ):
            move_axe = "y"
            if GtkLayerShell.Edge.RIGHT in parent_anchor:
                self.anchor = "top right"
            else:
                self.anchor = "top left"

        return move_axe

    def do_reposition(self, move_axe: str):
        parent_margin = self._parent.margin
        parent_y_margin = parent_margin[3]

        height = self.get_allocated_height()
        width = self.get_allocated_width()

        if self._pointing_widget:
            coords = self.get_coords_for_widget(self._pointing_widget)
            widget_width = self._pointing_widget.get_allocated_width()
            coords_centered = (
                round(coords[0] + widget_width / 2),
                round(coords[1] + self._pointing_widget.get_allocated_height() / 2),
            )
            screen_width = self.display.get_default_screen().get_width()
            third_width = screen_width // 3
            if coords[0] < third_width:
                position = "left"
            elif coords[0] < 2 * third_width:
                position = "center"
            else:
                position = "right"
        else:
            coords_centered = (
                round(self._parent.get_allocated_width() / 2),
                round(self._parent.get_allocated_height() / 2),
            )
            position = "center"

        monitor_geometry = self.get_monitor_geometry()
        x_margin = coords_centered[0] - (width / 2)

        if monitor_geometry and move_axe == "x":
            final_x = x_margin
            base_margins = list(self._base_margin.values())

            if final_x + width > monitor_geometry.width:
                if position in ["center", "right"]:
                    edge_position = monitor_geometry.width - width
                    margin_adjust = base_margins[3] + parent_margin[1]
                    x_margin = edge_position + margin_adjust
                else:
                    x_margin = parent_margin[3]
            elif final_x < 0:
                if position in ["center", "left"]:
                    x_margin = parent_margin[3]
                else:
                    edge_position = monitor_geometry.width - width
                    margin_adjust = base_margins[3] + parent_margin[1]
                    x_margin = edge_position + margin_adjust

        calculated_margin = (
            (0, 0, 0, x_margin)
            if move_axe == "x"
            else (round((parent_y_margin + coords_centered[1]) - (height / 2)), 0, 0, 0)
        )

        final_margin = tuple(
            a + b for a, b in zip(calculated_margin, self._base_margin.values())
        )

        self.margin = final_margin
