from datetime import datetime

from fabric.widgets.datetime import DateTime
from nepali.datetime import nepalidatetime


class NepaliDateTimeLabel(DateTime):
    """DateTime that displays the current date/time in Nepali (Bikram Sambat) calendar.

    Accepts the same strftime format codes as Python's datetime, but the year,
    month, and day values come from the Nepali calendar.  The time components
    (hour, minute, second) are taken from the system clock unchanged.
    """

    def do_format(self) -> str:
        nepali_now = nepalidatetime.from_datetime(datetime.now())
        return nepali_now.strftime(self._formatters[self._current_index])
