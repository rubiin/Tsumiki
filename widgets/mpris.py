from fabric.utils import bulk_connect, logger
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

        self.label = ScrollingLabel(
            text="Nothing playing",
            style_classes=["panel-text"],
            scroll_on_hover=True,
        )

        self.cover = Box(style_classes=["cover"])
        self._set_default_values()
        self.container_box.children = [self.cover, self.label]

        bulk_connect(
            self,
            {
                "enter-notify-event": self.on_hover_enter,
                "leave-notify-event": self.on_hover_leave,
            },
        )

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

        bulk_connect(
            self.player,
            {
                "changed": lambda *_: self.get_current(),
                "notify::metadata": lambda *_: self.get_current(),
                "notify::title": lambda *_: self.get_current(),
                "notify::arturl": lambda *_: self.get_current(),
            },
        )

    def on_hover_enter(self, widget, event):
        self.label.on_enter_notify()
        return False

    def on_hover_leave(self, widget, event):
        self.label.on_leave_notify()
        return False

    def get_current(self):
        if self.player is None:
            self._set_default_values()
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

    def _set_default_values(self):
        self.cover.set_style(
            "background-image: url('https://raw.githubusercontent.com/rubiin/tsumiki/refs/heads/master/assets/images/disk.png')"
        )
        self.label.set_text("Nothing playing")
