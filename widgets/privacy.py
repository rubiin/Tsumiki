from typing import ClassVar

from fabric.hyprland.widgets import HyprlandEvent, get_hyprland_connection
from fabric.utils import GObject, bulk_connect
from fabric.widgets.box import Box

from services import audio_service
from shared.widget_container import ButtonWidget
from utils.icons import get_text_icon
from utils.widget_utils import nerd_font_icon


class PrivacyWidget(ButtonWidget):
    """Privacy indicator widget showing camera, microphone, and screen recording status.

    Inspired by waybar's privacy module, displays active privacy-sensitive services.
    """

    __gsignals__: ClassVar = {
        "privacy-changed": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, **kwargs):
        super().__init__(name="privacy", **kwargs)

        self.audio_service = audio_service

        # State tracking
        self.mic_muted = None
        self.screen_active = False  # Track active screencast sessions
        self.camera_active = False  # Placeholder for future implementation

        # Create icon container
        self.privacy_icons_box = Box(
            orientation="h",
            spacing=4,
            style_classes=["privacy-icons"],
        )

        self.container_box.add(self.privacy_icons_box)

        self._hyprland_connection = get_hyprland_connection()

        # Connect signals
        bulk_connect(
            self.audio_service,
            {
                "notify::microphone": self._on_microphone_changed,
                "microphone_changed": self._on_microphone_changed,
            },
        )

        # Start listening to hyprland events
        self._hyprland_connection.connect(
            "event::screencastv2", self._on_hyprland_event
        )

        # Initial state update
        self._update_display()

    def _on_microphone_changed(self, *_):
        """Handle microphone state change."""
        self._update_display()

    def _on_hyprland_event(self, _, reply: HyprlandEvent):
        if reply.data[0] == "0":
            self.screen_active = False
        else:
            self.screen_active = True
        self._update_display()

    def _update_display(self):
        """Update icon display based on current state."""
        # Clear existing icons
        for child in self.privacy_icons_box.get_children():
            child.destroy()

        icons = []
        microphone = self.audio_service.microphone

        if microphone:
            self.mic_muted = microphone.muted
            if not self.mic_muted:
                icons.append(get_text_icon("microphone.high"))

        if self.screen_active:
            icons.append(get_text_icon("recorder"))

        if self.camera_active:
            icons.append(get_text_icon("ui.camera"))

        for icon_text in icons:
            self._add_privacy_icon(icon_text)

        visible = bool(icons) or not self.config.get("hide_when_inactive", True)
        self.set_visible(visible)

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            tooltip = self._get_tooltip() if icons else "No active privacy concerns"
            self.set_tooltip_text(tooltip)

        self.emit("privacy-changed")

    def _add_privacy_icon(self, icon_text: str):
        """Add an icon to the privacy box."""
        icon = nerd_font_icon(
            icon=icon_text,
            props={
                "style_classes": ["privacy-icon"],
            },
        )
        self.privacy_icons_box.add(icon)

    def _get_tooltip(self) -> str:
        """Generate tooltip text based on active items."""
        items = []
        if self.mic_muted is not None and not self.mic_muted:
            items.append("Microphone active")
        if self.screen_active:
            items.append("Screen recording")
        if self.camera_active:
            items.append("Camera active")
        return " | ".join(items) if items else "Privacy monitoring"
