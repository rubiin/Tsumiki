from shared.widget_container import ButtonWidget
from utils.i18n import _


class ClickCounterWidget(ButtonWidget):
    """A widget to count the number of clicks."""

    def __init__(self, **kwargs):
        super().__init__(name="click_counter", **kwargs)

        self.count = self.config.get("count", 0)
        self.set_label(f"{self.count}")

        self.connect("button-press-event", self.on_button_press)

        self.set_tooltip_if_enabled(_("widget.click_counter.tooltip"), default=True)

    def _increment(self, *_):
        self.count = self.count + 1
        self.set_label(f"{self.count}")

    def _reset(self, *_):
        self.count = 0
        self.set_label(f"{self.count}")

    def on_button_press(self, _, event):
        if event.button == 1:
            self._increment()
        else:
            self._reset()
