from fabric.core.service import Signal
from fabric.widgets.button import Button
from gi.repository import Gdk


class SwipeButton(Button):
    """A button that emits swipe signals when swiped."""

    @Signal
    def swipe(self, x: float, y: float, raw_x: int, raw_y: int) -> None: ...
    @Signal
    def swipe_end(self, x: float, y: float, raw_x: int, raw_y: int) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_events(("button-press", "button-release", "pointer-motion"))

        self._x_origin = None
        self._y_origin = None
        self._alloc = Gdk.Rectangle()

        self.connect("button-press-event", self.on_button_press)
        self.connect("motion-notify-event", self.on_motion_notify)
        self.connect("button-release-event", self.on_button_release)

    def do_size_allocate(self, allocation: Gdk.Rectangle):
        self._alloc = allocation
        Button.do_size_allocate(self, allocation)
        return

    def do_calculate_distance(
        self, x_origin: int, y_origin: int, x: int, y: int
    ) -> tuple[float, float, int, int]:
        xd = x - x_origin
        yd = y - y_origin
        normalized_xd = xd / float(self._alloc.width)  # type: ignore
        normalized_yd = yd / float(self._alloc.height)  # type: ignore
        return normalized_xd, normalized_yd, xd, yd

    def on_button_press(self, _, event):
        if event.button == 1:
            # NOTE: relative to self's coords
            self._x_origin, self._y_origin = event.x, event.y
        return True

    def on_motion_notify(self, _, event):
        if self._x_origin is None or self._y_origin is None:
            return False

        normalized_dx, normalized_dy, dx, dy = self.do_calculate_distance(
            self._x_origin, self._y_origin, event.x, event.y
        )
        self.swipe(normalized_dx, normalized_dy, dx, dy)
        return True

    def on_button_release(self, _, event):
        if self._x_origin is not None and self._y_origin is not None:
            self.swipe_end(
                *self.do_calculate_distance(
                    self._x_origin, self._y_origin, event.x, event.y
                )
            )

        self._x_origin = None
        self._y_origin = None
        return True
