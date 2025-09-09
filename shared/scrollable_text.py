from fabric.utils import bulk_connect, remove_handler
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from gi.repository import GLib


class ScrollableText(EventBox):
    """A scrollable text widget that allows text to be scrolled horizontally."""

    @property
    def label(self):
        """Get the label of the text widget."""
        return self.text_widget.get_label()

    @label.setter
    def label(self, value: str):
        """Set the label of the text widget."""
        self.text_widget.set_label(value)

    def __init__(self, **kwargs):
        super().__init__()
        self.text_widget = Label(**kwargs)

        self.text_widget.h_align = "start"

        self.add(self.text_widget)

        # Variables for timer
        self.scroll_id = None

        # Connect hover signals
        bulk_connect(
            self,
            {
                "enter-notify-event": self.on_hover_start,
                "leave-notify-event": self.on_hover_stop,
            },
        )

    def on_hover_start(self, widget, event):
        if self.scroll_id is None:
            self.scroll_id = GLib.timeout_add(150, self.scroll_text)

    def on_hover_stop(self, widget, event):
        if self.scroll_id:
            remove_handler(self.scroll_id)
            self.scroll_id = None

    def scroll_text(self):
        self.display_text = self.display_text[1:] + self.display_text[0]
        self.text_widget.set_text(self.display_text)
        return True  # Keep timer running

    def set_label(self, label: str):
        """Set the label to be displayed in the scrollable text widget."""
        self.text_widget.set_label(label)
