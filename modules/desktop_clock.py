from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window

from shared.widget_container import ToggleableWidget


class DesktopClock(Window, ToggleableWidget):
    """
    A simple desktop clock widget.
    """

    def __init__(self, config, **kwargs):
        self.config = config["modules"]["desktop_clock"]

        super().__init__(
            name="desktop_clock",
            layer=self.config["layer"],
            anchor=self.config["anchor"],
            child=Box(
                name="desktop-clock-box",
                orientation="v",
                children=[
                    DateTime(formatters=["%I:%M"], name="clock"),
                    DateTime(
                        formatters=[self.config["date_format"]],
                        interval=3600000,  # Update every hour
                        name="date",
                    ),
                ],
            ),
            all_visible=True,
            **kwargs,
        )
