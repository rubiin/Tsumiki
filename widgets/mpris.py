from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from loguru import logger

from services import MprisPlayer, MprisPlayerManager
from shared import ButtonWidget
from utils import BarConfig, Colors
from utils.icons import common_text_icons


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
            widget_config,
            **kwargs,
        )
        self.config = widget_config["mpris"]

        self.player = None

        self.label = Label(label="Nothing playing", style_classes="panel-text")
        self.text_icon = Label(
            label=common_text_icons["playing"],
        )

        # Services
        self.mpris_manager = MprisPlayerManager()

        for player in self.mpris_manager.players:
            logger.info(
                f"{Colors.INFO}[PLAYER MANAGER] player found: "
                f"{player.get_property('player-name')}",
            )
            self.player = MprisPlayer(player)
            bulk_connect(
                self.player,
                {
                    "notify::metadata": self.get_current,
                    "notify::playback-status": self.get_playback_status,
                },
            )

        self.revealer = Revealer(
            name="mpris-revealer",
            transition_type="slide-right",
            transition_duration=400,
            child=self.label,
            child_revealed=True,
        )

        self.cover = Box(style_classes="cover")

        self.box = Box(
            children=[self.text_icon],
        )

        self.children = self.box

        # Connect the button press event to the play_pause method
        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: self.play_pause(),
            },
        )

    def get_current(self, *_):
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

    def get_playback_status(self, *_):
        # Get the current playback status and change the icon accordingly

        status = self.player.playback_status.lower()
        if status == "playing":
            self.box.children = [self.cover, self.text_icon, self.revealer]
            self.revealer.set_reveal_child(True)
            self.text_icon.set_label(common_text_icons["paused"])
        elif status == "paused":
            self.box.children = [self.cover, self.text_icon, self.revealer]
            self.revealer.set_reveal_child(True)
            self.text_icon.set_label(common_text_icons["playing"])
        else:
            self.box.children = [self.text_icon]
            self.revealer.set_reveal_child(False)

    def play_pause(self, *_):
        # Toggle play/pause using playerctl
        if self.player is not None:
            self.player.play_pause()
