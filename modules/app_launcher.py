import operator
from collections.abc import Iterator
from enum import Enum
from typing import Callable

from fabric.utils import DesktopApp, idle_add, remove_handler
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.entry import Entry
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Gdk

from shared.buttons import HoverButton
from shared.tagentry import TagEntry
from utils.app import AppUtils


class LauncherCommandType(Enum):
    """Types of commands that can be executed by the launcher."""

    SINGLE_ENTRY = 0
    SINGLE_ENTRY_WITH_CONFIRMATION = 1
    LIST = 2
    LIST_WITH_CONFIRMATION = 3
    WIDGET = 4
    WIDGET_WITH_CONFIRMATION = 5


class AppLauncher(Window):
    """Launcher widget for launching applications and commands."""

    def __init__(self, config, **kwargs):
        self.config = config["modules"]["app_launcher"]
        super().__init__(
            name="launcher",
            layer="top",
            anchor="center",
            exclusivity="none",
            keyboard_mode="on-demand",
            visible=False,
            all_visible=False,
            **kwargs,
        )
        self._arranger_handler: int = 0

        self.app_util = AppUtils()
        self._all_apps = self.app_util.all_applications

        self.connect("key-press-event", self._on_key_press)

        self._commands = {}
        self._command_handler = None

        self.viewport = Box(spacing=2, orientation="v")
        self.search_entry = Entry(
            name="launcher-prompt",
            placeholder="Search Applications...",
            h_expand=True,
            notify_text=lambda entry, *_: self.arrange_viewport(entry.get_text()),
        )

        self.tag_entry = TagEntry(
            h_expand=True, placeholder="Tags", available_tags=["tag1", "tag2", "tag3"]
        )

        self.scrolled_window = ScrolledWindow(
            min_content_size=(280, 320),
            max_content_size=(280 * 2, 320),
            child=self.viewport,
        )

        self.add(
            Box(
                name="launcher-contents",
                spacing=2,
                orientation="v",
                children=[
                    # the header with the search entry
                    Box(
                        spacing=2,
                        orientation="h",
                        children=[
                            self.search_entry,
                            HoverButton(
                                name="launcher-close-button",
                                image=Image(icon_name="window-close"),
                                tooltip_text="Exit",
                                on_clicked=lambda *_: self.hide(),
                                v_align="center",
                                h_align="center",
                            ),
                        ],
                    ),
                    # self.tag_entry,
                    # the actual slots holder
                    self.scrolled_window,
                ],
            )
        )

        self.search_entry.grab_focus_without_selecting()
        self.hide()

    def _on_key_press(self, _, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()

    def arrange_viewport(self, query: str = ""):
        # reset everything so we can filter current viewport's slots...
        # remove the old handler so we can avoid race conditions
        remove_handler(self._arranger_handler) if self._arranger_handler else None

        # remove all children from the viewport
        self.viewport.children = []

        # make a new iterator containing the filtered apps
        command = None
        prompt = ""
        try:
            command, prompt = query.split(" ", 1)
        except Exception:
            command = query

        if len(command) > 0 and self._command_handler:
            command_data: tuple[LauncherCommandType, Callable] | None = None
            if (command_data := self._command_handler(command)) is not None:
                command_type, command_factory = command_data
                result = command_factory(prompt)

                if command_type == LauncherCommandType.SINGLE_ENTRY:
                    print(result.title, result.label)
                elif command_type == LauncherCommandType.LIST:
                    ...
                else:
                    ...
                return False
        filtered_apps_iter = iter(
            [
                app
                for app in self._all_apps
                if query.casefold()
                in (
                    (app.display_name or "")
                    + (" " + app.name + " ")
                    + (app.generic_name or "")
                ).casefold()
            ]
        )
        should_resize = operator.length_hint(filtered_apps_iter) == len(self._all_apps)

        # all aboard...
        # start the process of adding slots with a lazy executor
        # using this method makes the process of adding slots way more less
        # resource expensive without blocking the main thread and resulting in a lock
        self._arranger_handler = idle_add(
            lambda *args: self.add_next_application(*args)
            or (self.resize_viewport() if should_resize else False),
            filtered_apps_iter,
            pin=True,
        )

        return False

    def add_next_application(self, apps_iter: Iterator[DesktopApp]):
        if not (app := next(apps_iter, None)):
            return False

        self.viewport.add(self.bake_application_slot(app))
        return True

    def resize_viewport(self):
        self.scrolled_window.set_min_content_width(
            self.viewport.get_allocation().width  # type: ignore
        )
        return False

    def bake_application_slot(self, app: DesktopApp, **kwargs) -> Button:
        # TODO: remove nest
        def on_clicked(*_):
            app.launch()
            self.hide()
            self.search_entry.set_text("")

        return Button(
            style_classes="launcher-button",
            child=Box(
                orientation="h",
                spacing=12,
                children=[
                    Image(
                        pixbuf=app.get_icon_pixbuf(self.config.get("icon_size", 16)),
                        h_align="start",
                    ),
                    Label(
                        label=app.display_name or "Unknown",
                        v_align="center",
                        h_align="center",
                    ),
                ],
            ),
            tooltip_text=app.description if self.config.get("tooltip", False) else None,
            on_clicked=on_clicked,
            **kwargs,
        )

    def set_commands(self, commands: dict):
        self._commands = commands

    def set_command_handler(self, command_handler: Callable):
        self._command_handler = command_handler

    def toggle(self):
        if self.is_visible():
            return self.set_visible(False)
        self._all_apps = self.app_util.all_applications
        (self.search_entry.set_text(""),)
        self.search_entry.grab_focus_without_selecting()
        return self.set_visible(True)

    def launch(self, command: str):
        self.search_entry.set_text(command)
