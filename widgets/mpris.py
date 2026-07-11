from fabric.utils import GLib, bulk_connect, logger
from fabric.widgets.box import Box

from services.mpris import MprisPlayer, MprisPlayerManager
from shared.media import PlayerBoxStack
from shared.mixins import PopoverMixin
from shared.scrollable_text import ScrollingLabel
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.constants import ASSETS_DIR, NEWLINE_RE
from utils.functions import char_limit_to_px, safe_disconnect


class MprisWidget(ButtonWidget, PopoverMixin):
    """A widget to control the MPRIS."""

    def __init__(self, **kwargs):
        super().__init__(name="mpris", **kwargs)

        self.player = None
        self._player_update_handlers: list[int] = []
        self._progress_timer_id: int | None = None

        self.default_cover = f"{ASSETS_DIR}/images/disk.png"

        self.label = ScrollingLabel(
            name="mpris-label",
            style_classes=["panel-text"],
            scroll_on_hover=True,
            max_width=char_limit_to_px(self, self.config.get("truncation_size", 30)),
        )

        self.cover = Box(name="mpris-cover")
        self.progress = Box(name="mpris-progress")
        self.meta_box = Box(
            name="mpris-meta-box",
            orientation="v",
            spacing=2,
            h_expand=True,
            v_align="start",
            children=[self.label, self.progress],
        )
        self._set_default_values()
        self.container_box.children = [self.cover, self.meta_box]
        self._last_progress_pct: float | None = None

        bulk_connect(
            self,
            {
                "enter-notify-event": self.on_hover_enter,
                "leave-notify-event": self.on_hover_leave,
            },
        )

        config = {
            "enabled": True,
            "ignore": [""],
            "truncation_size": 30,
            "show_album": True,
            "show_artist": True,
            "show_time": True,
            "show_time_tooltip": True,
        }

        self.label_format = self.config.get("label_format", "{title} - {artist}")

        # Services
        self.mpris_manager = MprisPlayerManager()
        bulk_connect(
            self.mpris_manager,
            {
                "player-appeared": self.on_player_appeared,
                "player-vanished": self.on_player_vanished,
            },
        )

        for player in self.mpris_manager.players:
            logger.info(
                f"{Colors.INFO}[PLAYER MANAGER] player found: "
                f"{player.get_property('player-name')}",
            )
            if player.props.player_name in self.config.get("ignore", []):
                continue
            self._set_player(player)
            break

        self.setup_popover(
            lambda: PlayerBoxStack(self.mpris_manager, config=config),
        )
        self._start_progress_timer()

    def _bind_player_updates(self):
        self._unbind_player_updates()
        if self.player is None:
            return

        metadata_signals = [
            "changed",
            "notify::metadata",
            "notify::title",
            "notify::arturl",
            "notify::length",
            "notify::playback-status",
        ]

        for signal_name in metadata_signals:
            self._player_update_handlers.append(
                self.player.connect(signal_name, lambda *_: self.get_current())
            )

    def _start_progress_timer(self):
        if self._progress_timer_id is not None:
            return

        self._progress_timer_id = GLib.timeout_add(1000, self._on_progress_tick)

    def _stop_progress_timer(self):
        if self._progress_timer_id is None:
            return

        GLib.source_remove(self._progress_timer_id)
        self._progress_timer_id = None

    def _on_progress_tick(self):
        if self.player and self.player.playback_status == "playing":
            self._update_progress()
        return True

    def _update_progress(self):
        show_progress = False
        self.meta_box.v_align = "start"
        playback_status = self.player.playback_status if self.player else None

        if playback_status not in {"playing", "paused"}:
            self.meta_box.v_align = "center"
            progress_pct = 0.0
        else:
            title = (self.player.title or "").strip()
            show_progress = playback_status in {"playing", "paused"} and bool(title)
            length_raw = getattr(self.player, "length", None)
            position_raw = getattr(self.player, "position", 0)
            try:
                track_length = int(length_raw) if length_raw is not None else 0
            except (TypeError, ValueError):
                track_length = 0

            try:
                position = int(position_raw) if position_raw is not None else 0
            except (TypeError, ValueError):
                position = 0

            if track_length > 0:
                progress_pct = max(0.0, min(100.0, (position / track_length) * 100.0))
            else:
                progress_pct = 0.0

        self.progress.set_visible(show_progress)

        if not show_progress:
            self._last_progress_pct = None
            self.progress.set_style("")
            return

        rounded = round(progress_pct, 1)

        if rounded == self._last_progress_pct:
            return

        self._last_progress_pct = rounded

        self.progress.set_style(
            "background-image: linear-gradient(90deg, "
            "rgba(103, 200, 255, 0.95) 0%, "
            f"rgba(103, 200, 255, 0.95) {rounded:.1f}%, "
            f"rgba(255,255,255,0.20) {rounded:.1f}%, "
            "rgba(255,255,255,0.20) 100%);"
        )

    def _unbind_player_updates(self):
        if self.player is None:
            self._player_update_handlers.clear()
            return

        for handler_id in self._player_update_handlers:
            safe_disconnect(self.player, handler_id)
        self._player_update_handlers.clear()

    def _set_player(self, raw_player):
        self._unbind_player_updates()
        self._last_progress_pct = None
        self.player = MprisPlayer(raw_player)
        self._bind_player_updates()
        self.get_current()

    def on_player_appeared(self, manager, raw_player):
        if raw_player.props.player_name in self.config.get("ignore", []):
            return

        # Prefer active playback for the compact bar widget when players appear.
        if self.player is None or self.player.playback_status != "playing":
            self._set_player(raw_player)

    def on_player_vanished(self, manager, player_name):
        if self.player is None or self.player.player_name != player_name:
            return

        self._unbind_player_updates()
        self.player = None

        for raw_player in self.mpris_manager.players:
            if raw_player.props.player_name in self.config.get("ignore", []):
                continue
            self._set_player(raw_player)
            return

        self.get_current()

    def on_hover_enter(self, *_):
        self.label.on_enter_notify()
        return False

    def on_hover_leave(self, *_):
        self.label.on_leave_notify()
        return False

    def get_current(self):
        playback_status = self.player.playback_status if self.player else None
        if playback_status not in {"playing", "paused"}:
            self._set_default_values()
            return

        self.show()
        title = NEWLINE_RE.sub(" ", self.player.title or "").strip()
        bar_label = title or "Nothing playing"

        label_text = self.label_format.format(
            title=title,
            artist=self.player.artist or "",
            album=self.player.album or "",
            name=self.player.player_name or "",
        )

        self.label.set_text(label_text)

        art_url = getattr(self.player, "arturl", None)
        if not art_url:
            art_url = self.default_cover

        self.cover.set_style("background-image: url('" + art_url + "');")
        self._update_progress()

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(bar_label)

    def _set_default_values(self):
        self._last_progress_pct = None
        self.cover.set_style("background-image: url('" + self.default_cover + "');")
        self.label.set_text("Nothing playing")
        self.meta_box.v_align = "center"
        self.progress.set_visible(False)
        self.progress.set_style("")
        if self.config.get("hide_when_no_player", True):
            self.hide()

    def destroy(self):
        self._stop_progress_timer()
        self._unbind_player_updates()
        return super().destroy()
