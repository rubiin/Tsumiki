# ruff: noqa: N802
import math
import os
from time import sleep
from typing import List

from fabric import Fabricator
from fabric.utils import bulk_connect, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.scale import Scale
from fabric.widgets.stack import Stack
from gi.repository import Gio, GLib, GObject
from loguru import logger

from services import MprisPlayer, MprisPlayerManager
from shared import Animator, CircleImage, HoverButton
from utils import APP_CACHE_DIRECTORY
from utils.functions import ensure_directory
from utils.icons import icons
from utils.widget_utils import setup_cursor_hover


class PlayerBoxStack(Box):
    """A widget that displays the current player information."""

    def __init__(self, mpris_manager: MprisPlayerManager, config, **kwargs):
        self.config = config

        ensure_directory(f"{APP_CACHE_DIRECTORY}/media")

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

        if player_name in self.config["ignore"]:
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
        players: List[PlayerBox] = self.player_stack.get_children()
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
            lambda *args: [
                new_button.destroy(),  # type: ignore
                self.player_buttons.pop(self.player_buttons.index(new_button)),
            ],
        )
        self.buttons_box.add_center(self.player_buttons[-1])


def easeOutBounce(t: float) -> float:
    if t < 4 / 11:
        return 121 * t * t / 16
    elif t < 8 / 11:
        return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
    elif t < 9 / 10:
        return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
    return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


def easeInBounce(t: float) -> float:
    return 1 - easeOutBounce(1 - t)


def easeInOutBounce(t: float) -> float:
    if t < 0.5:
        return (1 - easeInBounce(1 - t * 2)) / 2
    return (1 + easeOutBounce(t * 2 - 1)) / 2


def easeOutElastic(t: float) -> float:
    c4 = (2 * math.pi) / 3
    return math.sin((t * 10 - 0.75) * c4) * math.pow(2, -10 * t) + 1


class PlayerBox(Box):
    """A widget that displays the current player information."""

    def __init__(self, player: MprisPlayer, config, **kwargs):
        super().__init__(
            h_align="center",
            name="player-box",
            **kwargs,
            h_expand=True,
        )
        # Setup
        self.player: MprisPlayer = player
        self.cover_path = get_relative_path("../assets/images/disk.png")

        self.image_size = 115

        self.config = config

        # State
        self.exit = False
        self.angle_direction = 1
        self.skipped = False

        self.image_box = CircleImage(size=self.image_size, image_file=self.cover_path)

        self.image_box.set_size_request(self.image_size, self.image_size)

        self.image_stack = Box(
            h_align="start", v_align="start", name="player-image-stack"
        )
        self.image_stack.children = [*self.image_stack.children, self.image_box]

        self.player.connect("notify::arturl", self.set_image)

        self.art_animator = Animator(
            bezier_curve=(0, 0, 1, 1),
            duration=12,
            min_value=0,
            max_value=360,
            tick_widget=self,
            repeat=True,
            notify_value=lambda p, *_: self.image_box.set_angle(p.value),
        )

        # Track Info
        self.track_title = Label(
            label="No Title",
            name="player-title",
            justfication="left",
            max_chars_width=self.config["truncation_size"],
            ellipsization="end",
            h_align="start",
        )

        self.track_artist = Label(
            label="No Artist",
            name="player-artist",
            justfication="left",
            max_chars_width=self.config["truncation_size"],
            ellipsization="end",
            h_align="start",
            visible=self.config["show_artist"],
        )

        self.track_album = Label(
            label="No Album",
            name="player-album",
            justfication="left",
            max_chars_width=self.config["truncation_size"],
            ellipsization="end",
            h_align="start",
            visible=self.config["show_album"],
        )

        self.player.bind_property(
            "title",
            self.track_title,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: x if x != "" else "No Title",  # type: ignore
        )
        self.player.bind_property(
            "artist",
            self.track_artist,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: x if x != "" else "No Artist",  # type: ignore
        )

        self.player.bind_property(
            "album",
            self.track_album,
            "label",
            GObject.BindingFlags.DEFAULT,
            lambda _, x: x if x != "" else "No Album",  # type: ignore
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

        # Player Signals
        bulk_connect(
            self.player,
            {
                "notify::title": lambda *_: self.track_title.set_label(
                    self.player.title
                ),
                "exit": self.on_player_exit,
                "notify::playback-status": self.on_playback_change,
                "notify::shuffle": self.shuffle_update,
            },
        )

        def position_poll(_):
            while True:
                try:
                    yield self.player.position
                    sleep(1)
                except Exception:  # noqa: PERF203
                    self.player_fabricator.stop()

        # Create a fabricator to poll the system stats
        self.player_fabricator = Fabricator(poll_from=position_poll, stream=True)

        self.player_fabricator.connect("changed", lambda *_: self.move_seekbar())

        # Buttons
        self.button_box = Box(
            name="button-box",
            h_align="center",
            spacing=2,
        )

        self.position_label = Label(
            "00:00",
            v_align="center",
            style_classes="time-label",
            visible=self.config["show_time"],
        )
        self.length_label = Label(
            "00:00",
            v_align="center",
            style_classes="time-label",
            visible=self.config["show_time"],
        )

        self.controls_box = CenterBox(
            style_classes="player-controls",
            start_children=self.position_label,
            center_children=self.button_box,
            end_children=self.length_label,
        )

        icon_size = 15

        self.skip_next_icon = Image(
            icon_name=icons["mpris"]["next"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.skip_prev_icon = Image(
            icon_name=icons["mpris"]["prev"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.loop_icon = Image(
            icon_name=icons["mpris"]["prev"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.shuffle_icon = Image(
            icon_name=icons["mpris"]["shuffle"]["enabled"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.play_icon = Image(
            icon_name=icons["mpris"]["paused"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.pause_icon = Image(
            icon_name=icons["mpris"]["playing"],
            name="player-icon",
            icon_size=icon_size,
        )
        self.play_pause_stack = Stack()
        self.play_pause_stack.add_named(self.play_icon, "play")
        self.play_pause_stack.add_named(self.pause_icon, "pause")

        self.play_pause_button = HoverButton(
            name="player-button",
            child=self.play_pause_stack,
        )
        self.play_pause_button.connect("clicked", lambda _: self.player.play_pause())
        self.player.bind_property("can_pause", self.play_pause_button, "sensitive")

        self.next_button = HoverButton(name="player-button", child=self.skip_next_icon)
        self.next_button.connect("clicked", self.on_player_next)
        self.player.bind_property("can_go_next", self.next_button, "sensitive")

        self.prev_button = HoverButton(name="player-button", child=self.skip_prev_icon)
        self.prev_button.connect("clicked", self.on_player_prev)

        self.shuffle_button = HoverButton(name="player-button", child=self.shuffle_icon)
        self.shuffle_button.connect("clicked", lambda _: player.toggle_shuffle())
        self.player.bind_property("can_shuffle", self.shuffle_button, "sensitive")

        self.button_box.children = (
            self.shuffle_button,
            self.prev_button,
            self.play_pause_button,
            self.next_button,
        )

        # Seek Bar
        self.seek_bar = Scale(
            min_value=0,
            max_value=100,
            increments=(5, 5),
            orientation="h",
            draw_value=False,
            name="seek-bar",
        )

        setup_cursor_hover(self.seek_bar)

        self.player.connect(
            "notify::length",
            lambda _, x: (
                self.seek_bar.set_value(self.player.position),
                self.seek_bar.set_range(0, self.player.length),
                self.length_label.set_label(
                    self.length_str(self.player.length),
                ),
                self.art_animator.play(),
            )  # type: ignore
            if self.player.length
            else None,
        )
        self.player.bind_property("can-seek", self.seek_bar, "sensitive")

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
                    children=Image(icon_name=self.player.player_name, icon_size=20),
                    h_align="end",
                    v_align="start",
                    style="margin-top: 5px; margin-right: 10px;",
                    tooltip_text=self.player.player_name,  # type: ignore
                ),
            ],
        )
        self.children = [*self.children, self.overlay_box]

    def on_scale_move(self, scale: Scale, event, moved_pos: int):
        scale.set_value(moved_pos)
        self.player.position = moved_pos
        self.position_label.set_label(self.length_str(moved_pos))
        # self.player.set_position(moved_pos)

    def on_player_exit(self, _, value):
        self.exit = value
        self.destroy()

    def on_player_next(self, _):
        self.angle_direction = 1
        self.art_animator.pause()
        self.player.next()

    def on_player_prev(self, _):
        self.angle_direction = -1
        self.art_animator.pause()
        self.player.previous()

    def shuffle_update(self, _, __):
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
        status = self.player.playback_status
        if status == "paused":
            self.play_pause_button.get_child().set_visible_child_name("play")  # type: ignore
            self.art_animator.pause()
        if status == "playing":
            self.play_pause_button.get_child().set_visible_child_name("pause")  # type: ignore
            self.art_animator.play()

    def update_image(self):
        self.image_box.set_image_from_file(self.cover_path)

    def set_image(self, *args):
        url = self.player.arturl

        if url is None:
            return

        new_cover_path = (
            (
                f"{APP_CACHE_DIRECTORY}/media"
                + "/"
                + GLib.compute_checksum_for_string(GLib.ChecksumType.SHA1, url, -1)  # type: ignore
            )
            if url[0:7] != "file://"
            else url[7:]
        )

        if new_cover_path == self.cover_path:
            return

        self.cover_path = new_cover_path

        if os.path.exists(self.cover_path):
            self.update_image()
            return

        Gio.File.new_for_uri(uri=url).copy_async(
            Gio.File.new_for_path(self.cover_path),
            Gio.FileCopyFlags.OVERWRITE,
            GLib.PRIORITY_DEFAULT,
            None,
            None,
            self.img_callback,
        )

    def img_callback(self, source: Gio.File, result: Gio.AsyncResult):
        try:
            logger.info(f"[PLAYER] saving cover photo to {self.cover_path}")
            os.path.isfile(self.cover_path)
            # source.copy_finish(result)
            if os.path.isfile(self.cover_path):
                self.update_image()
        except ValueError:
            logger.error("[PLAYER] Failed to grab artUrl")

    def move_seekbar(self):
        self.position_label.set_label(self.length_str(self.player.position))
        if self.exit or not self.player.can_seek:
            return False
        self.seek_bar.set_value(self.player.position)
