from shared import ButtonWidget
from utils import BarConfig


class ClickCounterWidget(ButtonWidget):
    """A widget to count the number of clicks."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config["click_counter"], name="click_counter", **kwargs)

        self.count = self.config["count"]
        self.set_label(f"{self.count}")

        self.connect("button-press-event", self.on_button_press)

    def increment(self, *_):
        self.count = self.count + 1
        self.set_label(f"{self.count}")

    def reset(self, *_):
        self.count = 0
        self.set_label(f"{self.count}")

    def on_button_press(self, _, event):
        if event.button == 1:
            self.increment()
        else:
            self.reset()
