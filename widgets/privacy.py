from fabric.utils import GLib, invoke_repeater

from services import privacy_service
from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class PrivacyIndicatorWidget(ButtonWidget):
    """Privacy indicator widget showing camera, microphone, and screen recording status.

    Inspired by waybar's privacy module, displays active privacy-sensitive services.
    """

    def __init__(self, **kwargs):
        super().__init__(name="privacy_indicator", **kwargs)

        self.service = privacy_service
        self._privacy_repeater_id = None

        GLib.timeout_add(3500, self._start_privacy_repeater)

    def _start_privacy_repeater(self):
        self.update_privacy_status()
        self._privacy_repeater_id = invoke_repeater(1000, self.update_privacy_status)
        return False

    def update_privacy_status(self):
        """Update the privacy status by querying the service and updating icons."""
        stat = self.service.detect_privacy_usage()

        # Update microphone status
        mic = stat.get("microphone", [])
        camera = stat.get("camera", [])
        screen = stat.get("screen", [])

        if (
            self.config.get("hide_when_inactive", False)
            and len(mic) == 0
            and len(camera) == 0
            and len(screen) == 0
        ):
            self.hide()
            return True

        # Always reset the icon row before re-rendering.
        for child in self.container_box.get_children():
            self.container_box.remove(child)
        self.show()

        if len(mic) > 0:
            self._add_privacy_icon("")  # Microphone icon
        if len(camera) > 0:
            self._add_privacy_icon("")  # Camera icon
        if len(screen) > 0:
            self._add_privacy_icon("")  # Screen recording icon

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            tooltip_text = []
            if len(mic) > 0:
                tooltip_text.append("Microphone active")
            if len(camera) > 0:
                tooltip_text.append("Camera active")
            if len(screen) > 0:
                tooltip_text.append("Screen recording active")
            self.set_tooltip_text("\n".join(tooltip_text))
        else:
            self.set_tooltip_text("")

        return True

    def _add_privacy_icon(self, icon_text: str):
        """Add an icon to the privacy box."""
        icon = nerd_font_icon(
            icon=icon_text,
            props={
                "style_classes": ["privacy-icon"],
            },
        )
        self.container_box.add(icon)
