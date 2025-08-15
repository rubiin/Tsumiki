import gi
from fabric.utils import bulk_connect
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from gi.repository import Glace

from shared.widget_container import BoxWidget
from utils.icon_resolver import IconResolver

gi.require_versions({"Gtk": "3.0", "GdkPixbuf": "2.0", "Glace": "0.1"})


class TaskBarWidget(BoxWidget):
    """A widget to display the taskbar items."""

    def __init__(self, **kwargs):
        super().__init__(
            name="taskbar",
            **kwargs,
        )
        self._manager = Glace.Manager()

        self.icon_resolver = IconResolver()
        self._manager = Glace.Manager()
        self._manager.connect("client-added", self._on_client_added)

    def _on_client_added(self, _, client: Glace.Client):
        client_image = Image()

        def on_app_id(*_):
            client_image.set_from_pixbuf(
                self.icon_resolver.get_icon_pixbuf(
                    client.get_app_id(), self.config.get("icon_size", 22)
                )
            )
            client_button.set_tooltip_text(
                client.get_title() if self.config.get("tooltip", True) else None
            )

        client_button = Button(
            style_classes=["buttons-basic", "buttons-transition"],
            image=client_image,
            on_button_press_event=lambda *_: client.activate(),
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
