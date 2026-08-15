from fabric.utils import Gtk
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services import audio_service
from shared.buttons import HoverButton
from shared.list import ListBox
from shared.submenu import QuickSubMenu
from utils.icons import get_text_icon, symbolic_icons
from utils.widget_utils import nerd_font_icon
from widgets.quick_settings.sliders.audio import AudioSlider


class AudioSubMenu(QuickSubMenu):
    """A submenu to display application-specific audio controls."""

    def __init__(self, **kwargs):
        self.client = audio_service

        # Refresh button to re-scan the application list on demand.
        self.refresh_button = HoverButton(
            style_classes="submenu-button",
            name="refresh-button",
            child=nerd_font_icon(
                icon=get_text_icon("ui.refresh"),
                props={"style_classes": ["panel-font-icon"]},
            ),
            on_clicked=lambda *_: self.update_apps(),
        )

        self.app_list = ListBox(visible=True, name="app-list")

        self.child = ScrolledWindow(
            min_content_size=(-1, 120),
            max_content_size=(-1, 260),
            propagate_width=True,
            propagate_height=True,
            child=self.app_list,
        )

        super().__init__(
            title="Application Audio",
            title_icon=get_text_icon("volume.high"),
            scan_button=self.refresh_button,
            child=self.child,
            **kwargs,
        )

        self.update_apps()
        self._stream_added_handler = self.client.connect(
            "stream-added", self.update_apps
        )
        self._stream_removed_handler = self.client.connect(
            "stream-removed", self.update_apps
        )
        self.connect("destroy", self._on_destroy)

    def _on_destroy(self, *_):
        from utils.functions import safe_disconnect

        safe_disconnect(self.client, self._stream_added_handler)
        safe_disconnect(self.client, self._stream_removed_handler)
        self._stream_added_handler = None
        self._stream_removed_handler = None

    def update_apps(self, *_):
        """Rebuild the list of applications with volume controls."""
        self.app_list.remove_all()
        for app in self.client.applications:
            self.app_list.add(self._make_app_row(app))

    def _make_app_row(self, app):
        full_name = (app.name or app.description or "Unknown").strip()
        name = full_name
        if len(name) > 30:
            name = f"{name[:30]}…"

        icon_name = app.icon_name or symbolic_icons["audio"]["volume"]["high"]

        header = Box(
            orientation="h",
            spacing=10,
            h_expand=True,
            children=(
                Image(
                    icon_name=icon_name,
                    icon_size=18,
                ),
                Label(
                    label=name,
                    style_classes=["submenu-item-label", "audio-source-name"],
                    h_align="start",
                    h_expand=True,
                    ellipsization="end",
                    tooltip_text=full_name,
                ),
            ),
        )

        row = Gtk.ListBoxRow(visible=True)
        row.add(
            Box(
                orientation="v",
                spacing=4,
                name="audio-source-item",
                children=(header, AudioSlider(app)),
            )
        )
        return row
