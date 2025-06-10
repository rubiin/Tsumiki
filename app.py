import gi

gi.require_version("Gtk", "3.0")  # Or "4.0" for GTK 4
from gi.repository import Gtk, GLib


class MarqueeLabel(Gtk.Window):
    def __init__(self):
        super().__init__(title="Marquee Example")
        self.set_border_width(10)
        self.set_default_size(400, 50)

        self.label_text = "This is a scrolling marquee effect in GTK!     "
        self.label = Gtk.Label(label=self.label_text)
        self.label.set_justify(Gtk.Justification.LEFT)
        self.label.set_xalign(0.0)  # Align text to the left

        self.add(self.label)


        GLib.timeout_add(150, self.scroll_text)

    def scroll_text(self):
        self.label_text = self.label_text[1:] + self.label_text[0]
        self.label.set_text(self.label_text)
        return True


win = MarqueeLabel()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
