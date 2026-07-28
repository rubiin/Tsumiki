import tempfile
import urllib.parse

from fabric.utils import GLib, GObject, bulk_connect, idle_add, logger, os
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.stack import Stack

from services.mpris import MprisPlayer, MprisPlayerManager
from shared.sinewave_slider import SineWaveSlider
from utils.constants import APP_DATA_DIRECTORY, ASSETS_DIR, NEWLINE_RE
from utils.functions import ensure_directory, get_http_client
from utils.icons import get_text_icon
from utils.widget_utils import nerd_font_icon

from .buttons import HoverButton


def _format_seconds(micro_seconds: int) -> str:
    seconds = int(micro_seconds / 1_000_000)
    minutes = seconds // 60
    rem = seconds % 60
    return f"{minutes}:{rem:02d}"


def _format_time_combined(position_us: int, length_us: int) -> str:
    return f"{_format_seconds(position_us)} / {_format_seconds(length_us)}"


class PlayerBoxStack(Box):
    """Manages multiple player instances with navigation dots."""

    def __init__(self, mpris_manager: MprisPlayerManager, config, **kwargs):
        self.config = config
        ensure_directory(f"{APP_DATA_DIRECTORY}/media")

        self.player_stack = Stack(
            transition_type="slide-left-right",
            transition_duration=500,
            name="player-stack",
        )
        self.current_stack_pos = 0
        self.player_buttons: list[Button] = []
        self.buttons_box = CenterBox()

        super().__init__(
            orientation="v", children=[self.player_stack, self.buttons_box]
        )
        self.hide()

        self.mpris_manager = mpris_manager
        bulk_connect(
            self.mpris_manager,
            {
                "player-appeared": self.on_new_player,
                "player-vanished": self.on_lost_player,
            },
        )

        for player in self.mpris_manager.players:
            logger.info(
                f"[PLAYER MANAGER] player found: {player.get_property('player-name')}",
            )
            self.on_new_player(self.mpris_manager, player)

    def on_player_clicked(self, direction):
        self.player_buttons[self.current_stack_pos].remove_style_class("active")
        count = len(self.player_stack.get_children())
        if direction == "next":
            self.current_stack_pos = (self.current_stack_pos + 1) % count
        elif direction == "prev":
            self.current_stack_pos = (self.current_stack_pos - 1) % count
        self.player_buttons[self.current_stack_pos].add_style_class("active")
        self.player_stack.set_visible_child(
            self.player_stack.get_children()[self.current_stack_pos],
        )

    def on_new_player(self, mpris_manager, player):
        player_name = player.props.player_name
        if player_name in self.config.get("ignore", []):
            return
        self.set_visible(True)
        self.buttons_box.set_visible(len(self.player_stack.get_children()) > 0)
        self.player_stack.children = [
            *self.player_stack.children,
            PlayerBox(player=MprisPlayer(player), config=self.config),
        ]
        self.make_new_player_button(self.player_stack.get_children()[-1])
        logger.info(
            f"[PLAYER MANAGER] adding new player: {player.get_property('player-name')}",
        )
        self.player_buttons[self.current_stack_pos].set_style_classes(["active"])

    def on_lost_player(self, mpris_manager, player_name):
        logger.info(f"[PLAYER_MANAGER] Player Removed {player_name}")
        players: list = self.player_stack.get_children()
        if len(players) == 1 and player_name == players[0].player.player_name:
            self.hide()
            self.current_stack_pos = 0
            return
        if players[self.current_stack_pos].player.player_name == player_name:
            self.current_stack_pos = max(0, self.current_stack_pos - 1)
            self.player_stack.set_visible_child(
                self.player_stack.get_children()[self.current_stack_pos],
            )
        self.player_buttons[self.current_stack_pos].set_style_classes(["active"])
        self.buttons_box.set_visible(len(players) > 2)

    def make_new_player_button(self, player_box):
        new_button = HoverButton(name="player-stack-button")

        def on_player_button_click(button: Button):
            self.player_buttons[self.current_stack_pos].remove_style_class("active")
            self.current_stack_pos = self.player_buttons.index(button)
            button.add_style_class("active")
            self.player_stack.set_visible_child(player_box)

        new_button.connect("clicked", on_player_button_click)
        self.player_buttons.append(new_button)
        player_box.connect(
            "destroy",
            lambda *_: [
                new_button.destroy(),
                self.player_buttons.pop(self.player_buttons.index(new_button)),
            ],
        )
        self.buttons_box.add_center(self.player_buttons[-1])


class PlayerBox(Box):
    """Glassmorphism player card: album art, metadata, waveform, playback."""

    def __init__(self, player: MprisPlayer, config: dict, **kwargs):
        super().__init__(
            name="player-box",
            spacing=0,
            **kwargs,
        )

        self.player: MprisPlayer = player
        self.config = config
        self.fallback_cover_path = f"{ASSETS_DIR}/images/disk.png"
        self._last_temp_art_path: str | None = None
        self._seekbar_timer_id: int | None = None
        self.exit = False

        # ─── Album Art ───
        self.album_art = Box(
            name="player-album-art",
            style=f"background-image: url('{self.fallback_cover_path}');",
        )

        # ─── Track Info ───
        self.title_label = Label(
            name="player-title",
            label="No Title",
            max_chars_width=28,
            ellipsization="end",
            h_align="start",
        )
        self.artist_label = Label(
            name="player-artist",
            label="No Artist",
            max_chars_width=28,
            ellipsization="end",
            h_align="start",
            visible=self.config.get("show_artist", True),
        )
        self.time_label = Label(
            name="player-time",
            label="0:00 / 0:00",
            h_align="start",
            visible=self.config.get("show_time", True),
        )

        for prop, widget in [
            ("title", self.title_label),
            ("artist", self.artist_label),
        ]:
            fallback = f"No {prop.title()}"
            self.player.bind_property(
                prop,
                widget,
                "label",
                GObject.BindingFlags.DEFAULT,
                lambda _, x, f=fallback: NEWLINE_RE.sub(" ", x) if x else f,
            )

        # ─── Progress Bar ───
        self.progress_bar = SineWaveSlider(name="player-slider")

        # ─── Bottom Controls Row ───
        prev_icon = nerd_font_icon(
            icon=get_text_icon("mpris.previous"),
            props={"style_classes": ["player-icon-sm"]},
        )
        self.prev_btn = HoverButton(
            name="player-prev",
            child=prev_icon,
            on_clicked=self.player.previous,
        )
        self.player.bind_property("can_go_previous", self.prev_btn, "sensitive")

        next_icon = nerd_font_icon(
            icon=get_text_icon("mpris.next"),
            props={"style_classes": ["player-icon-sm"]},
        )
        self.next_btn = HoverButton(
            name="player-next",
            child=next_icon,
            on_clicked=self.player.next,
        )
        self.player.bind_property("can_go_next", self.next_btn, "sensitive")

        self.controls_row = Box(
            name="player-controls-row",
            spacing=6,
            v_align="center",
            children=[self.prev_btn, self.progress_bar, self.next_btn],
        )

        # ─── Center Column ───
        self.meta_col = Box(
            name="player-meta-col",
            orientation="v",
            spacing=3,
            v_align="center",
            h_expand=True,
            children=[
                self.title_label,
                self.artist_label,
                self.time_label,
                self.controls_row,
            ],
        )

        # ─── Play/Pause Button ───
        self.play_pause_icon = nerd_font_icon(
            icon=get_text_icon("mpris.paused"),
            props={"style_classes": ["player-icon-lg"]},
        )
        self.play_pause_btn = HoverButton(
            name="player-play-pause",
            child=self.play_pause_icon,
            on_clicked=self.player.play_pause,
            v_align="start",
        )
        self.player.bind_property("can_pause", self.play_pause_btn, "sensitive")

        # ─── Main Row ───
        self.main_row = Box(
            name="player-main-row",
            spacing=12,
            children=[self.album_art, self.meta_col, self.play_pause_btn],
        )
        self.children = [self.main_row]

        # ─── Signals ───
        bulk_connect(
            self.player,
            {
                "exit": self.on_player_exit,
                "notify::playback-status": self.on_playback_change,
                "notify::metadata": self.on_metadata,
            },
        )

    # ─── Metadata & Artwork ─────────────────────────────────────────────────

    def on_metadata(self, *_):
        self._set_image()
        length = self.player.length
        if length:
            pos = self.player.position or 0
            self.time_label.set_label(_format_time_combined(pos, length))
        self._stop_seekbar_timer()
        self._seekbar_timer_id = GLib.timeout_add(1000, self._move_seekbar)

    def _set_image(self, *_):
        art_url = self.player.arturl
        if not art_url:
            self._update_art(self.fallback_cover_path)
            return
        parsed = urllib.parse.urlparse(art_url)
        if parsed.scheme == "file":
            local_arturl = urllib.parse.unquote(parsed.path)
            self._update_art(local_arturl)
        elif parsed.scheme in ("http", "https"):
            GLib.Thread.new("download-artwork", self._download_and_set_artwork, art_url)
        else:
            self._update_art(art_url)

    def _download_and_set_artwork(self, arturl):
        try:
            parsed = urllib.parse.urlparse(arturl)
            suffix = os.path.splitext(parsed.path)[1] or ".png"
            response = get_http_client().get(arturl, timeout=5)
            old_temp_path = self._last_temp_art_path
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(response.content)
                local_arturl = temp_file.name
            self._last_temp_art_path = local_arturl
            if (
                old_temp_path
                and old_temp_path != local_arturl
                and os.path.exists(old_temp_path)
            ):
                try:
                    os.remove(old_temp_path)
                except OSError:
                    logger.debug(f"[Media] Failed to remove temp file: {old_temp_path}")
        except Exception:
            local_arturl = self.fallback_cover_path
        idle_add(self._update_art, local_arturl)

    def _update_art(self, image_path):
        url = (
            f"url('{image_path}')"
            if image_path and os.path.isfile(image_path)
            else f"url('{self.fallback_cover_path}')"
        )
        self.album_art.set_style(
            f"background-image: {url};"
            " background-size: cover; background-position: center;"
        )

    # ─── Playback Controls ──────────────────────────────────────────────────

    def on_playback_change(self, player, _status):
        status = player.get_property("playback-status")
        if status == "paused":
            self.play_pause_icon.set_label(get_text_icon("mpris.playing"))
        elif status == "playing":
            self.play_pause_icon.set_label(get_text_icon("mpris.paused"))

    def _on_waveform_seek(self, fraction: float):
        length = self.player.length
        if length:
            self.player.position = int(length * fraction)

    def _move_seekbar(self, *_):
        if self.player is None or self.exit:
            self._seekbar_timer_id = None
            return False
        pos = self.player.position
        length = self.player.length
        if length:
            self.time_label.set_label(_format_time_combined(pos, length))
            self.progress_bar.set_value(pos / length if length > 0 else 0.0)
        return True

    def _stop_seekbar_timer(self):
        if self._seekbar_timer_id is not None:
            GLib.source_remove(self._seekbar_timer_id)
            self._seekbar_timer_id = None

    # ─── Lifecycle ──────────────────────────────────────────────────────────

    def on_player_exit(self, _, value):
        self.exit = value
        self._stop_seekbar_timer()
        self.destroy()

    def destroy(self):
        self._stop_seekbar_timer()
        if self._last_temp_art_path and os.path.exists(self._last_temp_art_path):
            try:
                os.remove(self._last_temp_art_path)
            except OSError:
                logger.debug(
                    f"[Media] Failed to remove temp file: {self._last_temp_art_path}"
                )
            finally:
                self._last_temp_art_path = None
        super().destroy()
