from functools import partial

from fabric.widgets.scale import Scale

from utils.bezier import cubic_bezier

from ..widget_container import BaseWidget


class AnimatedScale(Scale, BaseWidget):
    """A widget to display a scale with animated transitions."""

    def __init__(self, name, curve, duration=0.8, **kwargs):
        super().__init__(name=name, **kwargs)
        self.curve = curve
        self.duration = duration
        self.animator = None

    def set_notify_value(self, p, *_):
        if p.value == self.value:
            return
        self.set_value(p.value)

    def animate_value(self, value: float):
        from ..animator import Animator

        if self.animator is None:
            self.animator = Animator(
                timing_function=partial(cubic_bezier, *self.curve),
                duration=self.duration,
                min_value=self.min_value,
                max_value=self.value,
                tick_widget=self,
                notify_value=self.set_notify_value,
            )

        self.animator.pause()
        self.animator.min_value = self.value
        self.animator.max_value = min(max(value, self.min_value), self.max_value)
        self.animator.play()
        return
