from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones

from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon, reusable_fabricator


class WorldClockWidget(ButtonWidget):
    """a widget that displays the title of the active window."""

    def __init__(self, **kwargs):
        super().__init__(name="world_clock", **kwargs)

        self.clocks = []
        valid_zones = available_timezones()

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config.get("icon", "󰃰"),  # fallback icon,
                props={"style_classes": "panel-font-icon"},
            )
            self.container_box.add(self.icon)

        self.container_box.set_spacing(10)

        timezones = self.config.get("timezones", [])

        self.is_24hr = self.config.get("use_24hr", True)
        self.time_format = "%H:%M:%S" if self.is_24hr else "%I:%M:%S %p"

        for tz_name in timezones:
            if tz_name in valid_zones:
                label = Label(style_classes="world-clock-label")
                self.container_box.pack_start(label, True, True, 0)
                tz = ZoneInfo(tz_name)
                self.clocks.append((label, tz))
            else:
                logger.info(f"[world_clock] Skipping invalid timezone: {tz_name}")

        # reusing the fabricator to call specified intervals
        reusable_fabricator.connect("changed", self._update_ui)

    def _update_ui(self, *_):
        try:
            utc_now = datetime.now(timezone.utc)
            for label, tz in self.clocks:
                local_time = utc_now.astimezone(tz)
                abbrev = local_time.tzname()
                formatted = local_time.strftime(self.time_format)
                label.set_text(f"{abbrev}: {formatted}")
        except Exception as e:
            logger.error(f"[world_clock] Failed to update UI: {e}")
        return True
