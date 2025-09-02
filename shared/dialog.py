from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from .popup import PopupWindow


class Dialog(PopupWindow):
    """A dialog box to display a message."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        **kwargs,
    ):
        self.wrapper = Box(orientation="v", name="dialog-wrapper")

        self.title = Label(
            h_align="center",
            name="dialog-title",
        )
        self.body = Label(h_align="center", name="dialog-body")

        self.buttons = Box(
            orientation="h",
            name="dialog-buttons-box",
            v_align="center",
            h_align="center",
        )

        self.ok_btn = Button(label="OK", name="dialog-button")
        self.cancel_btn = Button(
            label="Cancel", name="dialog-button", on_clicked=lambda *_: self.destroy()
        )

        self.buttons.children = (self.ok_btn, self.cancel_btn)

        self.wrapper.children = (self.title, self.body, self.buttons)

        super().__init__(
            name="dialog",
            child=self.wrapper,
            transition_duration=300,
            transition_type="crossfade",
            anchor="center",
            enable_inhibitor=True,
            keyboard_mode="exclusive",
            **kwargs,
        )

    def add_content(
        self,
        title: str,
        body: str,
        command: str,
    ):
        self.title.set_label(title.upper())
        self.body.set_label(body)
        self.ok_btn.connect(
            "clicked", lambda *_: exec_shell_command_async(command, lambda *_: None)
        )

        return self
