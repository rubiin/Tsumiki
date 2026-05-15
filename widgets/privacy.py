from typing import ClassVar

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import GObject, bulk_connect

from services import audio_service
from shared.widget_container import ButtonWidget
from utils.icons import text_nerd_icons
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
        self.screencast_clients = {}  # Track active screencast sessions
        self.camera_active = False  # Placeholder for future implementation

        # Create icon container
        self.privacy_icons_box = None
        self._setup_icons()
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

    def _setup_icons(self):
        """Setup icon display box."""
        from fabric.widgets.box import Box

        self.privacy_icons_box = Box(
            orientation="h",
            spacing=4,
            style_classes=["privacy-icons"],
        )

        self.container_box.children = (self.privacy_icons_box,)

    def _on_microphone_changed(self, *_):
        """Handle microphone state change."""
        self._update_display()

    def _on_hyprland_event(self, *_):
        print("Received Hyprland event, updating privacy display")
        print(*_)

    def _update_display(self):
        """Update icon display based on current state."""
        # Clear existing icons
        for child in self.privacy_icons_box.get_children():
            child.destroy()

        active_count = 0

        # Check microphone
        microphone = self.audio_service.microphone
        if microphone:
            is_muted = microphone.muted
            if not is_muted:
                mic_icon = text_nerd_icons.get("microphone", "🎤")
                self._add_privacy_icon(mic_icon, "Microphone active")
                active_count += 1
            self.mic_muted = is_muted

        # Check screen recording
        if self.screencast_clients:
            screen_icon = text_nerd_icons.get("screenrecorder", "🔴")
            client_names = ", ".join(self.screencast_clients.keys())
            tooltip = f"Screen recording: {client_names}"
            self._add_privacy_icon(screen_icon, tooltip)
            active_count += 1

        # Check camera (placeholder)
        if self.camera_active:
            self._add_privacy_icon("📷", "Camera active")
            active_count += 1

        # Update visibility and tooltip
        if active_count > 0:
            self.set_visible(True)
            if self.config.get("tooltip", True) and self.general_config.get(
                "tooltips", True
            ):
                self.set_tooltip_text(self._get_tooltip())
        else:
            if self.config.get("hide_when_inactive", True):
                self.set_visible(False)
            else:
                if self.config.get("tooltip", True) and self.general_config.get(
                    "tooltips", True
                ):
                    self.set_tooltip_text("No active privacy concerns")

        self.emit("privacy-changed")

    def _add_privacy_icon(self, icon_text: str, tooltip: str = ""):
        """Add an icon to the privacy box."""
        icon = nerd_font_icon(
            icon=icon_text,
            props={
                "style_classes": ["privacy-icon"],
                "tooltip_text": tooltip if self.config.get("tooltip", True) else None,
            },
        )
        self.privacy_icons_box.add(icon)
        icon.show_all()

    def _get_tooltip(self) -> str:
        """Generate tooltip text based on active items."""
        items = []
        if self.mic_muted is not None and not self.mic_muted:
            items.append("Microphone active")
        if self.screencast_clients:
            items.append("Screen recording")
        if self.camera_active:
            items.append("Camera active")
        return " | ".join(items) if items else "Privacy monitoring"
