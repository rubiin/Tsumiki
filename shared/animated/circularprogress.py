from functools import partial

from fabric.widgets.circularprogressbar import CircularProgressBar

from shared.animator import cubic_bezier


class AnimatedCircularProgressBar(CircularProgressBar):
    """A circular progress bar widget with animation support."""

    def __init__(self, duration=0.6, curve=(0.34, 1.56, 0.64, 1.0), **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.curve = curve

    def set_notify_value(self, p, *_):
        if p.value == self.value:
            return
        self.set_value(p.value)

    def animate_value(self, value: float):
        from ..animator import Animator

        if self.animator is None:
            self.animator = Animator(
                # edit the following parameters to customize the animation
                timing_function=partial(cubic_bezier, *self.curve),
                duration=self.duration,
                min_value=self.min_value,
                max_value=self.value,
                tick_widget=self,
                notify_value=self.set_notify_value,
            )

        self.animator.pause()
        self.animator.min_value = self.value
        self.animator.max_value = value
        self.animator.play()
        return
