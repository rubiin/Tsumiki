from datetime import datetime

from fabric.utils import GLib
from fabric.widgets.label import Label
from nepali.datetime import nepalidatetime


class NepaliDateTimeLabel(Label):
    """Label that displays the current date/time in Nepali (Bikram Sambat) calendar.

    Accepts the same strftime format codes as Python's datetime, but the year,
    month, and day values come from the Nepali calendar.  The time components
    (hour, minute, second) are taken from the system clock unchanged.
    """

    def __init__(
        self,
        fmt: str = "%Y-%m-%d",
        interval: int = 1000,
        name: str | None = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self._fmt = fmt
        self._interval = interval
        self._repeater_id: int | None = None
        self._tick()
        self._repeater_id = GLib.timeout_add(self._interval, self._tick)

    def _tick(self) -> bool:
        nepali_now = nepalidatetime.from_datetime(datetime.now())
        self.set_label(nepali_now.strftime(self._fmt))
        return True  # keep repeater alive

    def destroy(self):
        if self._repeater_id is not None:
            GLib.source_remove(self._repeater_id)
            self._repeater_id = None
        super().destroy()
