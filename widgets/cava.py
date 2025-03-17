from fabric import Fabricator
from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.label import Label

import utils.functions as helpers
from shared import ButtonWidget
from utils import BarConfig, ExecutableNotFoundError


class CavaWidget(ButtonWidget):
    """A widget to display the Cava audio visualizer."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="cava", **kwargs)

        self.config = widget_config["cava"]
        cava_command = "cava"

        if not helpers.executable_exists(cava_command):
            raise ExecutableNotFoundError(cava_command)

        if not helpers.is_valid_gjs_color(self.config["color"]):
            raise ValueError("Invalid color supplied for cava widget")

        command = f"kitty --title systemupdate sh -c '{cava_command}'"

        self.box = Box()

        self.children = self.box

        cava_label = Label(
            v_align="center",
            h_align="center",
            style=f"color: {self.config['color']};",
        )

        script_path = get_relative_path("../assets/scripts/cava.sh")

        self.box.children = Box(spacing=1, children=[cava_label]).build(
            lambda box, _: Fabricator(
                poll_from=f"bash -c '{script_path} {self.config['bars']}'",
                stream=True,
                on_changed=lambda f, line: cava_label.set_label(line),
            )
        )

        self.connect(
            "clicked", lambda _: exec_shell_command_async(command, lambda *_: None)
        )
