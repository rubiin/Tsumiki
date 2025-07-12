import math
from typing import Iterable, Literal

import cairo
from fabric.core.service import Property
from fabric.widgets.widget import Widget
from gi.repository import Gdk, GdkPixbuf, Gtk

from .widget_container import BaseWidget


class CircleImage(Gtk.DrawingArea, BaseWidget):
    """A widget that displays an image in a circle."""

    @Property(int, "read-write")
    def angle(self) -> int:  # type: ignore
        return self._angle

    @angle.setter
    def angle(self, value: int):
        self._angle = value % 360
        self.queue_draw()

    def __init__(
        self,
        image_file: str | None = None,
        pixbuf: None = None,
        name: str | None = None,
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
        size: Iterable[int] | int | None = None,
        **kwargs,
    ):
        Gtk.DrawingArea.__init__(self)
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
            size=size,
            **kwargs,
        )
        self._image_file = image_file
        self._angle = 0
        self.size = size
        self._image: GdkPixbuf.Pixbuf | None = (
            GdkPixbuf.Pixbuf.new_from_file_at_size(image_file, size, size)
            if image_file
            else pixbuf
            if pixbuf
            else None
        )
        self.connect("draw", self.on_draw)

    def on_draw(self, widget: "CircleImage", ctx: cairo.Context):
        if self._image:
            ctx.save()
            ctx.arc(self.size / 2, self.size / 2, self.size / 2, 0, 2 * math.pi)
            ctx.translate(self.size * 0.5, self.size * 0.5)
            ctx.rotate(self._angle * math.pi / 180.0)
            ctx.translate(
                -self.size * 0.5
                - self._image.get_width() // 2
                + self._image.get_height() // 2,
                -self.size * 0.5,
            )
            Gdk.cairo_set_source_pixbuf(ctx, self._image, 0, 0)
            ctx.clip()
            ctx.paint()
            ctx.restore()

    def set_image_from_file(self, new_image_file):
        if new_image_file == "":
            return
        self._image = (
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                new_image_file,
                -1,
                self.size,
            )
            if self._image_file is not None
            else None
        )
        self.queue_draw()

    def set_image_from_pixbuf(self, pixbuf):
        if not pixbuf:
            return
        self._image = pixbuf
        self.queue_draw()

    def set_image_size(self, size: Iterable[int] | int):
        if size is Iterable:
            x, y = size
        else:
            self._image = self._image.scale_simple(
                size, size, GdkPixbuf.InterpType.BILINEAR
            )
        self.queue_draw()
