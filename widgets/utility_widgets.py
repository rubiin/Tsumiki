from fabric.widgets.box import Box

from shared import Separator
from utils import BarConfig


class SpacingWidget(Box):
    """A simple widget to add spacing between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        self.config = widget_config["spacing"]
        super().__init__(
            name="spacing", style=f"min-width: {self.config['size']}px;", **kwargs
        )


class DividerWidget(Box):
    """A simple widget to add a divider between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="divider", **kwargs)

        self.config = widget_config["divider"]
        self.children = Box(
            children=(
                Separator(
                    orientation="vertical", style=f"min-width: {self.config['size']}px;"
                ),
            )
        )
