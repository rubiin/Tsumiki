from functools import partial

import gi
from gi.repository import GLib, Gtk, PangoCairo

from shared.animator import Animator, cubic_bezier

gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")


class ScrollingLabel(Gtk.DrawingArea):
    """A custom Gtk widget that displays text and scrolls it horizontally if it exceeds
    the available width."""

    def __init__(
        self,
        text="---",
        bezier=(0, 0.37, 1, 0.65),
        speed=0.8,
        pause_ms=2000,
        max_width=200,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.set_name("song-title")
        self.text = text
        self.speed = speed
        self.max_width_limit = max_width
        self.pause_ms = pause_ms

        self.set_halign(Gtk.Align.START)

        self._pause_source_id = None

        # Initialize Animator with a dummy duration (it will be updated dynamically)
        self.animator = Animator(
            duration=1.0,
            timing_function=partial(cubic_bezier, *bezier),
            min_value=0.0,
            max_value=1.0,
            repeat=False,
            tick_widget=self,
        )

        self.animator.connect("notify::value", self.on_animator_step)
        self.animator.connect("finished", self.on_animator_finished)

    def on_animator_step(self, animator, *args):
        self.queue_draw()

    def on_animator_finished(self, *args):
        # Swap min/max to reverse direction
        current_min = self.animator.min_value
        current_max = self.animator.max_value
        self.animator.min_value = current_max
        self.animator.max_value = current_min

        if self._pause_source_id:
            GLib.source_remove(self._pause_source_id)

        self._pause_source_id = GLib.timeout_add(self.pause_ms, self._resume_animation)

    def _resume_animation(self):
        self._pause_source_id = None
        self.animator.play()
        return GLib.SOURCE_REMOVE

    def get_text(self):
        return self.text

    def set_text(self, new_text):
        if self.text != str(new_text):
            self.text = str(new_text)

            # Reset Animator State
            self.animator.pause()
            if self._pause_source_id:
                GLib.source_remove(self._pause_source_id)
                self._pause_source_id = None

            self.animator.min_value = 0.0
            self.animator.max_value = 1.0
            self.animator.value = 0.0

            self.queue_resize()

    def do_get_preferred_width(self):
        layout = self.create_pango_layout(self.text)
        style_context = self.get_style_context()
        layout.set_font_description(style_context.get_font(Gtk.StateFlags.NORMAL))
        text_w, _ = layout.get_pixel_size()

        natural = min(text_w, self.max_width_limit)
        return natural, natural

    def do_get_preferred_height(self):
        layout = self.create_pango_layout(self.text)
        style_context = self.get_style_context()
        layout.set_font_description(style_context.get_font(Gtk.StateFlags.NORMAL))
        _, text_h = layout.get_pixel_size()
        return text_h, text_h

    def do_draw(self, cr):
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        style_context = self.get_style_context()
        rgba = style_context.get_color(Gtk.StateFlags.NORMAL)
        font_desc = style_context.get_font(Gtk.StateFlags.NORMAL)

        layout = self.create_pango_layout(self.text)
        layout.set_font_description(font_desc)
        text_w, text_h = layout.get_pixel_size()

        cr.rectangle(0, 0, width, height)
        cr.clip()

        y_pos = (height - text_h) / 2

        if text_w > width:
            max_scroll = width - text_w - 4
            scroll_distance = abs(max_scroll)

            # Convert speed (pixels per 16ms tick) to pixels per second
            pixels_per_second = self.speed * (1000 / 16)

            # Dynamically calculate the duration needed to cover the distance
            # at the given speed
            target_duration = scroll_distance / pixels_per_second

            # Update the animator's duration if it has changed
            if abs(self.animator.duration - target_duration) > 0.01:
                self.animator.duration = target_duration

            if not self.animator.playing and self._pause_source_id is None:
                self.animator.play()

            x_offset = max_scroll * self.animator.value
        else:
            self.animator.pause()
            if self._pause_source_id:
                GLib.source_remove(self._pause_source_id)
                self._pause_source_id = None
            self.animator.value = 0.0
            self.animator.min_value = 0.0
            self.animator.max_value = 1.0
            x_offset = 0

        cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
        cr.move_to(x_offset, y_pos)
        PangoCairo.show_layout(cr, layout)
