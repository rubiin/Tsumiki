import json

import gi
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import bulk_connect, logger, truncate
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.revealer import Revealer
from fabric.widgets.separator import Separator
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Gdk, Glace, GLib, Gtk

from modules.app_launcher import AppLauncher
from shared.popoverv1 import PopOverWindow
from utils.app import AppUtils
from utils.config import widget_config
from utils.constants import PINNED_APPS_FILE
from utils.functions import read_json_file, write_json_file
from utils.icon_resolver import IconResolver
from utils.widget_settings import BarConfig

gi.require_versions({"Glace": "0.1", "Gtk": "3.0"})

# DnD target for dock app reordering
DOCK_DND_TARGET = [Gtk.TargetEntry.new("dock-app", Gtk.TargetFlags.SAME_APP, 0)]


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

        for i in range(self._count):
            if self._orientation == "vertical":
                cx = alloc.width / 2
                cy = radius + 1 + i * (self._size + self._spacing)
            else:
                cx = radius + 1 + i * (self._size + self._spacing)
                cy = alloc.height / 2

            cr.arc(cx, cy, radius, 0, 2 * 3.14)
            cr.set_source_rgb(1.0, 1.0, 1.0)  # white dot
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
        "_all_apps",
        "_app_groups",
        "_dragging_box",
        "_group_apps",
        "_hyprland_connection",
        "_is_dragging",
        "_manager",
        "_parent",
        "_pinned_app_buttons",
        "_preview_image",
        "app_identifiers",
        "app_launcher",
        "app_util",
        "config",
        "icon_resolver",
        "icon_size",
        "menu",
        "orientation",
        "pinned_apps",
        "pinned_apps_container",
        "popup",
        "popup_revealer",
        "preview_size",
        "separator",
    )

    def on_launcher_clicked(self, *_):
        """Toggle the app launcher visibility."""
        if self.app_launcher is None:
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

        self.app_util = AppUtils()
        self._all_apps = self.app_util.all_applications
        self.app_identifiers = self.app_util.app_identifiers

        self.config = parent.config
        self.menu = None
        self.app_launcher = None
        self.icon_size = self.config.get("icon_size", 30)
        self.preview_size = self.config.get("preview_size", [40, 50])
        self.orientation = self.config.get("orientation", "horizontal")
        self._group_apps = self.config.get("group_apps", True)
        self.truncation_size = self.config.get("truncation_size", 20)

        # Track grouped apps: app_id -> {box, button, indicator, clients: []}
        self._app_groups = {}

        # Determine orientation for boxes
        is_vertical = self.orientation == "vertical"
        box_orientation = "vertical" if is_vertical else "horizontal"
        launcher_style = "margin-bottom: 8px;" if is_vertical else "margin-right: 8px;"

        launcher_button = Button(
            style=launcher_style,
            image=Image(
                icon_name="view-app-grid-symbolic",
                icon_size=self.icon_size,
            ),
            on_button_press_event=self.on_launcher_clicked,
        )

        super().__init__(
            spacing=10,
            orientation=box_orientation,
            name="dock-bar",
            style_classes=["window-basic", "sleek-border", f"dock-{self.orientation}"],
            children=[launcher_button],
        )
        self.pinned_apps = read_json_file(PINNED_APPS_FILE) or []
        self.icon_resolver = IconResolver()
        self._manager = Glace.Manager()
        self._manager.connect("client-added", self.on_client_added)
        self._preview_image = Image()
        self._hyprland_connection = get_hyprland_connection()

        pinned_align = "h_align" if is_vertical else "v_align"
        self.pinned_apps_container = Box(
            spacing=7, orientation=box_orientation, **{pinned_align: "center"}
        )
        self.add(self.pinned_apps_container)
        self.separator = Separator(
            orientation="horizontal" if is_vertical else "vertical", visible=False
        )
        self.add(self.separator)

        self._pinned_app_buttons = {}  # app_id -> Button widget
        self._populate_pinned_apps(self.pinned_apps)

        if self.config.get("preview_apps", True):
            self.popup_revealer = Revealer(
                child=Box(
                    children=self._preview_image,
                    style_classes=["window-basic", "sleek-border"],
                ),
                transition_type="crossfade",
                transition_duration=400,
            )

            self.popup = PopOverWindow(
                parent,
                child=self.popup_revealer,
                margin="0px 0px 80px 0px",
                visible=False,
            )

            self.popup_revealer.connect(
                "notify::child-revealed",
                lambda *_: self.popup.set_visible(False)
                if not self.popup_revealer.child_revealed
                else None,
            )

    def _close_popup(self, *_):
        self.popup_revealer.unreveal()
        return False

    def _capture_callback(self, pbuf, _):
        self._preview_image.set_from_pixbuf(
            pbuf.scale_simple(self.preview_size[0], self.preview_size[1], 2)
        )
        self.popup.set_visible(True)
        self.popup_revealer.reveal()

    def _update_preview_image(self, client: Glace.Client, client_button: Button):
        self.popup.set_pointing_to(client_button)

        self._manager.capture_client(
            client=client,
            overlay_cursor=False,
            callback=self._capture_callback,
            user_data=None,
        )

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

    def _check_if_pinned(self, client: Glace.Client) -> bool:
        """Check if a client is pinned."""
        return client.get_app_id() in self.pinned_apps

    def _open_new_window(self, client: Glace.Client):
        app = self.app_util.find_app(client.get_app_id())
        if app:
            app.launch()
        else:
            logger.warning(f"[Dock] No application found for {client.get_app_id()}")

    def _toggle_floating(self, client: Glace.Client):
        addr = client.get_hyprland_address()

        hex_address = hex(addr)
        if hex_address:
            self._hyprland_connection.send_command_async(
                f"dispatch togglefloating address:{hex_address}",
                lambda _: None,
            )

    def _toggle_fullscreen(self, client: Glace.Client):
        try:
            if client.get_fullscreen():
                client.unfullscreen()
            else:
                client.fullscreen()
        except Exception as e:
            logger.exception(f"[Dock] Failed to toggle fullscreen: {e}")

    def _move_to_workspace(self, client: Glace.Client, workspace: int):
        client_address = client.get_hyprland_address()
        hex_address = hex(client_address)
        if hex_address:
            self._hyprland_connection.send_command_async(
                f"dispatch movetoworkspace address:{hex_address} {workspace}",
                lambda _: None,
            )

    def _close_running_app(self, client: Glace.Client):
        try:
            # Try to close the client gracefully first
            client.close()
        except Exception:
            # If that fails, try to get the app_id and use hyprctl to kill the window
            try:
                app_id = client.get_app_id()
                if app_id:
                    # Use hyprctl to kill windows of this application class
                    self._hyprland_connection.send_command_async(
                        f"closewindow class:{app_id}", lambda _: None
                    )
            except Exception:
                logger.exception(f"[Dock] Failed to close client {client.get_app_id()}")

    def _make_item(self, label: str, callback):
        mi = Gtk.MenuItem(label=label)
        mi.connect("activate", lambda *_: callback())
        return mi

    def _init_menu(self):
        """Initialize or clear the context menu."""
        self._close_popup()
        if not self.menu:
            self.menu = Gtk.Menu()
        else:
            for item in self.menu.get_children():
                self.menu.remove(item)
                item.destroy()

    def _build_client_submenu(self, client: Glace.Client) -> Gtk.Menu:
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
        self, client: Glace.Client, clients: list | None = None
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

    def _show_menu(self, client: Glace.Client):
        """Show the context menu for a single client."""
        self._init_menu()

        # Instance with submenu
        title = truncate(
            client.get_title() or client.get_app_id() or "", self.truncation_size
        )
        instance_item = Gtk.MenuItem(label=title)
        instance_item.set_submenu(self._build_client_submenu(client))
        self.menu.add(instance_item)

        self.menu.add(Gtk.SeparatorMenuItem())

        # Common items (Close All, Pin/Unpin, New Window)
        for item in self._build_common_menu_items(client):
            self.menu.add(item)

        self.menu.show_all()

    def _save_pinned_apps(self):
        """Save pinned apps to file."""
        write_json_file(self.pinned_apps, PINNED_APPS_FILE)

    def _pin_running_app(self, client: Glace.Client):
        app_id = client.get_app_id()
        if not self._check_if_pinned(client):
            self.pinned_apps.append(app_id)
            self._add_pinned_app_button(app_id)
            self._save_pinned_apps()

    def _unpin_app(self, client: Glace.Client):
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

    def on_enter_notify_event(self, client: Glace.Client, client_button: Button):
        if self.config.get("preview_apps", False):
            self._update_preview_image(client, client_button)

    def on_leave_notify_event(self, client: Glace.Client, client_button: Button):
        if self.config.get("preview_apps", True):
            GLib.timeout_add(100, self._close_popup)

    def _on_group_enter(self, app_id: str, client_button: Button):
        """Handle hover on a grouped app - show preview of first/active window."""
        if not self.config.get("preview_apps", False):
            return
        group = self._app_groups.get(app_id)
        if not group or not group["clients"]:
            return
        # Show preview of active window, or first window if none active
        active_client = None
        for c in group["clients"]:
            if c.get_activated():
                active_client = c
                break
        if not active_client:
            active_client = group["clients"][0]
        self._update_preview_image(active_client, client_button)

    def _get_app_id_safe(self, client: Glace.Client) -> str | None:
        """Safely get app_id, returning None if not available yet."""
        try:
            app_id = client.get_app_id()
            return app_id if app_id else None
        except Exception:
            return None

    def _add_client_to_group(self, app_id: str, client: Glace.Client):
        """Add a client to an existing app group."""
        if app_id not in self._app_groups:
            return

        group = self._app_groups[app_id]
        group["clients"].append(client)
        group["indicator"].set_count(len(group["clients"]))

        # Update active state when this client's activated state changes
        def update_active(*_):
            # Check if any client in the group is activated
            any_active = any(c.get_activated() for c in group["clients"])
            if any_active:
                group["button"].add_style_class("active")
            else:
                group["button"].remove_style_class("active")

        def on_close(*_):
            self._remove_client_from_group(app_id, client)

        bulk_connect(
            client,
            {
                "notify::activated": update_active,
                "close": on_close,
            },
        )

    def _remove_client_from_group(self, app_id: str, client: Glace.Client):
        """Remove a client from an app group."""
        if app_id not in self._app_groups:
            return

        group = self._app_groups[app_id]
        if client in group["clients"]:
            group["clients"].remove(client)

        if len(group["clients"]) == 0:
            # No more clients, remove the group
            box = group["box"]
            self.remove(box)
            box.destroy()
            del self._app_groups[app_id]
        else:
            # Update the indicator count
            group["indicator"].set_count(len(group["clients"]))
            # Update active state
            any_active = any(c.get_activated() for c in group["clients"])
            if any_active:
                group["button"].add_style_class("active")
            else:
                group["button"].remove_style_class("active")

    def _create_app_group(self, app_id: str, client: Glace.Client):
        """Create a new app group for the given client."""
        is_vertical = self.orientation == "vertical"
        indicator_orientation = "vertical" if is_vertical else "horizontal"

        client_image = Image(size=self.icon_size)
        indicator = MultiDotIndicator(
            count=1,
            size=5,
            spacing=3,
            orientation=indicator_orientation,
        )

        client_button = self._bake_button(
            image=client_image,
            on_enter_notify_event=lambda *_: self._on_group_enter(
                app_id, client_button
            ),
            on_leave_notify_event=lambda *_: self.on_leave_notify_event(
                None, client_button
            ),
        )

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

        # Store group info
        self._app_groups[app_id] = {
            "box": box,
            "button": client_button,
            "indicator": indicator,
            "image": client_image,
            "clients": [client],
        }

        box._dock_app_id = app_id

        # Handle click - cycle through windows or activate single window
        def on_click(*_):
            clients = self._app_groups.get(app_id, {}).get("clients", [])
            if len(clients) == 1:
                clients[0].activate()
            elif len(clients) > 1:
                # Find current active and activate next
                active_idx = -1
                for i, c in enumerate(clients):
                    if c.get_activated():
                        active_idx = i
                        break
                next_idx = (active_idx + 1) % len(clients)
                clients[next_idx].activate()

        # Handle button press/release
        def on_button_press(w, e):
            if e.button == 3:
                clients = self._app_groups.get(app_id, {}).get("clients", [])
                if clients:
                    self._show_group_menu(app_id, clients)
                    self.menu.popup_at_pointer(e)
                return True
            return False

        def on_button_release(w, e):
            if e.button == 1 and not self._is_dragging:
                on_click()
                return True
            return False

        client_button.connect("button-press-event", on_button_press)
        client_button.connect("button-release-event", on_button_release)

        # Set up drag
        client_button.drag_source_set(
            start_button_mask=Gdk.ModifierType.BUTTON1_MASK,
            targets=DOCK_DND_TARGET,
            actions=Gdk.DragAction.MOVE,
        )
        client_button.connect("drag-begin", self._on_drag_begin, box, client_image)
        client_button.connect("drag-end", self._on_drag_end, box)

        box.drag_dest_set(
            Gtk.DestDefaults.ALL,
            DOCK_DND_TARGET,
            Gdk.DragAction.MOVE,
        )
        box.connect("drag-data-received", self._on_drag_data_received)

        # Set initial icon if app_id is available
        if app_id:
            client_image.set_from_pixbuf(
                self.icon_resolver.get_icon_pixbuf(app_id, self.icon_size)
            )
            client_button.set_tooltip_text(
                client.get_title() if self.config.get("tooltip", True) else None
            )

        # Update icon when app_id changes
        def on_app_id_change(*_):
            aid = self._get_app_id_safe(client)
            if aid and aid in self.config.get("ignored_apps", []):
                self._remove_client_from_group(app_id, client)
                return
            if aid:
                client_image.set_from_pixbuf(
                    self.icon_resolver.get_icon_pixbuf(aid, self.icon_size)
                )
            client_button.set_tooltip_text(
                client.get_title() if self.config.get("tooltip", True) else None
            )

        # Update active state
        def update_active(*_):
            clients = self._app_groups.get(app_id, {}).get("clients", [])
            any_active = any(c.get_activated() for c in clients)
            if any_active:
                client_button.add_style_class("active")
            else:
                client_button.remove_style_class("active")

        def on_close(*_):
            self._remove_client_from_group(app_id, client)

        bulk_connect(
            client,
            {
                "notify::app-id": on_app_id_change,
                "notify::activated": update_active,
                "close": on_close,
            },
        )

        self.add(box)

        if len(self.pinned_apps) > 0 and not self.separator.get_visible():
            self.separator.set_visible(True)

    def _show_group_menu(self, app_id: str, clients: list):
        """Show context menu for a grouped app (multiple windows)."""
        self._init_menu()

        # Add each instance with its submenu
        for client in clients:
            title = truncate(client.get_title() or app_id, self.truncation_size)
            instance_item = Gtk.MenuItem(label=title)
            instance_item.set_submenu(self._build_client_submenu(client))
            self.menu.add(instance_item)

        self.menu.add(Gtk.SeparatorMenuItem())

        # Common items (Close All, Pin/Unpin, New Window)
        for item in self._build_common_menu_items(clients[0], clients):
            self.menu.add(item)

        self.menu.show_all()

    def on_client_added(self, _, client: Glace.Client):
        app_id = self._get_app_id_safe(client)

        # If grouping is enabled
        if self._group_apps:
            if app_id:
                # Check if ignored
                if app_id in self.config.get("ignored_apps", []):
                    return
                # If we already have this app, add to existing group
                if app_id in self._app_groups:
                    self._add_client_to_group(app_id, client)
                    return
                # Create a new group
                self._create_app_group(app_id, client)
                return
            else:
                # app_id not available yet, wait for it
                def on_app_id_ready(*_):
                    aid = self._get_app_id_safe(client)
                    if aid:
                        client.disconnect_by_func(on_app_id_ready)
                        if aid in self.config.get("ignored_apps", []):
                            return
                        if aid in self._app_groups:
                            self._add_client_to_group(aid, client)
                        else:
                            self._create_app_group(aid, client)

                client.connect("notify::app-id", on_app_id_ready)
                return

        # Non-grouped mode (original behavior)
        client_image = Image(size=self.icon_size)

        client_button = self._bake_button(
            image=client_image,
            on_enter_notify_event=lambda *_: self.on_enter_notify_event(
                client, client_button
            ),
            on_leave_notify_event=lambda *_: self.on_leave_notify_event(
                client, client_button
            ),
        )

        is_vertical = self.orientation == "vertical"

        if is_vertical:
            # For vertical dock: horizontal box with dot beside button
            box = Box(
                orientation="horizontal",
                spacing=0,
                h_align="center",
                children=[
                    DotIndicator(),
                    client_button,
                ],
            )
        else:
            # For horizontal dock: vertical box with dot below button
            box = Box(
                orientation="vertical",
                spacing=4,
                v_align="center",
                children=[client_button, DotIndicator()],
            )
        # Store client reference on box for DnD
        box._dock_client = client

        # Handle button press/release manually to allow both click and drag
        client_button.connect(
            "button-press-event",
            lambda w, e: self._on_button_press(w, e, client),
        )
        client_button.connect(
            "button-release-event",
            lambda w, e: self._on_button_release(w, e, client),
        )

        # Set up drag source on the button
        client_button.drag_source_set(
            start_button_mask=Gdk.ModifierType.BUTTON1_MASK,
            targets=DOCK_DND_TARGET,
            actions=Gdk.DragAction.MOVE,
        )
        client_button.connect("drag-begin", self._on_drag_begin, box, client_image)
        client_button.connect("drag-data-get", self._on_drag_data_get, client)
        client_button.connect("drag-end", self._on_drag_end, box)

        # Set up drag destination on the box
        box.drag_dest_set(
            Gtk.DestDefaults.ALL,
            DOCK_DND_TARGET,
            Gdk.DragAction.MOVE,
        )
        box.connect("drag-data-received", self._on_drag_data_received)

        bulk_connect(
            client,
            {
                "notify::app-id": lambda *_: self.on_app_id(
                    client, client_button, client_image
                ),
                "notify::activated": lambda *_: client_button.add_style_class("active")
                if client.get_activated()
                else client_button.remove_style_class("active"),
                "close": lambda *_: (self.remove(box), box.destroy()),
            },
        )

        self.add(box)

        if len(self.pinned_apps) > 0 and not self.separator.get_visible():
            self.separator.set_visible(True)

    def _on_button_press(self, widget, event, client):
        """Handle button press - right click shows menu."""
        if event.button == 3:
            self._show_menu(client)
            self.menu.popup_at_pointer(event)
            return True
        return False

    def _on_button_release(self, widget, event, client):
        """Handle button release - activate window if no drag occurred."""
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

    def _on_drag_data_get(self, widget, context, data, info, time, client):
        """Provide the dragged client's address for identification."""
        try:
            addr = str(client.get_hyprland_address())
            data.set(data.get_target(), 8, addr.encode())
        except Exception as e:
            logger.warning(f"[Dock] Failed to get drag data: {e}")

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

    def _handle_workspace_response(self, data: dict):
        try:
            if data.get("windows", 0) == 0:
                self.revealer.set_reveal_child(True)
            else:
                self.revealer.set_reveal_child(False)
        except json.JSONDecodeError as e:
            logger.exception(f"[Dock] Failed to parse workspace response: {e}")
            return

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
            return
