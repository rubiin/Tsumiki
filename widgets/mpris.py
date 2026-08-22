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
from utils.i18n import _


class MprisWidget(ButtonWidget, PopoverMixin):
    """A compact bar widget showing the currently playing track."""

    def __init__(self, **kwargs):
        super().__init__(name="mpris", **kwargs)

        self.player = None
        self._player_update_handlers: list[int] = []
        self._progress_timer_id: int | None = None

        self.default_cover = f"{ASSETS_DIR}/images/disk.png"

        # Scrolling track label
        self.label = ScrollingLabel(
            name="mpris-label",
            style_classes="panel-text",
            scroll_on_hover=True,
            max_width=char_limit_to_px(self, self.config.get("truncation_size", 30)),
        )

        # Cover art thumbnail
        self.cover = Box(
            name="mpris-cover",
            style=f"background-image: url('{self.default_cover}');",
        )

        # Progress bar — styled via SCSS (#mpris-progress)
        self.progress = Box(name="mpris-progress")
        self.progress_fill = Box(
            name="mpris-progress-fill",
            h_align="start",
        )
        self.progress.children = [self.progress_fill]

        self.meta_box = Box(
            name="mpris-meta-box",
            orientation="v",
            spacing=2,
            h_expand=True,
            v_align="start",
            children=[self.label, self.progress],
        )

        self._last_progress_pct: float | None = None
        self._set_default_values()
        self.container_box.children = [self.cover, self.meta_box]

        bulk_connect(
            self,
            {
                "enter-notify-event": self.on_hover_enter,
                "leave-notify-event": self.on_hover_leave,
            },
        )

        self.label_format = self.config.get("label_format", "{title} - {artist}")

        # Services
        self.mpris_manager = MprisPlayerManager()
        for hid in bulk_connect(
            self.mpris_manager,
            {
                "player-appeared": self.on_player_appeared,
                "player-vanished": self.on_player_vanished,
            },
        ):
            self._register_handler(self.mpris_manager, hid)

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
            lambda: PlayerBoxStack(self.mpris_manager, config=self.config),
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
        self._progress_timer_id = self._register_repeater(
            GLib.timeout_add(1000, self._on_progress_tick)
        )

    def _stop_progress_timer(self):
        if self._progress_timer_id is None:
            return
        self._unregister_repeater(self._progress_timer_id)
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
            try:
                track_length = (
                    int(self.player.length) if self.player.length is not None else 0
                )
            except (TypeError, ValueError):
                track_length = 0

            try:
                position = (
                    int(self.player.position) if self.player.position is not None else 0
                )
            except (TypeError, ValueError):
                position = 0

            if track_length > 0:
                progress_pct = max(0.0, min(100.0, (position / track_length) * 100.0))
            else:
                progress_pct = 0.0

        self.progress.set_visible(show_progress)

        if not show_progress:
            self._last_progress_pct = None
            self.progress_fill.set_style("")
            return

        rounded = round(progress_pct, 1)
        if rounded == self._last_progress_pct:
            return

        self._last_progress_pct = rounded
        alloc_width = self.progress.get_allocated_width()
        if alloc_width > 0:
            fill_px = max(1, round(alloc_width * rounded / 100.0))
            self.progress_fill.set_style(f"min-width: {fill_px}px;")
        else:
            self.progress_fill.set_style("")

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
        bar_label = title or _("widget.mpris.nothing_playing")

        label_text = self.label_format.format(
            title=title,
            artist=self.player.artist or "",
            album=self.player.album or "",
            name=self.player.player_name or "",
        )
        self.label.set_text(label_text)

        art_url = getattr(self.player, "arturl", None) or self.default_cover
        safe_url = art_url.replace("\\", "\\\\").replace("'", "\\'")
        self.cover.set_style(f"background-image: url('{safe_url}');")

        self._update_progress()

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(bar_label)

    def _set_default_values(self):
        self._last_progress_pct = None
        self.cover.set_style(f"background-image: url('{self.default_cover}');")
        self.label.set_text("Nothing playing")
        self.meta_box.v_align = "center"
        self.progress.set_visible(False)
        self.progress_fill.set_style("")
        if self.config.get("hide_when_no_player", True):
            self.hide()

    def destroy(self):
        self._stop_progress_timer()
        self._unbind_player_updates()
        return super().destroy()
