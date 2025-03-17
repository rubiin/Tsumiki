from typing import Literal

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from utils.functions import handle_power_action

from .pop_up import PopupWindow


class Dialog(PopupWindow):
    """A dialog box to display a message."""

    def __init__(
        self,
        title: Literal["shutdown", "reboot", "hibernate", "suspend", "lock", "logout"],
        body: str,
        **kwargs,
    ):
        self.wrapper = Box(orientation="v", name="dialog-wrapper")

        self.title = Label(h_align="center", name="dialog-title", label=title.upper())

        self.body = Label(h_align="center", name="dialog-body", label=body)

        self.buttons = Box(
            orientation="h",
            name="dialog-buttons-box",
            v_align="center",
            h_align="center",
        )

        self.ok_btn = Button(label="OK", name="dialog-button")
        self.cancel_btn = Button(label="Cancel", name="dialog-button")

        self.buttons.children = (self.ok_btn, self.cancel_btn)

        self.ok_btn.connect("clicked", lambda *_: handle_power_action(operation=title))
        self.cancel_btn.connect("clicked", lambda *_: self.destroy())

        self.wrapper.children = (self.title, self.body, self.buttons)

        super().__init__(
            name="dialog",
            transition_type="crossfade",
            child=self.wrapper,
            anchor="center",
            keyboard_mode="on-demand",
            **kwargs,
        )
