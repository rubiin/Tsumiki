import os
import typing
from pathlib import Path

import gi
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import Gdk, GLib, GObject, Gtk
from loguru import logger

from shared.list import ListBox
from shared.widget_container import ButtonWidget
from utils.functions import read_json_file, write_json_file
from utils.widget_utils import create_surface_from_widget, nerd_font_icon

gi.require_versions({"Gtk": "3.0", "GObject": "2.0", "Gdk": "3.0"})


class InlineEditor(Box):
    """A simple inline editor for editing text in a Gtk.TextView."""

    __gsignals__: typing.ClassVar = {
        "confirmed": (GObject.SignalFlags.RUN_LAST, None, (str,)),
        "canceled": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, initial_text=""):
        super().__init__(name="inline-editor", spacing=4)

        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        buffer = self.text_view.get_buffer()
        buffer.set_text(initial_text)

        # Connect key press events to handle Return and SHIFT+Return.
        self.text_view.connect("key-press-event", self.on_key_press)

        confirm_btn = Button(
            name="kanban-btn", child=Label(name="kanban-btn-label", markup="")
        )
        confirm_btn.connect("clicked", self.on_confirm)
        confirm_btn.get_style_context().add_class("flat")

        cancel_btn = Button(
            name="kanban-btn", child=Label(name="kanban-btn-neg", markup="")
        )
        cancel_btn.connect("clicked", self.on_cancel)
        cancel_btn.get_style_context().add_class("flat")

        # Pack the TextView inside a ScrolledWindow for better appearance.
        sw = ScrolledWindow(
            h_scrollbar_policy="never",
            v_scrollbar_policy="automatic",
        )
        sw.set_min_content_height(50)
        sw.add(self.text_view)

        self.button_box = Box(children=[confirm_btn, cancel_btn], spacing=4)
        self.center_box = CenterBox(center_children=[self.button_box], orientation="v")

        self.pack_start(sw, True, True, 0)
        self.pack_start(self.center_box, False, False, 0)
        self.show_all()

    def on_confirm(self, widget):
        buffer = self.text_view.get_buffer()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end, True).strip()
        if text:
            self.emit("confirmed", text)
        else:
            self.emit("canceled")

    def on_cancel(self, widget):
        self.emit("canceled")

    def on_key_press(self, widget: Gtk.Widget, event):
        # Check for Escape to cancel.
        if event.keyval == Gdk.KEY_Escape:
            self.emit("canceled")
            return True

        # If Return is pressed...
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            state = event.get_state()
            if state & Gdk.ModifierType.SHIFT_MASK:
                # SHIFT+Return: insert a newline.
                buffer = self.text_view.get_buffer()
                cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
                buffer.insert(cursor_iter, "\n")
                return True  # Prevent further handling.
            else:
                # Plain Return: confirm the edit.
                self.on_confirm(widget)
                return True
        return False


class KanbanNote(EventBox):
    """A widget representing a single note in the Kanban board."""

    __gsignals__: typing.ClassVar = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, text: str):
        super().__init__()
        self.text = text
        # Variables to store the click offset for drag preview.
        self.setup_ui()
        self.setup_dnd()
        self.connect("button-press-event", self.on_button_press)

    def setup_ui(self):
        self.box = Box(name="kanban-note", spacing=4)
        self.label = Label(label=self.text, line_wrap=True, v_expand=True)
        self.label.set_line_wrap(True)
        # Wrap long lines.
        self.label.set_line_wrap_mode(Gtk.WrapMode.WORD)

        self.delete_btn = Button(
            name="kanban-btn", child=Label(name="kanban-btn-neg", markup="")
        )
        self.delete_btn.connect("clicked", self.on_delete_clicked)

        self.center_btn = CenterBox(orientation="v", start_children=[self.delete_btn])

        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.center_btn, False, False, 0)
        self.add(self.box)
        self.show_all()

    def setup_dnd(self):
        self.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            [Gtk.TargetEntry.new("UTF8_STRING", Gtk.TargetFlags.SAME_APP, 0)],
            Gdk.DragAction.MOVE,
        )

        bulk_connect(
            self,
            {
                "drag-data-get": self.on_drag_data_get,
                "drag-data-delete": self.on_drag_data_delete,
                "drag-begin": self.on_drag_begin,
            },
        )

    def on_button_press(self, widget, event):
        if event.type != Gdk.EventType._2BUTTON_PRESS:
            return True
        self.start_edit()
        return False

    def on_drag_begin(self, widget, context):
        surface = create_surface_from_widget(self)
        Gtk.drag_set_icon_surface(context, surface)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        data.set_text(self.label.get_text(), -1)

    def on_drag_data_delete(self, widget, drag_context):
        self.get_parent().destroy()

    def on_delete_clicked(self, button):
        self.get_parent().destroy()

    def start_edit(self):
        row = self.get_parent()
        editor = InlineEditor(self.label.get_text())

        def on_confirmed(editor, text: str):
            self.label.set_text(text)
            row.remove(editor)
            row.add(self)
            row.show_all()
            self.emit("changed")

        def on_canceled(editor):
            row.remove(editor)
            row.add(self)
            row.show_all()

        bulk_connect(
            editor,
            {
                "confirmed": on_confirmed,
                "canceled": on_canceled,
            },
        )

        row.remove(self)
        row.add(editor)
        row.show_all()
        GLib.timeout_add(50, lambda: (editor.text_view.grab_focus(), False))


class KanbanColumn(Gtk.Frame):
    """A column in the Kanban board, containing notes."""

    __gsignals__: typing.ClassVar = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, title):
        super().__init__(name="kanban-column", vexpand=True, hexpand=True)
        self.title = title
        self.setup_ui()
        self.setup_dnd()

    def setup_ui(self):
        self.box = Box(orientation="vertical", spacing=4)
        self.listbox = ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.add_btn = Button(
            name="kanban-btn-add",
            child=Label(name="kanban-btn-label", markup=""),
        )
        header = CenterBox(
            name="kanban-header",
            center_children=[Label(name="column-header", label=self.title)],
            end_children=[self.add_btn],
        )
        self.box.pack_start(header, False, False, 0)

        self.add_btn.connect("clicked", self.on_add_clicked)

        scrolled = ScrolledWindow(
            name="kanban-scroll",
            v_expand=True,
            v_scrollbar_policy="automatic",
            h_scrollbar_policy="never",
        )
        scrolled.add(self.listbox)

        self.box.pack_start(scrolled, True, True, 0)
        self.box.pack_start(self.add_btn, False, False, 0)
        self.add(self.box)
        self.show_all()

    def setup_dnd(self):
        self.listbox.drag_dest_set(
            Gtk.DestDefaults.ALL,
            [Gtk.TargetEntry.new("UTF8_STRING", Gtk.TargetFlags.SAME_APP, 0)],
            Gdk.DragAction.MOVE,
        )

        bulk_connect(
            self.listbox,
            {
                "drag-data-received": self.on_drag_data_received,
                "drag-motion": self.on_drag_motion,
                "drag-leave": self.on_drag_leave,
            },
        )

    def on_add_clicked(self, button):
        editor = InlineEditor()
        row = Gtk.ListBoxRow(name="kanban-row")
        row.add(editor)
        self.listbox.add(row)
        self.listbox.show_all()
        editor.text_view.grab_focus()

        def on_confirmed(editor, text):
            note = KanbanNote(text)
            note.connect("changed", lambda x: self.emit("changed"))
            row.remove(editor)
            row.add(note)
            self.listbox.show_all()
            self.emit("changed")  # Emit on add

        def on_canceled(editor):
            row.destroy()

        bulk_connect(
            editor,
            {
                "confirmed": on_confirmed,
                "canceled": on_canceled,
            },
        )

    def add_note(self, text: str, suppress_signal=False):
        note = KanbanNote(text)
        note.connect("changed", lambda x: self.emit("changed"))
        row = Gtk.ListBoxRow(name="kanban-row")
        row.add(note)
        row.connect("destroy", lambda x: self.emit("changed"))
        self.listbox.add(row)
        self.listbox.show_all()
        if not suppress_signal:
            self.emit("changed")

    def get_notes(self):
        return [
            row.get_children()[0].label.get_text()
            for row in self.listbox.get_children()
            if isinstance(row.get_children()[0], KanbanNote)
        ]

    def clear_notes(self, suppress_signal=False):
        for row in self.listbox.get_children():
            row.destroy()
        if not suppress_signal:
            self.emit("changed")

    def on_drag_data_received(
        self, widget: Gtk.Widget, drag_context, x, y, data, info, time
    ):
        text = data.get_text()
        if text:
            row = self.listbox.get_row_at_y(y)
            new_note = KanbanNote(text)
            new_note.connect("changed", lambda x: self.emit("changed"))
            new_row = Gtk.ListBoxRow(name="kanban-row")
            new_row.add(new_note)
            new_row.connect("destroy", lambda x: self.emit("changed"))

            if row:
                self.listbox.insert(new_row, row.get_index())
            else:
                self.listbox.add(new_row)

            self.listbox.show_all()
            drag_context.finish(True, False, time)
            self.emit("changed")  # Emit on move

    def on_drag_motion(self, widget: Gtk.Widget, drag_context, x, y, time):
        Gdk.drag_status(drag_context, Gdk.DragAction.MOVE, time)
        return True

    def on_drag_leave(self, widget: Gtk.Widget, drag_context, time):
        widget.get_parent().get_parent().drag_unhighlight()


class Kanban(Box):
    """A simple Kanban board with three columns: To Do, In Progress, and Done."""

    STATE_FILE = Path(os.path.expanduser("~/.kanban.json"))

    def __init__(self):
        super().__init__(name="kanban-board", spacing=4)

        self.grid = Grid(column_spacing=4, column_homogeneous=True, v_expand=True)

        self.add(self.grid)

        self.columns = [
            KanbanColumn("To Do"),
            KanbanColumn("In Progress"),
            KanbanColumn("Done"),
        ]

        for i, column in enumerate(self.columns):
            self.grid.attach(column, i, 0, 1, 1)
            column.connect("changed", lambda x: self.save_state())

        self.load_state()
        self.show_all()

    def save_state(self):
        state = {
            "columns": [
                {"title": col.title, "notes": col.get_notes()} for col in self.columns
            ]
        }
        write_json_file(
            state,
            self.STATE_FILE,
        )

    def load_state(self):
        state = read_json_file(self.STATE_FILE)
        if state:
            for col_data in state["columns"]:
                for column in self.columns:
                    if column.title == col_data["title"]:
                        column.clear_notes(suppress_signal=True)
                        for note_text in col_data["notes"]:
                            column.add_note(note_text, suppress_signal=True)
                        break
        else:
            logger.info(
                f"[Kanban] No saved state found at {self.STATE_FILE}, starting fresh."
            )


class KanbanWidget(ButtonWidget):
    """A widget to display and manage clipboard history."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            name="kanban",
            **kwargs,
        )

        self.container_box.add(
            nerd_font_icon(
                icon=self.config.get("icon", "󰒲"),
                props={"style_classes": "panel-font-icon"},
            )
        )

        if self.config.get("label", True):
            self.container_box.add(Label(label="Kanban", style_classes="panel-text"))

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Kanban Board")

        self.popup = None

        self.connect(
            "clicked",
            self.show_popover,
        )

    def show_popover(self, *_):
        """Show the popover."""
        if self.popup is None:
            from shared.popover import Popover

            self.popup = Popover(
                content=Kanban(),
                point_to=self,
            )
        self.popup.open()
