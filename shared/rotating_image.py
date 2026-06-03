import math

import cairo
from fabric.widgets.svg import Svg

from .animator import Animator


class RotatingIcon(Svg):
    """A widget that displays an SVG icon and rotates it when active."""

    def __init__(
        self, icon_name: str, icon_size: int = 16, duration: float = 1.0, **kwargs
    ):
        super().__init__(icon_name=icon_name, icon_size=icon_size, **kwargs)
        self._rotating = False

        self.animator = (
            Animator(
                bezier_curve=(0.0, 0.0, 1.0, 1.0),
                duration=duration,
                min_value=0.0,
                max_value=1.0,
                repeat=True,
                tick_widget=self,
                notify_value=lambda *_: self.queue_draw(),
            )
            .build()
            .unwrap()
        )

    def set_active(self, active: bool):
        self._rotating = active
        if active:
            self.animator.value = 0.0
            self.animator.play()
        else:
            self.animator.pause()
            self.animator.value = 0.0
            self.queue_draw()

    def do_draw(self, cr: cairo.Context):
        if not self._rotating:
            return super().do_draw(cr)

        alloc = self.get_allocation()
        cx = alloc.width / 2
        cy = alloc.height / 2
        angle = self.animator.value * 2 * math.pi

        cr.save()
        cr.translate(cx, cy)
        cr.rotate(angle)
        cr.translate(-cx, -cy)
        super().do_draw(cr)
        cr.restore()
