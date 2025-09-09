from typing import Protocol, cast

import gi
from fabric import Property, Service, Signal
from fabric.utils import clamp, remove_handler
from gi.repository import GLib, Gtk

from utils.bezier import ease_linear, lerp

gi.require_versions({"Gtk": "3.0"})


class TimingFunctionCallback(Protocol):
    """A callback that takes a progress value and returns a float."""

    def __call__(self, progress: float, *args, **kwargs) -> float: ...


class Animator(Service):
    """
    An animator is a simple way for animating a value on
    a set timeline based on a given timing function
    """

    @Signal
    def finished(self) -> None: ...

    @Property(TimingFunctionCallback, "read-write")
    def timing_function(self) -> TimingFunctionCallback:
        return self._timing_function

    @timing_function.setter
    def timing_function(self, value: TimingFunctionCallback):
        self._timing_function = value
        return

    @Property(float, "read-write")
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: float):
        if value <= 0.0:
            raise ValueError("duration can't be smaller than or equal to 0.0")

        self._duration = value
        return

    @Property(float, "read-write")
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = clamp(
            value,
            min(self._min_value, self._max_value),
            max(self._min_value, self._max_value),
        )
        return

    @Property(float, "read-write")
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value: float):
        self._max_value = value
        return

    @Property(float, "read-write")
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, value: float):
        self._min_value = value
        return

    @Property(bool, "read-write", default_value=False)
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, value: bool):  # this setter is intended for internal usage only
        self._playing = value
        return

    @Property(bool, "read-write", default_value=False)
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, value: bool):
        self._repeat = value
        return

    def __init__(
        self,
        duration: float = 0.8,
        timing_function: TimingFunctionCallback = ease_linear,
        value: float = 0.0,
        min_value: float = 0.0,
        max_value: float = 1.0,
        repeat: bool = False,
        tick_widget: Gtk.Widget | None = None,
        tick_interval: int = 16,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._playing = False
        self._value = value
        self._min_value = 0.0
        self._max_value = 1.0
        self._repeat = False
        self._duration = 0.8
        self._timing_function = timing_function
        self._tick_widget = tick_widget
        self._tick_interval = tick_interval

        self.timing_function = timing_function
        self.repeat = repeat
        self.duration = duration
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.playing = False

        self._start_time = None
        self._tick_handler = None
        self._timeline_pos = 0.0

    def _get_time_now(self):
        return GLib.get_monotonic_time() / 1_000_000

    def _update_value(self, delta_time: float):
        if not self._playing:
            return

        elapsed_time = delta_time - cast(float, self._start_time)

        self._timeline_pos = min(1.0, elapsed_time / self._duration)

        self.value = lerp(
            self._min_value,
            self._max_value,
            self._timing_function(progress=self._timeline_pos),
        )

        if not self._timeline_pos >= 1.0:
            return

        if not self._repeat:
            # all done..
            self.value = self._max_value
            self.finished()
            self.pause()
            return

        self._start_time = delta_time
        self._timeline_pos = 0.0
        return

    def _handle_tick(self, *_):
        current_time = self._get_time_now()
        self._update_value(current_time)
        return True

    def _remove_tick_handlers(self):
        if not self._tick_handler:
            return

        if self._tick_widget:
            self._tick_widget.remove_tick_callback(self._tick_handler)
        else:
            remove_handler(self._tick_handler)
        self._tick_handler = None
        return

    def play(self):
        if self._playing:
            return

        self.playing = True
        self._start_time = self._get_time_now()

        if self._tick_handler:
            return

        if self._tick_widget:
            self._tick_handler = self._tick_widget.add_tick_callback(self._handle_tick)
            return

        self._tick_handler = GLib.timeout_add(self._tick_interval, self._handle_tick)
        return

    def pause(self):
        self.playing = False
        return self._remove_tick_handlers()

    def stop(self):
        if not self._tick_handler:
            self._timeline_pos = 0
            self.playing = False
            return
        return self._remove_tick_handlers()

    def play_pause(self):
        if self._playing:
            self.pause()
        else:
            self.play()
        return
