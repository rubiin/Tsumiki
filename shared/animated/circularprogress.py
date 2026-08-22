from functools import partial

from fabric.widgets.circularprogressbar import CircularProgressBar

from ..animator import cubic_bezier


class AnimatedCircularProgressBar(CircularProgressBar):
    """A circular progress bar widget with animation support."""

    def __init__(self, duration=0.6, curve=(0.34, 1.56, 0.64, 1.0), **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.curve = curve
        self.animator = None
        self._destroyed = False

        self.connect("destroy", self._on_destroy)

    def _on_destroy(self, *_):
        self._destroyed = True
        if self.animator is not None:
            self.animator.pause()

    def set_notify_value(self, p, *_):
        if self._destroyed or p.value == self.value:
            return
        self.set_value(p.value)

    def animate_value(self, value: float):
        if self._destroyed:
            return

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
