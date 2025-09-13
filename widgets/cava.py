from fabric import Fabricator
from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.label import Label

import utils.functions as helpers
from shared.widget_container import ButtonWidget
from utils.constants import ASSETS_DIR


class CavaWidget(ButtonWidget):
    """A widget to display the Cava audio visualizer."""

    def __init__(self, **kwargs):
        super().__init__(name="cava", **kwargs)

        cava_command = "cava"

        helpers.check_executable_exists(cava_command)

        command = f"kitty --title cava-visualizer sh -c '{cava_command}'"

        color = self.config.get("color", "#ffffff")  # default white
        bars = self.config.get("bars", 10)

        if not helpers.is_valid_gjs_color(color):
            raise ValueError(f"Invalid color '{color}' supplied for cava widget")

        cava_label = Label(
            v_align="center",
            h_align="center",
            style=f"color: {color};",
        )

        script_path = f"{ASSETS_DIR}/scripts/cava.sh"

        self.container_box.children = Box(spacing=1, children=[cava_label]).build(
            lambda box, _: Fabricator(
                poll_from=f"bash -c '{script_path} {bars}'",
                stream=True,
                on_changed=lambda f, line: cava_label.set_label(line),
            )
        )

        self.connect(
            "clicked", lambda _: exec_shell_command_async(command, lambda *_: None)
        )
