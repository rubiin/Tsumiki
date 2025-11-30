import os
import re
import tempfile
import urllib.parse
import urllib.request
from functools import partial

import gi

# Pre-compiled regex for newline replacement
_NEWLINE_RE = re.compile(r"\r?\n")

from fabric.utils import (
    bulk_connect,
    cooldown,
    invoke_repeater,
    logger,
)
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.scale import Scale
from fabric.widgets.stack import Stack
from gi.repository import GLib, GObject

from services.mpris import MprisPlayer, MprisPlayerManager
from shared.animator import cubic_bezier
from shared.buttons import HoverButton
from shared.circle_image import CircularImage
from utils.constants import APP_DATA_DIRECTORY, ASSETS_DIR
from utils.functions import (
    ensure_directory,
    get_simple_palette_threaded,
    mix_colors,
    rgb_to_css,
    tint_color,
)
from utils.icons import text_icons
from utils.widget_utils import (
    create_scale,
    nerd_font_icon,
    setup_cursor_hover,
)

gi.require_versions({"GObject": "2.0"})


class PlayerBoxStack(Box):
    """A widget that displays the current player information."""

    def __init__(self, mpris_manager: MprisPlayerManager, config, **kwargs):
        self.config = config

        ensure_directory(f"{APP_DATA_DIRECTORY}/media")

        # The player stack
        self.player_stack = Stack(
            transition_type="slide-left-right",
            transition_duration=500,
            name="player-stack",
        )
        self.current_stack_pos = 0

        # List to store player buttons
        self.player_buttons: list[Button] = []

        # Box to contain all the buttons
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

        for player in self.mpris_manager.players:  # type: ignore
            logger.info(
                f"[PLAYER MANAGER] player found: {player.get_property('player-name')}",
            )
            self.on_new_player(self.mpris_manager, player)

    def on_player_clicked(self, type):
        # unset active from prev active button
        self.player_buttons[self.current_stack_pos].remove_style_class("active")
        if type == "next":
            self.current_stack_pos = (
                self.current_stack_pos + 1
                if self.current_stack_pos != len(self.player_stack.get_children()) - 1
                else 0
            )
        elif type == "prev":
            self.current_stack_pos = (
                self.current_stack_pos - 1
                if self.current_stack_pos != 0
                else len(self.player_stack.get_children()) - 1
            )
        # set new active button
        self.player_buttons[self.current_stack_pos].add_style_class("active")
        self.player_stack.set_visible_child(
            self.player_stack.get_children()[self.current_stack_pos],
        )

    def on_new_player(self, mpris_manager, player):
        player_name = player.props.player_name

        if player_name in self.config.get("ignore", []):
            return

        self.set_visible(True)
        if len(self.player_stack.get_children()) == 0:
            self.buttons_box.hide()
        else:
            self.buttons_box.set_visible(True)

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
        # the playerBox is automatically removed from mprisbox children on being removed
        logger.info(f"[PLAYER_MANAGER] Player Removed {player_name}")
        players: list[PlayerBox] = self.player_stack.get_children()
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
        self.buttons_box.hide() if len(players) == 2 else self.buttons_box.set_visible(
            True
        )

    def make_new_player_button(self, player_box):
        new_button = HoverButton(name="player-stack-button")

        def on_player_button_click(button: Button):
            self.player_buttons[self.current_stack_pos].remove_style_class("active")
            self.current_stack_pos = self.player_buttons.index(button)
            button.add_style_class("active")
            self.player_stack.set_visible_child(player_box)

        new_button.connect(
            "clicked",
            on_player_button_click,
        )
        self.player_buttons.append(new_button)

        # This will automatically destroy our used button
        player_box.connect(
            "destroy",
            lambda *_: [
                new_button.destroy(),  # type: ignore
                self.player_buttons.pop(self.player_buttons.index(new_button)),
            ],
        )
        self.buttons_box.add_center(self.player_buttons[-1])


class PlayerBox(Box):
    """A widget that displays the current player information."""

    def __init__(self, player: MprisPlayer, config: dict, **kwargs):
        super().__init__(
            h_align="center",
            name="player-box",
            **kwargs,
            h_expand=True,
        )
        # Setup
        self.player: MprisPlayer = player
        self.fallback_cover_path = f"{ASSETS_DIR}/images/disk.png"

        self.image_size = 120

        self.config = config

        self.icon_size = 15

        # State
        self.exit = False
        self.angle_direction = 1
        self.skipped = False

        self.image_box = CircularImage(
            size=self.image_size, image_file=self.fallback_cover_path
        )

        self.image_stack = Box(
            h_align="start", v_align="center", name="player-image-stack"
        )
        self.image_stack.children = [*self.image_stack.children, self.image_box]

        self.art_animator = None
        # Track Info
        self.track_title = Label(
            label="No Title",
            name="player-title",
            justfication="left",
            max_chars_width=self.config.get("truncation_size", 50),
            ellipsization="end",
            h_align="start",
        )

        self.track_artist = Label(
            label="No Artist",
            name="player-artist",
            justfication="left",
            max_chars_width=self.config.get("truncation_size", 50),
            ellipsization="end",
            h_align="start",
            visible=self.config.get("show_artist", True),
        )

        self.track_album = Label(
            label="No Album",
            name="player-album",
            justfication="left",
            max_chars_width=self.config.get("truncation_size", 50),
            ellipsization="end",
            h_align="start",
            visible=self.config.get("show_album", True),
        )

        self.player.bind_property(
            "title",
            self.track_title,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: _NEWLINE_RE.sub(" ", x)
            if x != "" and x is not None
            else "No Title",  # type: ignore
        )
        self.player.bind_property(
            "artist",
            self.track_artist,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: _NEWLINE_RE.sub(" ", x)
            if x != "" and x is not None
            else "No Artist",  # type: ignore
        )

        self.player.bind_property(
            "album",
            self.track_album,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: _NEWLINE_RE.sub(" ", x)
            if x != "" and x is not None
            else "No Album",  # type: ignore
        )

        self.track_info = Box(
            name="track-info",
            spacing=5,
            orientation="v",
            v_align="start",
            h_align="start",
            children=[
                self.track_title,
                self.track_artist,
                self.track_album,
            ],
        )

        # Buttons
        self.button_box = Box(
            name="button-box",
            h_align="center",
            spacing=2,
        )

        self.position_label = Label(
            "00:00",
            v_align="center",
            style_classes=["time-label"],
            visible=self.config.get("show_time", True),
        )
        self.length_label = Label(
            "00:00",
            v_align="center",
            style_classes=["time-label"],
            visible=self.config.get("show_time", True),
        )

        # Seek Bar
        self.seek_bar = create_scale(name="seek-bar")

        self.seek_bar.connect("change-value", self.on_scale_move)
        self.player.bind("can-seek", "sensitive", self.seek_bar)

        setup_cursor_hover(self.seek_bar)

        self.controls_box = CenterBox(
            name="player-controls",
            start_children=self.position_label,
            center_children=self.button_box,
            end_children=self.length_label,
        )

        self.skip_next_icon = nerd_font_icon(
            icon=text_icons["mpris"]["next"],
            props={"style_classes": ["panel-font-icon", "player-icon"]},
        )
        self.skip_prev_icon = nerd_font_icon(
            icon=text_icons["mpris"]["previous"],
            props={"style_classes": ["panel-font-icon", "player-icon"]},
        )
        self.loop_icon = nerd_font_icon(
            icon=text_icons["mpris"]["loop"],
            props={"style_classes": ["panel-font-icon", "player-icon"]},
        )
        self.shuffle_icon = nerd_font_icon(
            icon=text_icons["mpris"]["shuffle"],
            props={"style_classes": ["panel-font-icon", "player-icon"]},
        )
        self.play_pause_icon = nerd_font_icon(
            icon=text_icons["mpris"]["paused"],
            props={"style_classes": ["panel-font-icon", "player-icon"]},
        )

        self.play_pause_button = HoverButton(
            name="player-button",
            child=self.play_pause_icon,
            on_clicked=self.player.play_pause,
        )

        self.player.bind_property("can_pause", self.play_pause_button, "sensitive")

        self.next_button = HoverButton(
            style_classes=["player-button"],
            child=self.skip_next_icon,
            on_clicked=self.on_player_next,
        )
        self.player.bind_property("can_go_next", self.next_button, "sensitive")

        self.prev_button = HoverButton(
            style_classes=["player-button"],
            child=self.skip_prev_icon,
            on_clicked=self.on_player_prev,
        )
        self.shuffle_button = HoverButton(
            style_classes=["player-button"],
            child=self.shuffle_icon,
            on_clicked=self.player.toggle_shuffle,
        )
        self.player.bind_property("can_shuffle", self.shuffle_button, "sensitive")

        self.button_box.children = (
            self.shuffle_button,
            self.prev_button,
            self.play_pause_button,
            self.next_button,
        )
        self.player_info_box = Box(
            name="player-info-box",
            v_align="center",
            h_align="start",
            orientation="v",
            children=[self.track_info, self.seek_bar, self.controls_box],
        )

        self.inner_box = Box(
            name="inner-player-box",
            v_align="center",
            h_align="start",
        )
        # resize the inner box
        self.outer_box = Box(
            name="outer-player-box",
            h_align="start",
        )

        self.overlay_box = Overlay(
            child=self.outer_box,
            overlays=[
                self.inner_box,
                self.player_info_box,
                self.image_stack,
                Box(
                    children=Image(icon_name=self.player.player_name, icon_size=18),
                    h_align="end",
                    v_align="start",
                    style="margin-top: 5px; margin-right: 10px;",
                    tooltip_text=self.player.player_name,  # type: ignore
                ),
            ],
        )

        self.children = [*self.children, self.overlay_box]

        bulk_connect(
            self.player,
            {
                "exit": self.on_player_exit,
                "notify::playback-status": self.on_playback_change,
                "notify::shuffle": self.on_shuffle_update,
                "notify::metadata": self.on_metadata,
            },
        )

    def on_metadata(self, *_):
        self._set_image()

        duration = self.player.length

        if duration:
            self.length_label.set_label(self.length_str(self.player.length))
            self.seek_bar.set_range(0, duration)

        invoke_repeater(1000, self._move_seekbar)

    def _set_notify_value(self, p, *_):
        self.image_box.angle = self.angle_direction * p.value

    def on_player_exit(self, _, value):
        self.exit = value
        self.destroy()

    def on_player_next(self, *_):
        self.angle_direction = 1

        from shared.animator import Animator

        if self.art_animator is None:
            self.art_animator = Animator(
                timing_function=partial(cubic_bezier, 0, 0, 1, 1),
                duration=4,
                min_value=0,
                max_value=360,
                tick_widget=self.image_box,
                notify_value=self._set_notify_value,
            )

        self.art_animator.play()
        self.player.next()

    def on_player_prev(self, *_):
        self.angle_direction = -1
        self.art_animator.play()
        self.player.previous()

    def on_shuffle_update(self, *_):
        if self.player.shuffle is None:
            return
        if self.player.shuffle is True:
            self.shuffle_icon.style_classes = []
            self.shuffle_icon.add_style_class("shuffle-on")
        else:
            self.shuffle_icon.style_classes = []
            self.shuffle_icon.add_style_class("shuffle-off")

    def length_str(self, micro_seconds: int) -> str:
        micro_to_seconds = 1000000
        seconds = int(micro_seconds / micro_to_seconds)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"

    def on_playback_change(self, player, status):
        status = player.get_property("playback-status")

        if status == "paused":
            self.play_pause_icon.set_label(
                text_icons["mpris"]["playing"],
            )

        if status == "playing":
            self.play_pause_icon.set_label(
                text_icons["mpris"]["paused"],
            )

    def _update_image(self, image_path):
        if image_path and os.path.isfile(image_path):
            self.image_box.set_image_from_file(image_path)
            self.update_colors(image_path)
        else:
            self.image_box.set_image_from_file(self.fallback_cover_path)
            self.update_colors(self.fallback_cover_path)

    def on_accent_color(self, palette):
        default_color = (255, 0, 0)  # fallback color

        base_color = palette[0] if palette else default_color
        mix_target = (247, 239, 209)  # #F7EFD1

        # Mix base color with the target color
        mixed_color = mix_colors(base_color, mix_target, 0.5)
        # Then apply a tint to lighten it a bit more (e.g., 20%)
        tinted_color = tint_color(mixed_color, 0.2)

        mixed_css_color = rgb_to_css(tinted_color)

        bg = f"background-color: {mixed_css_color};"
        border = f"border-color: {mixed_css_color};"

        self.seek_bar.set_style(
            f"trough highlight {{ {bg} {border} }} slider {{ {bg} }}"
        )

        css_colors = [rgb_to_css(color) for color in palette]
        gradient = f"linear-gradient(135deg, {', '.join(css_colors)})"

        self.inner_box.set_style(f"background: {gradient};")

    def update_colors(self, image_path):
        get_simple_palette_threaded(
            image_path=image_path, color_count=5, callback=self.on_accent_color
        )

    def _set_image(self, *_):
        art_url = self.player.arturl

        parsed = urllib.parse.urlparse(art_url)
        if parsed.scheme == "file":
            local_arturl = urllib.parse.unquote(parsed.path)
            self._update_image(local_arturl)
        elif parsed.scheme in ("http", "https"):
            GLib.Thread.new("download-artwork", self._download_and_set_artwork, art_url)
        else:
            self._update_image(art_url)

    def _download_and_set_artwork(self, arturl):
        """
        Download the artwork from the given URL asynchronously and update the cover
        using GLib.idle_add to ensure UI updates occur on the main thread.
        """
        try:
            parsed = urllib.parse.urlparse(arturl)
            suffix = os.path.splitext(parsed.path)[1] or ".png"
            with urllib.request.urlopen(arturl) as response:
                data = response.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(data)
                local_arturl = temp_file.name
        except Exception:
            local_arturl = self.fallback_cover_path
        GLib.idle_add(self._update_image, local_arturl)
        return None

    def _move_seekbar(self, *_):
        if self.player is None or self.exit:
            return False

        self.position_label.set_label(self.length_str(self.player.position))
        self.seek_bar.set_value(self.player.position)

        return True

    @cooldown(0.1)
    def on_scale_move(self, scale: Scale, event, pos: int):
        self.player.position = pos
        self.position_label.set_label(self.length_str(pos))
        self.seek_bar.set_value(pos)
