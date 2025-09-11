import json
import random
from typing import Callable, TypedDict, cast

import gi
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils.helpers import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.fixed import Fixed
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from gi.repository import GdkPixbuf, GLib, Gtk
from loguru import logger

from shared.clippingbox import ClippingBox
from shared.popup import PopupWindow

try:
    gi.require_version("Glace", "0.1")
    from gi.repository import Glace
except:
    logger.error("[Pager] Can't import Glace")


class HyprlandClient(TypedDict):
    ""

    title: str
    initialClass: str
    initialTitle: str
    at: list[int]
    size: list[int]
    address: str
    mapped: bool
    hidden: bool
    workspace: dict[str, int | str]
    floating: bool
    monitor: int
    pid: int
    xwayland: bool
    pinned: bool
    fullscreen: bool
    fullscreenMode: int
    fakeFullscreen: bool
    grouped: list[str]
    swallowing: str
    focusHistoryID: int


class TickChoker:
    ""

    def __init__(
        self, widget: Gtk.Widget, target_fps: int, callback: Callable, *callback_data
    ):
        self.widget: Gtk.Widget = widget
        self.callback: Callable = callback
        self.callback_data = callback_data

        self.period: float = 1.0 / target_fps
        self.offset_time: float = random.uniform(0, self.period)
        self.last_tick_time: float = 0.0

        self.handler_id = 0

        self.widget.connect("map", self.on_map)
        self.widget.connect("unmap", self.on_unmap)

        self.wireup()

    def on_map(self, _):
        # don't stress hyprland by capturing and moving a window at the same time
        return invoke_repeater(
            round(self.offset_time * 500), self.wireup, initial_call=False
        )

    def on_unmap(self, _):
        return self.stop()

    def do_handle_tick(self, *_):
        if not self.widget.get_mapped():
            return False

        now = GLib.get_monotonic_time() / 1_000_000
        if self.last_tick_time == 0.0:
            self.last_tick_time = now + self.offset_time

        if now - self.last_tick_time >= self.period:
            self.last_tick_time = now
            self.callback(*self.callback_data)

        return True

    def wireup(self):
        self.stop()
        self.handler_id = self.widget.add_tick_callback(self.do_handle_tick)
        return

    def stop(self):
        if self.handler_id:
            self.widget.remove_tick_callback(self.handler_id)
            self.handler_id = 0
        return


class PagerClientView(Box):
    ""

    def __init__(
        self, client: Glace.Client, manager: Glace.Manager, scale: float = 0.1, **kwargs
    ):
        super().__init__(
            style_classes="pager-client", v_align="center", h_align="center", **kwargs
        )
        self.client = client
        self.manager = manager
        self.scale = scale

        self.image = Image(
            icon_name="image-missing",
            h_expand=True,
            v_expand=True,
        )
        self.overlay_container = Box(
            h_align="fill",
            v_align="fill",
            h_expand=True,
            v_expand=True,
            style_classes="overlay-container",
        )

        self.children = Overlay(
            child=ClippingBox(
                style_classes="pager-preview",
                children=self.image,
                h_expand=True,
                v_expand=True,
            ),
            overlays=self.overlay_container,
        )

        self.client.connect("close", self.do_handle_close)
        self.client.connect("notify::activated", self.do_update_focus_style)

        self.tick_handler = TickChoker(
            self,
            2,
            self.manager.capture_client,
            self.client,
            False,
            self.do_handle_capture,
        )

        self.show()

    def update_for_data(self, hyprland_data: HyprlandClient):
        self.set_size_request(
            *(round(val * self.scale) for val in hyprland_data["size"])
        )

        return self.do_update_focus_style()

    def do_update_focus_style(self, *_):
        if self.client.get_activated():
            return self.add_style_class("focused")
        return self.remove_style_class("focused")

    def do_handle_capture(self, pixbuf: GdkPixbuf.Pixbuf | None):
        if not pixbuf:
            return
        return self.image.set_from_pixbuf(
            pixbuf.scale_simple(
                round(pixbuf.get_width() * self.scale),
                round(pixbuf.get_height() * self.scale),
                GdkPixbuf.InterpType.BILINEAR,
            )
        )

    def do_handle_close(self, *_):
        self.tick_handler.stop()
        if not (pager := cast(Pager, self.get_ancestor(Pager))):
            return
        return pager.remove_client_view(self.client.get_hyprland_address())


class PagerWorkspaceView(Overlay):
    ""

    def __init__(self, workspace_id: int, workspace_data: dict, scale: float, **kwargs):
        super().__init__(style_classes="pager-workspace", **kwargs)
        self.workspace_id = workspace_id
        self.scale = scale

        self.background = Box(
            style_classes="pager-workspace-inner",
            children=Label(
                label=str(workspace_id),
                h_align="center",
                v_align="center",
                h_expand=True,
                v_expand=True,
                style_classes="pager-workspace-num",
            ),
        )

        self.client_container = Fixed()
        self.children = self.background
        self.overlays = self.client_container

        self.update_state(workspace_data)

    def update_state(self, workspace_data: dict):
        self.set_size_request(
            *(
                round(workspace_data.get("monitor", {}).get(dim, 0) * self.scale)
                for dim in ["width", "height"]
            )
        )
        if workspace_data.get("active", False):
            return self.background.add_style_class("focused")
        return self.background.remove_style_class("focused")

    def add_client(self, client_view: PagerClientView, x: int, y: int):
        if client_view.get_parent() is self.client_container:
            return self.client_container.move(client_view, x, y)
        if old_parent := client_view.get_parent():
            cast(Gtk.Container, old_parent).remove(client_view)
        return self.client_container.put(client_view, x, y)

    def remove_client(self, client_view: PagerClientView):
        # if client_view.get_parent() is self.client_container: ...
        return self.client_container.remove(client_view)


class Pager(Box):
    ""

    def __init__(self, scale: float = 0.11, **kwargs):
        super().__init__(orientation="h", style_classes="pager", spacing=4, **kwargs)
        self.scale = scale
        self.connection = get_hyprland_connection()

        self.clients: dict[int, PagerClientView] = {}
        self.workspaces: dict[int, PagerWorkspaceView] = {}

        self.manager = Glace.Manager(on_client_added=self.on_client_added)
        self.connection.connect("event", self.do_sync_state)
        self.show()

    def on_client_added(self, _, client: Glace.Client):
        return client.connect("notify::hyprland-address", self.on_client_ready)

    def on_client_ready(self, client: Glace.Client, _):
        if not (address := client.get_hyprland_address()) or address in self.clients:
            return

        self.clients[address] = PagerClientView(client, self.manager, self.scale)

        return self.do_sync_state()

    def remove_client_view(self, address: int):
        if client_view := self.clients.pop(address, None):
            client_view.destroy()
            if (parent := client_view.get_parent()) is not None:
                parent.remove(client_view)

    def do_sync_state(self, *_):
        if not self.connection.ready:
            return

        try:
            hypr_clients: list[HyprlandClient] = json.loads(
                self.connection.send_command("j/clients").reply.decode()
            )
            hypr_workspaces: list[dict] = json.loads(
                self.connection.send_command("j/workspaces").reply.decode()
            )
            hypr_monitors: list[dict] = json.loads(
                self.connection.send_command("j/monitors").reply.decode()
            )
            active_workspace_id: int = json.loads(
                self.connection.send_command("j/activeworkspace").reply.decode()
            )["id"]
        except (json.JSONDecodeError, KeyError) as e:
            return logger.error(f"[Pager] Failed to parse Hyprland IPC data: {e}")

        monitors_map = {m["name"]: m for m in hypr_monitors}
        hypr_workspace_ids = set()
        for ws_data in sorted(hypr_workspaces, key=lambda w: w["id"]):
            ws_id = ws_data["id"]
            hypr_workspace_ids.add(ws_id)

            ws_data["monitor"] = monitors_map.get(ws_data["monitor"], {})
            ws_data["active"] = ws_id == active_workspace_id

            if ws_id in self.workspaces:
                self.workspaces[ws_id].update_state(ws_data)
                continue

            workspace_view = PagerWorkspaceView(ws_id, ws_data, self.scale)
            self.workspaces[ws_id] = workspace_view
            self.add(workspace_view)
            self.reorder_child(workspace_view, ws_id)

        # old workspaces
        stale_workspace_ids = set(self.workspaces.keys()) - hypr_workspace_ids
        for ws_id in stale_workspace_ids:
            if not (old_ws_view := self.workspaces.pop(ws_id, None)):
                continue
            old_ws_view.destroy()

        # clients
        client_addresses = set()
        for client_data in hypr_clients:
            address = int(client_data["address"], 16)
            client_addresses.add(address)

            client_view = self.clients.get(address)
            if not client_view:
                continue  # this no good

            client_view.update_for_data(client_data)

            workspace_id = client_data["workspace"]["id"]
            workspace_view = self.workspaces.get(workspace_id)
            if not workspace_view:
                continue  # orphan client.. how?

            workspace_view.add_client(
                client_view, *(round(val * self.scale) for val in client_data["at"])
            )

        # old clients
        stale_client_addresses = set(self.clients.keys()) - client_addresses
        for address in stale_client_addresses:
            self.remove_client_view(address)

        return True


class OverViewOverlay(PopupWindow):
    """A popup window for selecting wallpapers."""

    def __init__(self):
        super().__init__(
            layer="top",
            child=Box(
                orientation="v",
                children=[Pager()],
            ),
            transition_duration=300,
            transition_type="crossfade",
            anchor="center",
            enable_inhibitor=True,
            keyboard_mode="exclusive",
        )

    def toggle_popup(self, monitor: bool = False):
        super().toggle_popup(monitor)
