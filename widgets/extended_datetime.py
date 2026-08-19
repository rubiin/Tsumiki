import time
from datetime import datetime

from fabric.widgets.datetime import DateTime
from nepali.datetime import nepalidatetime


class ExtendedDateTime(DateTime):
    """DateTime that optionally displays date/time in Nepali (Bikram Sambat) calendar.

    When *nepali_time* is True the year, month, and day values come from the
    Nepali calendar while time components are taken from the system clock
    unchanged.  When False the standard ``time.strftime`` path is used.

    Accepts the same strftime format codes as Python's datetime.
    """

    def __init__(self, nepali_time: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._nepali_time = nepali_time

    def do_format(self) -> str:
        if self._nepali_time:
            nepali_now = nepalidatetime.from_datetime(datetime.now())
            return nepali_now.strftime(self._formatters[self._current_index])
        return time.strftime(self._formatters[self._current_index])
