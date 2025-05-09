from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from loguru import logger

from services import MprisPlayer, MprisPlayerManager
from shared import ButtonWidget
from shared.pop_over import Popover
from utils import BarConfig, Colors
from widgets.media import PlayerBoxStack


class Mpris(ButtonWidget):
    """A widget to control the MPRIS."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(
            widget_config["mpris"],
            name="mpris",
            **kwargs,
        )

        self.player = None

        self.label = Label(label="Nothing playing", style_classes="panel-text")

        self.cover = Box(style_classes="cover")
        self.box.children = [self.cover, self.label]

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

        config = {
            "enabled": True,
            "ignore": ["vlc"],
            "truncation_size": 30,
            "show_album": True,
            "show_artist": True,
            "show_time": True,
            "show_time_tooltip": True,
        }

        popup = Popover(
            content_factory=lambda: Box(
                style_classes="mpris-box",
                children=[
                    PlayerBoxStack(self.mpris_manager, config=config),
                ],
            ),
            point_to=self,
        )

        # Connect the button press event to the play_pause method
        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: popup.open(),
            },
        )

    def get_current(self):
        bar_label = self.player.title

        truncated_info = (
            bar_label
            if len(bar_label) < self.config["truncation_size"]
            else bar_label[:30]
        )

        self.label.set_label(truncated_info)

        art_url = self.player.metadata["mpris:artUrl"]

        if art_url == "" or art_url is None:
            art_url = "https://ladydanville.wordpress.com/wp-content/uploads/2012/03/blankart.png?w=297&h=278"

        self.cover.set_style(
            "background-image: url('" + art_url + "');background-size: cover;"
        )

        if self.config["tooltip"]:
            self.set_tooltip_text(bar_label)
