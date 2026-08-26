"""Turn any GTK3 widget class into a Fabric Widget."""

from collections.abc import Iterable
from typing import Literal, TypeVar

from fabric.utils import Gtk
from fabric.widgets.widget import Widget

GtkT = TypeVar("GtkT", bound=Gtk.Widget)


def _gtk_accepts(widget_cls, key):
    """Check if a GObject class has the given property."""
    try:
        return widget_cls.find_property(key) is not None
    except (ValueError, TypeError):
        return False


def fabricate(widget_cls: type[GtkT]) -> type[GtkT]:
    """Wrap a GTK3 widget class so it gains Fabric's Widget features.

    Returns a new class with explicit typed parameters matching the
    pattern with explicit typed parameters. Extra kwargs are forwarded to
    the GTK widget if it supports them, otherwise they are silently
    absorbed by Widget/Service (same as shared/list.py).

    Usage::

        Label = fabricate(Gtk.Label)
        widget1 = Label(name="my-label", label="hello", style_classes=["big"])
    """

    class Fabricated(widget_cls, Widget):  # type: ignore[misc]
        def __init__(
            self,
            *,
            name: str | None = None,
            visible: bool = True,
            all_visible: bool = False,
            style: str | None = None,
            style_classes: Iterable[str] | str | None = None,
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
            **gtk_kwargs,
        ):
            # Forward only kwargs the GTK widget actually supports.
            valid_gtk = {
                k: v for k, v in gtk_kwargs.items() if _gtk_accepts(widget_cls, k)
            }
            widget_cls.__init__(self, **valid_gtk)
            Widget.__init__(
                self,
                name,
                visible,
                all_visible,
                style,
                style_classes,
                tooltip_text,
                tooltip_markup,
                h_align,
                v_align,
                h_expand,
                v_expand,
                size,
            )

    Fabricated.__name__ = f"Fabric{widget_cls.__name__}"
    Fabricated.__qualname__ = f"Fabric{widget_cls.__qualname__}"
    Fabricated.__module__ = widget_cls.__module__

    return Fabricated  # type: ignore[return-value]
