import time

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from gi.repository import GLib

from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


class StopWatchWidget(ButtonWidget):
    """Widget to display a stopwatch."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        super().__init__(widget_config, title="stopwatch", **kwargs)

        self.start_time = 0
        self.running = False
        self.elapsed_time = 0

        self.config = widget_config["stop_watch"]

        self.box = Box()

        self.children = (self.box,)

        self.icon = text_icon(
            icon=self.config["stopped_icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.time_label = Label(label="00:00", style_classes="panel-text")
        self.box.children = (self.icon, self.time_label)

        self.connect("clicked", self.on_start_stop_clicked)

        self.timeout_id = GLib.timeout_add(100, self.update_time)

    def on_start_stop_clicked(self, button):
        if self.running:
            self.running = False
            self.icon.set_label(
                self.config["stopped_icon"],
            )
        else:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.icon.set_label(
                self.config["running_icon"],
            )

    def update_time(self):
        if self.running:
            # Calculate the elapsed time
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(self.elapsed_time, 60)
            self.time_label.set_text(f"{int(minutes):02}:{int(seconds):02}")
        return True
