import re

from fabric.utils import logger
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from services.mpris import MprisPlayer, MprisPlayerManager
from shared.media import PlayerBoxStack
from shared.popover import Popover
from shared.widget_container import ButtonWidget
from utils.colors import Colors


class MprisWidget(ButtonWidget):
    """A widget to control the MPRIS."""

    def __init__(
        self,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(
            name="mpris",
            **kwargs,
        )

        self.player = None

        self.label = Label(label="Nothing playing", style_classes=["panel-text"])

        self.cover = Box(style_classes=["cover"])
        self.container_box.children = [self.cover, self.label]

        # Services
        self.mpris_manager = MprisPlayerManager()

        for player in self.mpris_manager.players:
            logger.info(
                f"{Colors.INFO}[PLAYER MANAGER] player found: "
                f"{player.get_property('player-name')}",
            )
            self.player = MprisPlayer(player)
            self.get_current()
            break

        self.config = {
            "enabled": True,
            "ignore": ["vlc"],
            "truncation_size": 30,
            "show_album": True,
            "show_artist": True,
            "show_time": True,
            "show_time_tooltip": True,
        }

        self.popup = None

        self.connect("clicked", self.on_click)

    def get_current(self):
        bar_label = re.sub(r"\r?\n", " ", self.player.title)

        truncated_info = (
            bar_label
            if len(bar_label) < self.config.get("truncation_size", 30)
            else bar_label[:30]
        )

        self.label.set_label(truncated_info)

        art_url = self.player.metadata["mpris:artUrl"]

        if art_url == "" or art_url is None:
            art_url = "https://ladydanville.wordpress.com/wp-content/uploads/2012/03/blankart.png?w=297&h=278"

        self.cover.set_style(
            "background-image: url('" + art_url + "');background-size: cover;"
        )

        if self.config.get("tooltip", False):
            self.set_tooltip_text(bar_label)

    def on_click(self, *_):
        if self.popup is None:
            self.popup = Popover(
                content=Box(
                    style_classes=["mpris-box"],
                    children=[
                        PlayerBoxStack(self.mpris_manager, config=self.config),
                    ],
                ),
                point_to=self,
            )
        self.popup.open()
