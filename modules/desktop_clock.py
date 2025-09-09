from utils.imports import Box, DateTime, Window


class DesktopClock(Window):
    """
    A simple desktop clock widget.
    """

    def __init__(self, config, **kwargs):
        self.config = config["modules"]["desktop_clock"]

        super().__init__(
            name="desktop_clock",
            layer=self.config.get("layer", "overlay"),
            anchor=self.config.get("anchor", "center"),
            child=Box(
                name="desktop-clock-box",
                orientation="v",
                children=[
                    DateTime(
                        formatters=[self.config.get("time_format", "%H:%M:%S")],
                        name="clock",
                    ),
                    DateTime(
                        formatters=[self.config.get("date_format", "%Y-%m-%d")],
                        interval=3600000,  # Update every hour
                        name="date",
                    ),
                ],
            ),
            all_visible=True,
            **kwargs,
        )
