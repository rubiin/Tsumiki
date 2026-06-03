import json

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import Gdk, GLib, Gtk, bulk_connect, logger, truncate
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window

from utils.app import AppUtils
from utils.config import widget_config
from utils.constants import PINNED_APPS_FILE
from utils.functions import (
    normalize_address,
    read_json_file,
    write_json_file,
)
from utils.icon_resolver import IconResolver
from utils.widget_settings import BarConfig

# DnD target for dock app reordering
DOCK_DND_TARGET = [Gtk.TargetEntry.new("dock-app", Gtk.TargetFlags.SAME_APP, 0)]
DOCK_SYNC_DEBOUNCE_MS = 60


class NativeClient:
    """Lightweight Hyprland client adapter matching dock expectations."""

    __slots__ = ("_active", "_data", "_hyprland_connection")

    def __init__(self, data: dict, hyprland_connection, active_address: str | None):
        self._data = data
        self._hyprland_connection = hyprland_connection
        self._active = normalize_address(data.get("address")) == active_address

    def get_app_id(self) -> str:
        return self._data.get("initialClass") or self._data.get("class") or ""

    def get_title(self) -> str:
        return self._data.get("title") or self.get_app_id()

    def get_hyprland_address(self) -> int:
        addr = normalize_address(self._data.get("address"))
        return int(addr, 16) if addr else 0

    def get_address_str(self) -> str | None:
        return normalize_address(self._data.get("address"))

    def get_fullscreen(self) -> bool:
        return bool(self._data.get("fullscreen", False))

    def get_activated(self) -> bool:
        return self._active

    def set_activated(self, active: bool):
        self._active = active

    def activate(self):
        addr = self.get_address_str()
        if addr:
            self._hyprland_connection.send_command_async(
                f"dispatch focuswindow address:{addr}",
                lambda *_: None,
            )

    def close(self):
        addr = self.get_address_str()
        if addr:
            self._hyprland_connection.send_command_async(
                f"dispatch closewindow address:{addr}",
                lambda *_: None,
            )

    def fullscreen(self):
        self.activate()
        self._hyprland_connection.send_command_async(
            "dispatch fullscreen 1",
            lambda *_: None,
        )

    def unfullscreen(self):
        self.activate()
        self._hyprland_connection.send_command_async(
            "dispatch fullscreen 0",
            lambda *_: None,
        )


class MultiDotIndicator(Gtk.DrawingArea):
    """A dot indicator widget that can show multiple dots for grouped apps."""

    def __init__(self, count=1, size=5, spacing=3, orientation="vertical"):
        super().__init__(visible=True)
        self._count = count
        self._size = size
        self._spacing = spacing
        self._orientation = orientation
        self._update_size()
        self.connect("draw", self.on_draw)

    def _update_size(self):
        if self._orientation == "vertical":
            # Dots stacked vertically (for horizontal dock)
            width = self._size
            height = (self._size * self._count) + (self._spacing * (self._count - 1))
        else:
            # Dots side by side (for vertical dock)
            width = (self._size * self._count) + (self._spacing * (self._count - 1))
            height = self._size
        self.set_size_request(width, height)

    def set_count(self, count: int):
        self._count = max(1, min(count, 5))  # Limit to 5 dots max
        self._update_size()
        self.queue_draw()

    def on_draw(self, area, cr):
        alloc = self.get_allocation()
        radius = self._size / 2 - 1
        cr.set_source_rgb(1.0, 1.0, 1.0)  # white dot

        for i in range(self._count):
            if self._orientation == "vertical":
                cx = alloc.width / 2
                cy = radius + 1 + i * (self._size + self._spacing)
            else:
                cx = radius + 1 + i * (self._size + self._spacing)
                cy = alloc.height / 2

            cr.arc(cx, cy, radius, 0, 2 * 3.14)
            cr.fill()


class DotIndicator(Gtk.DrawingArea):
    """A simple dot indicator widget."""

    def __init__(self, size=5):
        super().__init__(
            visible=True,
        )
        self.set_size_request(size, size)
        self.connect("draw", self.on_draw)

    def on_draw(self, area, cr):
        alloc = self.get_allocation()
        radius = min(alloc.width, alloc.height) / 2 - 1
        cr.arc(alloc.width / 2, alloc.height / 2, radius, 0, 2 * 3.14)

        cr.set_source_rgb(1.0, 1.0, 1.0)  # white dot
        cr.fill()


class AppBar(Box):
    """A simple app bar widget for the dock."""

    __slots__ = (
        "_active_address",
        "_app_groups",
        "_app_util",
        "_clients_by_address",
        "_dragging_box",
        "_group_apps",
        "_hyprland_connection",
        "_is_dragging",
        "_parent",
        "_pinned_app_buttons",
        "_running_app_boxes",
        "_running_app_count",
        "_sync_in_progress",
        "_sync_scheduled_id",
        "app_launcher",
        "config",
        "icon_resolver",
        "icon_size",
        "menu",
        "orientation",
        "pinned_apps",
        "pinned_apps_container",
        "separator",
        "truncation_size",
    )

    @property
    def app_util(self) -> AppUtils:
        """Lazy-load AppUtils on first access."""
        if self._app_util is None:
            self._app_util = AppUtils()
        return self._app_util

    def on_launcher_clicked(self, *_):
        """Toggle the app launcher visibility."""
        if self.app_launcher is None:
            from modules.app_launcher import AppLauncher

            self.app_launcher = AppLauncher(widget_config)
        self.app_launcher.toggle()

    def _bake_button(self, **kwargs) -> Button:
        return Button(
            style_classes=["buttons-basic", "buttons-transition", "dock-button"],
            **kwargs,
        )

    def __init__(self, parent):
        self._parent = parent
        self._is_dragging = False
        self._dragging_box = None  # Track which box is being dragged

        self._app_util = None  # Lazy-load on first use

        self.config = parent.config
        self.menu = None
        self.app_launcher = None
        self.icon_size = self.config.get("icon_size", 30)
        self.orientation = self.config.get("orientation", "horizontal")
        self._group_apps = self.config.get("group_apps", True)
        self.show_launcher = self.config.get("show_launcher", True)
        self.launcher_position = self.config.get("launcher_position", "first")

        self.truncation_size = self.config.get("truncation_size", 20)

        # Track grouped apps: app_id -> {box, button, indicator, clients: []}
        self._app_groups = {}
        self._clients_by_address = {}
        self._running_app_boxes = {}
        self._active_address = None
        self._running_app_count = 0
        self._sync_scheduled_id = None
        self._sync_in_progress = False

        # Determine orientation for boxes
        is_vertical = self.orientation == "vertical"
        box_orientation = "vertical" if is_vertical else "horizontal"

        super().__init__(
            spacing=10,
            orientation=box_orientation,
            name="dock-bar",
            style_classes=["window-basic", "sleek-border", f"dock-{self.orientation}"],
        )

        if self.show_launcher:
            launcher_style = (
                "margin-bottom: 8px;" if is_vertical else "margin-right: 8px;"
            )

            launcher_button = Button(
                style=launcher_style,
                image=Image(
                    icon_name="view-app-grid-symbolic",
                    icon_size=self.icon_size,
                ),
                on_button_press_event=self.on_launcher_clicked,
            )
            self.add(launcher_button)

        self.pinned_apps = read_json_file(PINNED_APPS_FILE) or []
        self.icon_resolver = IconResolver()
        self._hyprland_connection = get_hyprland_connection()

        pinned_align = "h_align" if is_vertical else "v_align"
        self.pinned_apps_container = Box(
            spacing=7, orientation=box_orientation, **{pinned_align: "center"}
        )
        self.add(self.pinned_apps_container)

        self._pinned_app_buttons = {}  # app_id -> Button widget
        self._populate_pinned_apps(self.pinned_apps)

        bulk_connect(
            self._hyprland_connection,
            {
                "event::openwindow": self._on_hyprland_event,
                "event::closewindow": self._on_hyprland_event,
                "event::movewindow": self._on_hyprland_event,
                "event::activewindow": self._on_active_window_event,
                "event::activewindowv2": self._on_active_window_event,
                "event::windowtitle": self._on_hyprland_event,
            },
        )

        self.connect("destroy", self._on_destroy)

        if self._hyprland_connection.ready:
            self._sync_clients()
        else:
            self._hyprland_connection.connect("event::ready", self._on_hyprland_ready)

    def _on_hyprland_ready(self, *_):
        self._schedule_sync_clients(delay_ms=0)

    def _on_hyprland_event(self, *_):
        self._schedule_sync_clients()

    def _extract_active_address_from_event(self, event) -> str | None:
        data = getattr(event, "data", None)
        if data is None:
            return None

        if isinstance(data, str):
            parts = [part.strip() for part in data.split(",") if part.strip()]
        elif isinstance(data, (list, tuple)):
            parts = []
            for item in data:
                if item is None:
                    continue
                if isinstance(item, str):
                    parts.append(item.strip())
                else:
                    parts.append(str(item).strip())
        else:
            return None

        for token in reversed(parts):
            addr = normalize_address(token)
            if addr:
                return addr
        return None

    def _apply_active_state(self, active_address: str | None):
        self._active_address = active_address

        for address, client in self._clients_by_address.items():
            client.set_activated(address == active_address)

        if self._group_apps:
            for group in self._app_groups.values():
                if any(c.get_activated() for c in group["clients"]):
                    group["button"].add_style_class("active")
                else:
                    group["button"].remove_style_class("active")
                if self.config.get("tooltip", True) and group["clients"]:
                    active = next(
                        (c for c in group["clients"] if c.get_activated()),
                        group["clients"][0],
                    )
                    group["button"].set_tooltip_text(active.get_title())
        else:
            self._apply_ungrouped_active_styles()

    def _on_active_window_event(self, *_):
        if not self._clients_by_address:
            self._schedule_sync_clients(delay_ms=0)
            return

        event = _[1] if len(_) > 1 else None
        active_address = self._extract_active_address_from_event(event)
        if active_address is None:
            active_address = self._get_active_address()

        if active_address == self._active_address:
            return

        self._apply_active_state(active_address)

    def _schedule_sync_clients(self, delay_ms: int = DOCK_SYNC_DEBOUNCE_MS):
        if self._sync_scheduled_id is not None:
            return

        if delay_ms <= 0:
            self._sync_clients()
            return

        self._sync_scheduled_id = GLib.timeout_add(delay_ms, self._run_scheduled_sync)

    def _run_scheduled_sync(self):
        self._sync_scheduled_id = None
        self._sync_clients()
        return False

    def _on_destroy(self, *_):
        if self._sync_scheduled_id is not None:
            GLib.source_remove(self._sync_scheduled_id)
            self._sync_scheduled_id = None

    def _get_active_address(self) -> str | None:
        try:
            parsed = json.loads(
                self._hyprland_connection.send_command("j/activewindow")
                .reply.decode()
                .strip("\n")
            )
        except Exception:
            return None
        return normalize_address(parsed.get("address"))

    def _list_visible_clients(self) -> list[NativeClient]:
        try:
            raw_clients = json.loads(
                self._hyprland_connection.send_command("j/clients")
                .reply.decode()
                .strip("\n")
            )
        except Exception as e:
            logger.exception(f"[Dock] Failed to list clients: {e}")
            return []

        active_address = self._active_address
        if active_address is None:
            active_address = self._get_active_address()
        self._active_address = active_address

        clients = []
        for item in raw_clients:
            if item.get("workspace", {}).get("id", -1) <= 0:
                continue

            client = NativeClient(item, self._hyprland_connection, active_address)
            app_id = client.get_app_id()
            if not app_id or app_id in self.config.get("ignored_apps", []):
                continue
            clients.append(client)
        return clients

    def _capture_client_snapshot(
        self,
    ) -> tuple[list[NativeClient], dict[str, NativeClient]]:
        clients = self._list_visible_clients()
        clients_by_address = {
            client.get_address_str(): client
            for client in clients
            if client.get_address_str()
        }
        return clients, clients_by_address

    def _reconcile_clients(self, clients: list[NativeClient]):
        if self._group_apps:
            self._sync_grouped_clients(clients)
        else:
            self._sync_ungrouped_clients(clients)

    def _sync_clients(self):
        if self._sync_in_progress:
            self._schedule_sync_clients()
            return

        self._sync_in_progress = True
        try:
            clients, clients_by_address = self._capture_client_snapshot()
            self._clients_by_address = clients_by_address
            self._reconcile_clients(clients)
        finally:
            self._sync_in_progress = False

    def _populate_pinned_apps(self, apps: list):
        """Initial population of pinned apps (only called once at startup)."""
        for app in self.pinned_apps_container.get_children():
            self.pinned_apps_container.remove(app)
            app.destroy()
        self._pinned_app_buttons.clear()

        for item in apps:
            self._add_pinned_app_button(item)

    def _add_pinned_app_button(self, app_id: str) -> bool:
        """Add a single pinned app button. Returns True if added."""
        if app_id in self._pinned_app_buttons:
            return False  # Already exists

        app = self.app_util.find_app(app_id)
        if not app:
            return False

        btn = self._bake_button(
            name="pinned_app",
            tooltip_markup=app.display_name,
            image=Image(
                pixbuf=app.get_icon_pixbuf(self.icon_size),
                size=self.icon_size,
            ),
            on_clicked=lambda *_, app=app: app.launch(),
        )
        self._pinned_app_buttons[app_id] = btn
        self.pinned_apps_container.add(btn)
        return True

    def _remove_pinned_app_button(self, app_id: str) -> bool:
        """Remove a single pinned app button. Returns True if removed."""
        btn = self._pinned_app_buttons.pop(app_id, None)
        if btn:
            self.pinned_apps_container.remove(btn)
            btn.destroy()
            return True
        return False

    def _check_if_pinned(self, client: NativeClient) -> bool:
        """Check if a client is pinned."""
        return client.get_app_id() in self.pinned_apps

    def _open_new_window(self, client: NativeClient):
        app = self.app_util.find_app(client.get_app_id())
        if app:
            app.launch()
        else:
            logger.warning(f"[Dock] No application found for {client.get_app_id()}")

    def _toggle_floating(self, client: NativeClient):
        hex_address = client.get_address_str()
        if hex_address:
            self._hyprland_connection.send_command_async(
                f"dispatch togglefloating address:{hex_address}",
                lambda _: None,
            )

    def _toggle_fullscreen(self, client: NativeClient):
        try:
            if client.get_fullscreen():
                client.unfullscreen()
            else:
                client.fullscreen()
        except Exception as e:
            logger.exception(f"[Dock] Failed to toggle fullscreen: {e}")

    def _move_to_workspace(self, client: NativeClient, workspace: int):
        hex_address = client.get_address_str()
        if hex_address:
            self._hyprland_connection.send_command_async(
                f"dispatch movetoworkspace address:{hex_address} {workspace}",
                lambda _: None,
            )

    def _close_running_app(self, client: NativeClient):
        try:
            # Try to close the client gracefully first
            client.close()
        except Exception:
            # If that fails, try to get the app_id and use hyprctl to kill the window
            app_id = None
            try:
                app_id = client.get_app_id()
                if app_id:
                    # Use hyprctl to kill windows of this application class
                    self._hyprland_connection.send_command_async(
                        f"closewindow class:{app_id}", lambda _: None
                    )
            except Exception:
                logger.exception(f"[Dock] Failed to close client {app_id}")

    def _make_item(self, label: str, callback):
        mi = Gtk.MenuItem(label=label)
        mi.connect("activate", lambda *_: callback())
        return mi

    def _init_menu(self):
        """Initialize or clear the context menu."""
        if not self.menu:
            self.menu = Gtk.Menu()
        else:
            for item in self.menu.get_children():
                self.menu.remove(item)
                item.destroy()

    def _build_client_submenu(self, client: NativeClient) -> Gtk.Menu:
        """Build a submenu for a single client with toggle, close, workspace."""
        submenu = Gtk.Menu()

        # Activate
        submenu.add(self._make_item("Activate", lambda: client.activate()))

        # Toggle Floating
        submenu.add(
            self._make_item("Toggle Floating", lambda: self._toggle_floating(client))
        )

        # Toggle Fullscreen
        fs_label = (
            "Exit Full Screen" if client.get_fullscreen() else "Toggle Full Screen"
        )
        submenu.add(self._make_item(fs_label, lambda: self._toggle_fullscreen(client)))

        # Close
        submenu.add(self._make_item("Close", lambda: self._close_running_app(client)))

        submenu.add(Gtk.SeparatorMenuItem())

        # Workspace move options (1-8)
        for i in range(1, 9):
            ws_item = Gtk.MenuItem(label=f"Move to Workspace {i}")
            ws_item.connect(
                "activate", lambda *_, i=i: self._move_to_workspace(client, i)
            )
            submenu.add(ws_item)

        return submenu

    def _build_common_menu_items(
        self, client: NativeClient, clients: list | None = None
    ):
        """Build common menu items (close all, pin/unpin, new window)."""
        items = []
        clients = clients or [client]

        # Close All
        items.append(
            self._make_item(
                "Close All",
                lambda: [self._close_running_app(c) for c in clients.copy()],
            )
        )

        # Pin / Unpin
        if self._check_if_pinned(client):
            items.append(self._make_item("Unpin", lambda: self._unpin_app(client)))
        else:
            items.append(self._make_item("Pin", lambda: self._pin_running_app(client)))

        # New Window
        items.append(
            self._make_item("New Window", lambda: self._open_new_window(client))
        )

        return items

    def _render_context_menu(self, menu_spec: dict):
        """Render a context menu from a declarative specification."""
        self._init_menu()

        for instance in menu_spec.get("instances", []):
            item = Gtk.MenuItem(label=instance["label"])
            item.set_submenu(self._build_client_submenu(instance["client"]))
            self.menu.add(item)

        common_items = menu_spec.get("common_items", [])
        if common_items:
            self.menu.add(Gtk.SeparatorMenuItem())
            for item in common_items:
                self.menu.add(item)

        self.menu.show_all()

    def _show_menu(self, client: NativeClient):
        """Show the context menu for a single client."""
        title = truncate(
            client.get_title() or client.get_app_id() or "", self.truncation_size
        )
        menu_spec = {
            "instances": [{"label": title, "client": client}],
            "common_items": self._build_common_menu_items(client),
        }
        self._render_context_menu(menu_spec)

    def _save_pinned_apps(self):
        """Save pinned apps to file."""
        write_json_file(PINNED_APPS_FILE, self.pinned_apps)

    def _pin_running_app(self, client: NativeClient):
        app_id = client.get_app_id()
        if not self._check_if_pinned(client):
            self.pinned_apps.append(app_id)
            self._add_pinned_app_button(app_id)
            self._save_pinned_apps()

    def _unpin_app(self, client: NativeClient):
        app_id = client.get_app_id()
        if self._check_if_pinned(client):
            self.pinned_apps.remove(app_id)
            self._remove_pinned_app_button(app_id)
            self._save_pinned_apps()

    def on_app_id(self, client, client_button: Button, client_image: Image, *_):
        if client.get_app_id() in self.config.get("ignored_apps", []):
            client_button.destroy()
            client_image.destroy()
            return
        client_image.set_from_pixbuf(
            self.icon_resolver.get_icon_pixbuf(client.get_app_id(), self.icon_size)
        )
        client_button.set_tooltip_text(
            client.get_title() if self.config.get("tooltip", True) else None
        )

    def _get_app_id_safe(self, client: NativeClient) -> str | None:
        """Safely get app_id, returning None if not available yet."""
        try:
            app_id = client.get_app_id()
            return app_id if app_id else None
        except Exception:
            return None

    def _build_group_ui(self, app_id: str, clients: list[NativeClient]) -> dict:
        """Build grouped app UI widgets and return group state."""
        is_vertical = self.orientation == "vertical"
        indicator_orientation = "vertical" if is_vertical else "horizontal"

        client_image = Image(size=self.icon_size)
        indicator = MultiDotIndicator(
            count=max(1, len(clients)),
            size=5,
            spacing=3,
            orientation=indicator_orientation,
        )
        client_button = self._bake_button(image=client_image)

        if is_vertical:
            box = Box(
                orientation="horizontal",
                spacing=0,
                h_align="center",
                children=[
                    Box(v_align="center", children=[indicator]),
                    client_button,
                ],
            )
        else:
            box = Box(
                orientation="vertical",
                spacing=4,
                v_align="center",
                children=[
                    client_button,
                    Box(h_align="center", children=[indicator]),
                ],
            )

        box._dock_app_id = app_id
        return {
            "box": box,
            "button": client_button,
            "indicator": indicator,
            "image": client_image,
            "clients": clients,
        }

    def _activate_group(self, app_id: str):
        clients = self._app_groups.get(app_id, {}).get("clients", [])
        if len(clients) == 1:
            clients[0].activate()
            return
        if len(clients) <= 1:
            return

        active_idx = -1
        for i, client in enumerate(clients):
            if client.get_activated():
                active_idx = i
                break
        next_idx = (active_idx + 1) % len(clients)
        clients[next_idx].activate()

    def _wire_group_events(self, app_id: str, group: dict):
        client_button = group["button"]

        def on_button_press(_widget, event):
            if event.button != 3:
                return False
            clients = self._app_groups.get(app_id, {}).get("clients", [])
            if clients:
                self._show_group_menu(app_id, clients)
                self.menu.popup_at_pointer(event)
            return True

        def on_button_release(_widget, event):
            if event.button == 1 and not self._is_dragging:
                self._activate_group(app_id)
                return True
            return False

        bulk_connect(
            client_button,
            {
                "button-press-event": on_button_press,
                "button-release-event": on_button_release,
            },
        )

    def _wire_group_dnd(self, group: dict):
        box = group["box"]
        client_button = group["button"]
        client_image = group["image"]

        client_button.drag_source_set(
            start_button_mask=Gdk.ModifierType.BUTTON1_MASK,
            targets=DOCK_DND_TARGET,
            actions=Gdk.DragAction.MOVE,
        )
        client_button.connect("drag-begin", self._on_drag_begin, box, client_image)
        client_button.connect("drag-end", self._on_drag_end, box)

        box.drag_dest_set(Gtk.DestDefaults.ALL, DOCK_DND_TARGET, Gdk.DragAction.MOVE)
        box.connect("drag-data-received", self._on_drag_data_received)

    def _create_app_group(self, app_id: str, clients: list[NativeClient]):
        """Create a new app group for the given app id."""
        group = self._build_group_ui(app_id, clients)
        self._app_groups[app_id] = group

        self._wire_group_events(app_id, group)
        self._wire_group_dnd(group)
        self._refresh_group_visuals(app_id)

        self.add(group["box"])

    def _refresh_group_visuals(self, app_id: str):
        group = self._app_groups.get(app_id)
        if not group:
            return
        clients = group["clients"]
        if not clients:
            return

        group["indicator"].set_count(len(clients))
        group["image"].set_from_pixbuf(
            self.icon_resolver.get_icon_pixbuf(app_id, self.icon_size)
        )

        if self.config.get("tooltip", True):
            active = next((c for c in clients if c.get_activated()), clients[0])
            group["button"].set_tooltip_text(active.get_title())
        else:
            group["button"].set_tooltip_text(None)

        if any(c.get_activated() for c in clients):
            group["button"].add_style_class("active")
        else:
            group["button"].remove_style_class("active")

    def _sync_grouped_clients(self, clients: list[NativeClient]):
        grouped = {}
        for client in clients:
            grouped.setdefault(client.get_app_id(), []).append(client)

        stale_ids = [app_id for app_id in self._app_groups if app_id not in grouped]
        for app_id in stale_ids:
            group = self._app_groups.pop(app_id)
            self.remove(group["box"])
            group["box"].destroy()

        for app_id, app_clients in grouped.items():
            if app_id not in self._app_groups:
                self._create_app_group(app_id, app_clients)
                continue
            self._app_groups[app_id]["clients"] = app_clients
            self._refresh_group_visuals(app_id)

        for address in list(self._running_app_boxes):
            entry = self._running_app_boxes.pop(address)
            self.remove(entry["box"])
            entry["box"].destroy()
        self._running_app_count = 0

    def _add_ungrouped_client(self, client: NativeClient):
        client_image = Image(size=self.icon_size)
        client_image.set_from_pixbuf(
            self.icon_resolver.get_icon_pixbuf(client.get_app_id(), self.icon_size)
        )

        address = client.get_address_str()
        if not address:
            return

        client_button = self._bake_button(image=client_image)

        is_vertical = self.orientation == "vertical"
        if is_vertical:
            box = Box(
                orientation="horizontal",
                spacing=0,
                h_align="center",
                children=[DotIndicator(), client_button],
            )
        else:
            box = Box(
                orientation="vertical",
                spacing=4,
                v_align="center",
                children=[client_button, DotIndicator()],
            )

        box._dock_client_address = address
        client_button.connect(
            "button-press-event",
            lambda w, e, addr=address: self._on_button_press(w, e, addr),
        )
        client_button.connect(
            "button-release-event",
            lambda w, e, addr=address: self._on_button_release(w, e, addr),
        )

        client_button.drag_source_set(
            start_button_mask=Gdk.ModifierType.BUTTON1_MASK,
            targets=DOCK_DND_TARGET,
            actions=Gdk.DragAction.MOVE,
        )
        client_button.connect("drag-begin", self._on_drag_begin, box, client_image)
        client_button.connect("drag-data-get", self._on_drag_data_get, address)
        client_button.connect("drag-end", self._on_drag_end, box)

        box.drag_dest_set(Gtk.DestDefaults.ALL, DOCK_DND_TARGET, Gdk.DragAction.MOVE)
        box.connect("drag-data-received", self._on_drag_data_received)

        self._running_app_boxes[address] = {
            "box": box,
            "button": client_button,
            "image": client_image,
            "client": client,
        }
        self._running_app_count += 1
        self.add(box)

    def _clear_grouped_clients(self):
        for app_id in list(self._app_groups):
            group = self._app_groups.pop(app_id)
            self.remove(group["box"])
            group["box"].destroy()

    def _diff_ungrouped_clients(
        self, clients: list[NativeClient]
    ) -> tuple[list[str], list[NativeClient], list[NativeClient]]:
        target_by_address = {}
        for client in clients:
            address = client.get_address_str()
            if address:
                target_by_address[address] = client

        remove_addresses = [
            address
            for address in self._running_app_boxes
            if address not in target_by_address
        ]

        add_clients = []
        update_clients = []
        for address, client in target_by_address.items():
            if address in self._running_app_boxes:
                update_clients.append(client)
            else:
                add_clients.append(client)

        return remove_addresses, add_clients, update_clients

    def _apply_ungrouped_removals(self, remove_addresses: list[str]):
        for address in remove_addresses:
            entry = self._running_app_boxes.pop(address, None)
            if not entry:
                continue
            self.remove(entry["box"])
            entry["box"].destroy()
            self._running_app_count -= 1

    def _apply_ungrouped_additions(self, add_clients: list[NativeClient]):
        for client in add_clients:
            self._add_ungrouped_client(client)

    def _apply_ungrouped_updates(self, update_clients: list[NativeClient]):
        for client in update_clients:
            address = client.get_address_str()
            if not address:
                continue

            entry = self._running_app_boxes.get(address)
            if not entry:
                continue

            entry["client"] = client
            entry["image"].set_from_pixbuf(
                self.icon_resolver.get_icon_pixbuf(client.get_app_id(), self.icon_size)
            )
            entry["button"].set_tooltip_text(
                client.get_title() if self.config.get("tooltip", True) else None
            )

    def _apply_ungrouped_active_styles(self):
        for entry in self._running_app_boxes.values():
            client = entry["client"]
            if client.get_activated():
                entry["button"].add_style_class("active")
            else:
                entry["button"].remove_style_class("active")

    def _sync_ungrouped_clients(self, clients: list[NativeClient]):
        self._clear_grouped_clients()

        remove_addresses, add_clients, update_clients = self._diff_ungrouped_clients(
            clients
        )

        self._apply_ungrouped_removals(remove_addresses)
        self._apply_ungrouped_additions(add_clients)
        self._apply_ungrouped_updates(update_clients)
        self._apply_ungrouped_active_styles()

    def _show_group_menu(self, app_id: str, clients: list):
        """Show context menu for a grouped app (multiple windows)."""
        menu_spec = {
            "instances": [
                {
                    "label": truncate(
                        client.get_title() or app_id,
                        self.truncation_size,
                    ),
                    "client": client,
                }
                for client in clients
            ],
            "common_items": self._build_common_menu_items(clients[0], clients),
        }
        self._render_context_menu(menu_spec)

    def _on_button_press(self, widget, event, address: str):
        """Handle button press - right click shows menu."""
        client = self._clients_by_address.get(address)
        if not client:
            return False
        if event.button == 3:
            self._show_menu(client)
            self.menu.popup_at_pointer(event)
            return True
        return False

    def _on_button_release(self, widget, event, address: str):
        """Handle button release - activate window if no drag occurred."""
        client = self._clients_by_address.get(address)
        if not client:
            return False
        if event.button == 1 and not self._is_dragging:
            client.activate()
            return True
        return False

    def _on_drag_begin(self, widget, context, box, client_image):
        """Handle drag start."""
        self._is_dragging = True
        self._dragging_box = box
        # Use the app's actual icon as drag icon
        pixbuf = client_image.get_pixbuf()
        if pixbuf:
            Gtk.drag_set_icon_pixbuf(context, pixbuf, 0, 0)
        else:
            Gtk.drag_set_icon_name(context, "application-x-executable", 0, 0)

    def _on_drag_end(self, widget, context, box):
        """Handle drag end."""
        self._is_dragging = False
        self._dragging_box = None

    def _on_drag_data_get(self, widget, context, data, info, time, address: str):
        """Provide the dragged client's address for identification."""
        try:
            data.set(data.get_target(), 8, address.encode())
        except Exception as e:
            logger.exception(f"[Dock] Failed to get drag data: {e}")

    def _on_drag_data_received(self, widget, context, x, y, data, info, time):
        """Handle drop - reorder the dock apps."""
        source_box = self._dragging_box
        if source_box is None or source_box == widget:
            return

        self.reorder_child(source_box, self._get_child_position(widget))

    def _get_child_position(self, widget):
        """Get the position of a widget in the box."""
        children = self.get_children()
        try:
            return children.index(widget)
        except ValueError:
            return -1


class Dock(Window):
    """A dock for applications."""

    def __init__(self, config: BarConfig):
        self.config = config.get("modules", {}).get("dock", {})
        self._app_bar = AppBar(self)

        # Determine orientation and set appropriate styles
        orientation = self.config.get("orientation", "horizontal")
        is_vertical = orientation == "vertical"

        # Set padding and transition based on orientation
        if is_vertical:
            padding_style = "padding: 50px 5px 50px 20px;"
            transition_type = "slide-right"
        else:
            padding_style = "padding: 20px 50px 5px 50px;"
            transition_type = "slide-up"

        self.revealer = Revealer(
            child=Box(children=[self._app_bar], style=padding_style),
            transition_duration=500,
            transition_type=transition_type,
        )

        if self.config.get("behavior", "always_show") == "always_show":
            self.revealer.set_reveal_child(True)
            child = self.revealer
        else:
            # Adjust CenterBox for vertical orientation
            if is_vertical:
                centerbox = CenterBox(
                    orientation="vertical",
                    center_children=self.revealer,
                    start_children=Box(style="min-height: 5px; min-width: 10px;"),
                    end_children=Box(style="min-height: 5px; min-width: 10px;"),
                )
            else:
                centerbox = CenterBox(
                    center_children=self.revealer,
                    start_children=Box(style="min-height: 10px; min-width: 5px;"),
                    end_children=Box(style="min-height: 10px; min-width: 5px;"),
                )

            child = EventBox(
                events=["enter-notify", "leave-notify"],
                child=centerbox,
                on_enter_notify_event=lambda *_: self.revealer.set_reveal_child(True),
                on_leave_notify_event=lambda *_: self._on_leave_notify(),
            )

        if (
            self.config.get("show_when_no_windows", False)
            and self.config.get("behavior", "always_hide") == "intellihide"
        ):
            self._hyprland_connection = get_hyprland_connection()

            bulk_connect(
                self._hyprland_connection,
                {
                    "event::workspace": self._check_for_windows,
                    "event::closewindow": self._check_for_windows,
                    "event::openwindow": self._check_for_windows,
                    "event::movewindow": self._check_for_windows,
                },
            )

            self._check_for_windows()

        # Determine anchor based on config or default based on orientation
        default_anchor = "center-left" if is_vertical else "bottom-center"
        anchor = self.config.get("anchor", default_anchor)

        super().__init__(
            layer=self.config.get("layer", "top"),
            anchor=anchor,
            child=child,
            name="dock",
            title="dock",
        )

    def _on_leave_notify(self):
        """Hide dock on leave, unless a drag is in progress."""
        if not self._app_bar._is_dragging:
            self.revealer.set_reveal_child(False)

    def _handle_workspace_response(self, data: str):
        try:
            parsed = json.loads(data)
            if parsed.get("windows", 0) == 0:
                self.revealer.set_reveal_child(True)
            else:
                self.revealer.set_reveal_child(False)
        except (json.JSONDecodeError, AttributeError) as e:
            logger.exception(f"[Dock] Failed to parse workspace response: {e}")

    def _check_for_windows(self, *_):
        try:
            self._hyprland_connection.send_command_async(
                "j/activeworkspace",
                lambda res, *_: self._handle_workspace_response(
                    res.reply.decode().strip("\n")
                ),
            )
        except Exception as e:
            logger.exception(f"[Dock] Failed to get active workspace: {e}")
