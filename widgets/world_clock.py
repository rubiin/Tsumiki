from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones

import loguru
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon, util_fabricator


class WorldClockWidget(ButtonWidget):
    """a widget that displays the title of the active window."""

    def __init__(self, **kwargs):
        super().__init__(name="world_clock", **kwargs)

        self.clocks = []
        valid_zones = available_timezones()

        if self.config["show_icon"]:
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        self.box.set_spacing(10)

        for tz_name in self.config["timezones"]:
            if tz_name in valid_zones:
                label = Label(style_classes="world-clock-label")
                self.box.pack_start(label, True, True, 0)
                tz = ZoneInfo(tz_name)
                self.clocks.append((label, tz))
            else:
                loguru.info(f"[world_clock] Skipping invalid timezone: {tz_name}")

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, *_):
        utc_now = datetime.now(timezone.utc)
        for label, tz in self.clocks:
            local_time = utc_now.astimezone(tz)
            abbrev = local_time.tzname()  # e.g. 'EST', 'JST'
            formatted = local_time.strftime("%Y-%m-%d %H:%M:%S")
            label.set_text(f"{abbrev}: {formatted}")
        return True
