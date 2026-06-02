from fabric.utils import logger
from fabric.widgets.box import Box

from services.mpris import MprisPlayer, MprisPlayerManager
from shared.media import PlayerBoxStack
from shared.mixins import PopoverMixin
from shared.scrollable_text import ScrollingLabel
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.constants import NEWLINE_RE


class MprisWidget(ButtonWidget, PopoverMixin):
    """A widget to control the MPRIS."""

    def __init__(self, **kwargs):
        super().__init__(name="mpris", **kwargs)

        self.player = None

        self.label = ScrollingLabel(text="Nothing playing", style_classes=["panel-text"])

        self.cover = Box(style_classes=["cover"])
        self.container_box.children = [self.cover, self.label]

        self.config = {
            "enabled": True,
            "ignore": ["vlc"],
            "truncation_size": 30,
            "show_album": True,
            "show_artist": True,
            "show_time": True,
            "show_time_tooltip": True,
        }

        # Services
        self.mpris_manager = MprisPlayerManager()

        for player in self.mpris_manager.players:
            logger.info(
                f"{Colors.INFO}[PLAYER MANAGER] player found: "
                f"{player.get_property('player-name')}",
            )
            self.player = MprisPlayer(player)
            self._bind_player_updates()
            self.get_current()
            break

        self.setup_popover(
            lambda: Box(
                style_classes=["mpris-box"],
                children=[PlayerBoxStack(self.mpris_manager, config=self.config)],
            )
        )

    def _bind_player_updates(self):
        if self.player is None:
            return

        self.player.connect("changed", lambda *_: self.get_current())
        self.player.connect("notify::metadata", lambda *_: self.get_current())
        self.player.connect("notify::title", lambda *_: self.get_current())
        self.player.connect("notify::arturl", lambda *_: self.get_current())

    def get_current(self):
        if self.player is None:
            self.label.set_text("Nothing playing")
            return

        title = self.player.title or ""
        bar_label = NEWLINE_RE.sub(" ", title).strip() or "Nothing playing"

        truncated_info = (
            bar_label
            if len(bar_label) < self.config.get("truncation_size", 30)
            else bar_label[: self.config.get("truncation_size", 30)]
        )

        self.label.set_text(truncated_info)

        art_url = getattr(self.player, "arturl", None)
        if not art_url:
            art_url = "https://ladydanville.wordpress.com/wp-content/uploads/2012/03/blankart.png?w=297&h=278"

        self.cover.set_style(
            "background-image: url('" + art_url + "'); background-size: cover;"
        )

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(bar_label)
