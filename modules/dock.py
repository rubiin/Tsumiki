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
        "_dragging_box",
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

    def _show_menu(self, client: Glace.Client):
        """Show the context menu for a client."""

        self._close_popup()

        if not self.menu:
            self.menu = Gtk.Menu()
        else:
            for title_item in self.menu.get_children():
                self.menu.remove(title_item)
                title_item.destroy()

        new_window = self._make_item(
            "New Window", lambda: self._open_new_window(client)
        )
        toggle_full_screen = self._make_item(
            "Toggle Full Screen", lambda: self._toggle_fullscreen(client)
        )
        toggle_floating = self._make_item(
            "Toggle Floating", lambda: self._toggle_floating(client)
        )
        close_item = self._make_item("Close", lambda: self._close_running_app(client))
        close_all_item = self._make_item(
            "Close All", lambda: self._close_running_app(client)
        )

        title_item = Gtk.MenuItem(label=truncate(client.get_title(), 20))

        item_menu = Gtk.Menu()
        title_item.set_submenu(item_menu)

        if client.get_fullscreen():
            toggle_full_screen.set_label("Exit Full Screen")

        for i in range(1, 10):
            ws_item = Gtk.MenuItem(label=f"Move to Workspace {i}")
            ws_item.connect(
                "activate", lambda *_, i=i: self._move_to_workspace(client, i)
            )

            item_menu.add(ws_item)

        # Pin / Unpin
        if self._check_if_pinned(client):
            pin_item = self._make_item("Unpin", lambda: self._unpin_app(client))
        else:
            pin_item = self._make_item("Pin", lambda: self._pin_running_app(client))

        close_item.connect("activate", lambda *_: self._close_running_app(client))
        new_window.connect("activate", lambda *_: self._open_new_window(client))

        toggle_full_screen.connect(
            "activate", lambda *_: self._toggle_fullscreen(client)
        )
        toggle_floating.connect("activate", lambda *_: self._toggle_floating(client))
        close_all_item.connect("activate", lambda *_: self._toggle_floating(client))

        # Add items to menu
        for item in [
            title_item,
            pin_item,
            new_window,
            toggle_full_screen,
            toggle_floating,
            close_item,
            close_all_item,
        ]:
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

    def on_client_added(self, _, client: Glace.Client):
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
