import gi
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.revealer import Revealer
from fabric.widgets.separator import Separator
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Glace

from shared.popoverv1 import PopupWindow
from utils.app import AppUtils
from utils.icon_resolver import IconResolver
from utils.monitors import HyprlandWithMonitors

gi.require_version("Glace", "0.1")


class AppBar(Box):
    """A simple app bar widget for the dock."""

    def __init__(self, parent):
        self.client_buttons = {}
        self._parent = parent

        self.app_util = AppUtils()
        self._all_apps = self.app_util.all_applications
        self.app_identifiers = self.app_util.app_identifiers

        self.config = parent.config

        self.icon_size = self.config.get("icon_size", 30)
        self.preview_size = self.config.get("preview_size", [40, 50])

        super().__init__(
            spacing=10,
            name="app-bar",
            style_classes=["window-basic", "sleek-border"],
            children=[
                Button(
                    image=Image(
                        icon_name="view-app-grid-symbolic",
                        icon_size=self.icon_size,
                    ),
                    on_button_press_event=lambda *_: print(
                        self._parent.get_application().actions["toggle-appmenu"][0]()
                    ),
                )
            ],
        )
        self.icon_resolver = IconResolver()
        self._manager = Glace.Manager()
        self._manager.connect("client-added", self.on_client_added)
        self._preview_image = Image()
        self._hyp = HyprlandWithMonitors()

        self._add_pinned_apps()

        self.add(Separator())

        self.popup_revealer = Revealer(
            child=Box(
                children=self._preview_image,
                style_classes=["window-basic", "sleek-border"],
            ),
            transition_type="crossfade",
            transition_duration=400,
        )

        self.popup = PopupWindow(
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

    def update_preview_image(self, client, client_button: Button):
        self.popup.set_pointing_to(client_button)

        def capture_callback(pbuf, _):
            self._preview_image.set_from_pixbuf(
                pbuf.scale_simple(self.preview_size[0], self.preview_size[1], 2)
            )
            self.popup.set_visible(True)
            self.popup_revealer.reveal()

        self._manager.capture_client(
            client=client,
            overlay_cursor=False,
            callback=capture_callback,
            user_data=None,
        )

    def _add_pinned_apps(self):
        """Add user-configured pinned apps."""
        for item in self.config.get("pinned_apps", []):
            app = self.app_util.find_app(item)
            if app:
                self.add(
                    Button(
                        style_classes=["buttons-basic"],
                        image=Image(pixbuf=app.get_icon_pixbuf(self.icon_size)),
                        tooltip_text=app.display_name
                        if self.config.get("tooltip", True)
                        else None,
                        on_clicked=lambda *_, app=app: app.launch(),
                    )
                )

    def on_client_added(self, _, client: Glace.Client):
        client_image = Image()

        client_button = Button(
            style_classes=["buttons-basic", "buttons-transition"],
            image=client_image,
            on_button_press_event=lambda _, event: client.activate()
            if event.button == 1
            else None,
            on_enter_notify_event=lambda *_: self.update_preview_image(
                client, client_button
            ),
            on_leave_notify_event=lambda *_: self.popup_revealer.unreveal(),
        )
        self.client_buttons[client.get_id()] = client_button

        def on_app_id(*_):
            if client.get_app_id() in self.config.get(
                "ignored_apps", []
            ):  # TODO: this still needs work
                client_button.destroy()
                client_image.destroy()
                return
            client_image.set_from_pixbuf(
                self.icon_resolver.get_icon_pixbuf(client.get_app_id(), self.icon_size)
            )
            client_button.set_tooltip_text(
                client.get_title() if self.config.get("tooltip", True) else None
            )

        bulk_connect(
            client,
            {
                "notify::app-id": on_app_id,
                "notify::activated": lambda *_: client_button.add_style_class("active")
                if client.get_activated()
                else client_button.remove_style_class("active"),
                "close": lambda *_: self.remove(client_button),
            },
        )

        self.add(client_button)


class Dock(Window):
    """A dock for applications."""

    def __init__(self, config):
        self.config = config["modules"]["dock"]
        super().__init__(
            layer=self.config.get("layer", "top"),
            anchor=self.config.get("anchor", "bottom-center"),
        )
        self.revealer = Revealer(
            child=Box(children=[AppBar(self)], style="padding: 20px 50px 5px 50px;"),
            transition_duration=500,
            transition_type="slide-up",
        )
        self.children = EventBox(
            events=["enter-notify", "leave-notify"],
            child=Box(style="min-height: 1px", children=self.revealer),
            on_enter_notify_event=lambda *_: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *_: self.revealer.set_reveal_child(False),
        )
