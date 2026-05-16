import json
from contextlib import suppress

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import Gdk, GdkPixbuf, GLib, Gtk, bulk_connect, logger
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.grid import Grid
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

from shared.popup import PopupWindow
from utils.app import AppUtils
from utils.icon_resolver import IconResolver
from utils.widget_settings import BarConfig
from utils.widget_utils import create_surface_from_widget

SCALE = 0.14
TARGET = [Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 0)]


def _resolve_icon_pixbuf(
    icon_resolver: IconResolver,
    app_id: str,
    size: int,
    desktop_app=None,
) -> GdkPixbuf.Pixbuf | None:
    """Resolve icon pixbuf with desktop-app -> resolver -> fallback chain."""
    pixbuf = None
    if desktop_app:
        pixbuf = desktop_app.get_icon_pixbuf(size=size)
    if not pixbuf:
        pixbuf = icon_resolver.get_icon_pixbuf(app_id, size)
    if not pixbuf:
        pixbuf = icon_resolver.get_icon_pixbuf(
            "application-x-executable-symbolic", size
        )
    if not pixbuf:
        pixbuf = icon_resolver.get_icon_pixbuf("image-missing", size)
    if pixbuf and (pixbuf.get_width() != size or pixbuf.get_height() != size):
        pixbuf = pixbuf.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
    return pixbuf


class HyprlandWindowButton(Button):
    """A button to show a window in the overview."""

    def __init__(
        self,
        window: Box,
        title: str,
        address: str,
        app_id: str,
        size,
        transform: int = 0,
        hyprland_connection=None,
        app_util=None,
    ):
        self.transform = transform % 4
        self.size = size if transform in [0, 2] else (size[1], size[0])
        self.address = address
        self.app_id = app_id
        self.title = title
        self.window: Box = window
        self.icon_resolver = IconResolver()
        self._hyprland_connection = hyprland_connection or get_hyprland_connection()

        # Compute dynamic icon sizes based on the button size.
        # Using the minimum dimension of the button for scaling.
        icon_size_main = int(min(self.size) * 0.5)  # adjust factor as needed

        # Enhanced icon resolution using desktop apps
        if app_util is None:
            app_util = AppUtils()
        desktop_app = app_util.find_app(app_id)
        icon_pixbuf = _resolve_icon_pixbuf(
            self.icon_resolver, app_id, icon_size_main, desktop_app
        )

        super().__init__(
            name="overview-client-box",
            image=Image(pixbuf=icon_pixbuf),
            tooltip_text=title,
            size=size,
            on_clicked=self.on_click,
            on_button_press_event=lambda _, event: (
                self._hyprland_connection.send_command(
                    f"/dispatch closewindow address:{address}"
                )
                if event.button == 3
                else None
            ),
            on_drag_data_get=lambda _s, _c, data, *_: data.set_text(
                address, len(address)
            ),
            on_drag_begin=lambda _, context: Gtk.drag_set_icon_surface(
                context, create_surface_from_widget(self, (255, 255, 255, 0))
            ),
        )

        # Store the desktop_app for later use
        self.desktop_app = desktop_app

        self.drag_source_set(
            start_button_mask=Gdk.ModifierType.BUTTON1_MASK,
            targets=TARGET,
            actions=Gdk.DragAction.COPY,
        )

        self.connect("key_press_event", self.on_key_press_event)

    def on_key_press_event(self, widget, event):
        if (event.get_state() & Gdk.ModifierType.SHIFT_MASK) and event.keyval in (
            Gdk.KEY_Return,
            Gdk.KEY_KP_Enter,
            Gdk.KEY_space,
        ):
            self._hyprland_connection.send_command(
                f"/dispatch closewindow address:{self.address}"
            )
            return True
        return False

    def update_image(self, image):
        # Compute overlay icon size dynamically.
        icon_size_overlay = int(min(self.size) * 0.5)  # adjust factor as needed
        icon_pixbuf = _resolve_icon_pixbuf(
            self.icon_resolver, self.app_id, icon_size_overlay, self.desktop_app
        )

        self.set_image(
            Overlay(
                child=image,
                overlays=Image(
                    name="overview-icon",
                    pixbuf=icon_pixbuf,
                    h_align="center",
                    v_align="end",
                    tooltip_text=self.title,
                ),
            )
        )

    def on_click(self, *_):
        self._hyprland_connection.send_command(
            f"/dispatch focuswindow address:{self.address}"
        )


class WorkspaceEventBox(EventBox):
    """A widget to show a workspace in the overview."""

    def __init__(
        self,
        workspace_id: int,
        fixed: Gtk.Fixed | None = None,
        hyprland_connection=None,
    ):
        self.fixed = fixed

        screen = Gdk.Screen.get_default()
        current_width = screen.get_width()
        current_height = screen.get_height()

        self._hyprland_connection = hyprland_connection or get_hyprland_connection()

        super().__init__(
            name="overview-workspace-bg",
            h_expand=True,
            v_expand=True,
            size=(int(current_width * SCALE), int(current_height * SCALE)),
            child=fixed
            if fixed
            else Label(
                name="overview-add-label",
                h_expand=True,
                v_expand=True,
                label=f"{workspace_id}",
            ),
            on_drag_data_received=lambda _w, _c, _x, _y, data, *_: (
                self._hyprland_connection.send_command(
                    f"/dispatch movetoworkspacesilent {workspace_id},address:{data.get_data().decode()}"  # noqa: E501
                )
            ),
        )
        self.drag_dest_set(
            Gtk.DestDefaults.ALL,
            TARGET,
            Gdk.DragAction.COPY,
        )
        if fixed:
            fixed.show_all()


class OverviewMenu(Box):
    """A widget to show the overview of all workspaces and windows."""

    def __init__(self, **kwargs):
        # Initialize as a Box instead of a PopupWindow.
        super().__init__(name="overview-menu", orientation="v", spacing=8, **kwargs)
        self.workspace_boxes: dict[int, Gtk.Fixed] = {}
        self.workspace_overlays: dict[int, WorkspaceEventBox] = {}
        self.clients: dict[str, HyprlandWindowButton] = {}
        self._client_meta: dict[str, tuple] = {}
        self._update_source_id: int | None = None

        self._hyprland_connection = get_hyprland_connection()
        self._app_util = None  # Lazy-load on first access
        self._app_cache_dirty = False

        # Remove the window_class_aliases dictionary completely
        # TODO: replace with glace

        bulk_connect(
            self._hyprland_connection,
            {
                "event::openwindow": self._schedule_update,
                "event::closewindow": self._schedule_update,
                "event::movewindow": self._schedule_update,
            },
        )

        self._init_grid()
        self.update()

    def _init_grid(self):
        self.grid = Grid(
            row_spacing=7,
            column_spacing=7,
            column_homogeneous=True,
            row_homogeneous=True,
        )
        self.children = self.grid

        overlays = []
        for w_id in range(1, 11):
            fixed = Gtk.Fixed.new()
            self.workspace_boxes[w_id] = fixed

            overlay = WorkspaceEventBox(
                w_id,
                fixed,
                hyprland_connection=self._hyprland_connection,
            )
            self.workspace_overlays[w_id] = overlay
            overlays.append(overlay)

        self.grid.attach_flow(children=overlays, columns=5)

    @property
    def app_util(self) -> AppUtils:
        """Lazy-load AppUtils on first access."""
        if self._app_util is None:
            self._app_util = AppUtils()
        return self._app_util

    def _refresh_app_cache_if_needed(self):
        """Only refresh app cache when a new window appears with unknown app_id."""
        if self._app_cache_dirty and self._app_util is not None:
            self._app_util.refresh()
            self._app_cache_dirty = False

    def _schedule_update(self, *_):
        if self._update_source_id is not None:
            return
        self._update_source_id = GLib.timeout_add(80, self._run_scheduled_update)

    def _run_scheduled_update(self):
        self._update_source_id = None
        self.update(signal_update=True)
        return False

    def _create_client_button(
        self, client: dict, monitor_info: tuple
    ) -> HyprlandWindowButton:
        return HyprlandWindowButton(
            window=self,
            title=client["title"],
            address=client["address"],
            app_id=client["initialClass"],
            size=(client["size"][0] * SCALE, client["size"][1] * SCALE),
            transform=monitor_info[2],
            hyprland_connection=self._hyprland_connection,
            app_util=self.app_util,
        )

    def _build_client_target(self, client: dict, monitors: dict) -> tuple | None:
        workspace_id = client.get("workspace", {}).get("id", -1)
        if workspace_id <= 0:
            return None

        monitor_id = client.get("monitor")
        monitor_info = monitors.get(monitor_id)
        if monitor_info is None:
            return None

        address = client.get("address")
        if not address:
            return None

        x = abs(client["at"][0] - monitor_info[0]) * SCALE
        y = abs(client["at"][1] - monitor_info[1]) * SCALE

        meta = (
            workspace_id,
            x,
            y,
            client.get("title", ""),
            client.get("initialClass", ""),
            client.get("size", [0, 0])[0],
            client.get("size", [0, 0])[1],
            monitor_info[2],
        )
        return address, workspace_id, x, y, meta, monitor_info

    def _remove_client(self, address: str):
        button = self.clients.pop(address, None)
        self._client_meta.pop(address, None)
        if not button:
            return

        with suppress(Exception):
            parent = button.get_parent()
            if parent is not None:
                parent.remove(button)
        button.destroy()

    def _upsert_client(
        self,
        address: str,
        workspace_id: int,
        x: float,
        y: float,
        meta: tuple,
        client_data: dict,
        monitor_info: tuple,
    ):
        existing = self.clients.get(address)
        if existing is not None and self._client_meta.get(address) == meta:
            return

        if existing is not None:
            self._remove_client(address)

        button = self._create_client_button(client_data, monitor_info)
        self.clients[address] = button
        self._client_meta[address] = meta
        self.workspace_boxes[workspace_id].put(button, x, y)

    def _fetch_monitors(self) -> dict[int, tuple[int, int, int]]:
        monitors_data = json.loads(
            self._hyprland_connection.send_command("j/monitors")
            .reply.decode()
            .strip("\n")
        )
        return {
            monitor["id"]: (monitor["x"], monitor["y"], monitor["transform"])
            for monitor in monitors_data
        }

    def _fetch_clients(self) -> list[dict]:
        return json.loads(
            self._hyprland_connection.send_command("j/clients")
            .reply.decode()
            .strip("\n")
        )

    def update(self, signal_update=False):
        # Only refresh app cache if needed (marked dirty by unknown app_id)
        self._refresh_app_cache_if_needed()

        try:
            monitors = self._fetch_monitors()
            raw_clients = self._fetch_clients()
        except Exception as e:
            logger.exception(f"[Overview] Failed to update snapshot: {e}")
            return

        target_addresses = set()
        for client in raw_clients:
            target = self._build_client_target(client, monitors)
            if target is None:
                continue

            address, workspace_id, x, y, meta, monitor_info = target
            target_addresses.add(address)
            self._upsert_client(address, workspace_id, x, y, meta, client, monitor_info)

        stale_addresses = [
            address for address in self.clients if address not in target_addresses
        ]
        for address in stale_addresses:
            self._remove_client(address)

    def _update(self, *_):
        self._schedule_update(*_)


class OverViewOverlay(PopupWindow):
    """A popup window for selecting wallpapers."""

    def __init__(self, config: BarConfig):
        self.config = config.get("modules", {}).get("overview", {})
        super().__init__(
            name="overview",
            layer=self.config.get("layer", "top"),
            child=Box(
                orientation="v",
                children=[OverviewMenu()],
            ),
            transition_duration=self.config.get("transition_duration", 350),
            transition_type=self.config.get("transition_type", "crossfade"),
            anchor=self.config.get("anchor", "center"),
            enable_inhibitor=True,
            keyboard_mode="exclusive",
        )

    def toggle_popup(self, monitor: bool = False):
        super().toggle_popup(monitor)
