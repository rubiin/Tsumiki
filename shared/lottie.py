from typing import Literal

import cairo
import gi
from fabric.widgets.widget import Widget
from gi.repository import GLib, Gtk
from rlottie_python.rlottie_wrapper import LottieAnimation

from .widget_container import BaseWidget

gi.require_versions({"Gtk": "3.0"})


class LottieAnimationWidget(Gtk.DrawingArea, BaseWidget):
    """A widget to display a Lottie animation."""

    def __init__(
        self,
        lottie_animation: LottieAnimation,
        scale: float = 1.0,
        do_loop: bool = False,
        draw_frame: int | None = None,
        visible: bool = True,
        all_visible: bool = False,
        style: str | None = None,
        tooltip_text: str | None = None,
        tooltip_markup: str | None = None,
        h_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        v_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        h_expand: bool = False,
        v_expand: bool = False,
        name: str | None = None,
        **kwargs,
    ):
        Gtk.DrawingArea.__init__(
            self,
            visible=visible,
        )
        Widget.__init__(
            self,
            name=name,
            visible=visible,
            all_visible=all_visible,
            style=style,
            tooltip_text=tooltip_text,
            tooltip_markup=tooltip_markup,
            h_align=h_align,
            v_align=v_align,
            h_expand=h_expand,
            v_expand=v_expand,
        )

        # State Management
        self.timeout = None
        self.is_playing = False
        self.do_reverse = False
        self.curr_frame: int = 0 if draw_frame is None or do_loop else draw_frame
        self.end_frame: int = lottie_animation.lottie_animation_get_totalframe()

        self.do_loop: bool = do_loop
        self.lottie_animation: LottieAnimation = lottie_animation

        # LOTTIE STUFF
        self.anim_total_duration: int = (
            self.lottie_animation.lottie_animation_get_duration()
        )
        self.anim_total_frames: int = (
            self.lottie_animation.lottie_animation_get_totalframe()
        )
        self.width, self.height = self.lottie_animation.lottie_animation_get_size()

        self.width = int(self.width * scale)
        self.height = int(self.height * scale)

        self.timeout_delay = int(
            (1 / self.lottie_animation.lottie_animation_get_framerate()) * 1000
        )

        self.set_size_request(self.width, self.height)
        self.connect("draw", self.draw)
        if draw_frame is not None:
            self.on_update()

        if self.do_loop:
            self.play_loop()

    def play_loop(self):
        self.do_loop = True
        self.timeout = GLib.timeout_add(self.timeout_delay, self.on_update)

    def draw(self, _: Gtk.DrawingArea, ctx: cairo.Context):
        if self.lottie_animation.async_buffer_c is not None:
            image_surface = cairo.ImageSurface.create_for_data(
                # Using this because the actual buffer is read only
                self.lottie_animation.async_buffer_c,
                cairo.FORMAT_ARGB32,
                self.width,
                self.height,
            )
            ctx.set_source_surface(image_surface, 0, 0)
            ctx.paint()
        return False

    def do_realize(self):
        Gtk.DrawingArea.do_realize(self)
        if window := self.get_window():
            window.set_pass_through(True)
        return

    def on_update(self):
        self.is_playing = True
        self.lottie_animation.lottie_animation_render_async(
            self.curr_frame, width=self.width, height=self.height
        )

        self.lottie_animation.lottie_animation_render_flush()
        self.queue_draw()

        if self.do_reverse and self.curr_frame <= self.end_frame:
            self.is_playing = self.do_loop
            self.curr_frame = self.anim_total_frames
            return self.do_loop
        elif not self.do_reverse and self.curr_frame >= self.end_frame:
            self.is_playing = self.do_loop
            self.curr_frame = 0 if self.do_loop else self.curr_frame
            return self.do_loop
        self.curr_frame += -1 if self.do_reverse else 1
        return True

    def stop_play(self):
        GLib.source_remove(self.timeout)

    def play_animation(
        self,
        start_frame: int | None = None,
        end_frame: int | None = None,
        is_reverse: bool = False,
    ):
        if self.is_playing or self.do_loop:
            return
        self.do_reverse = is_reverse
        self.curr_frame = (
            start_frame
            if start_frame is not None
            else self.anim_total_frames
            if self.do_reverse
            else 0
        )
        self.end_frame = (
            end_frame if end_frame else 0 if self.do_reverse else self.anim_total_frames
        )
        # self.curr_frame = self.anim_total_frames if self.is_reverse else 0
        self.timeout = GLib.timeout_add(self.timeout_delay, self.on_update)
