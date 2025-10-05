from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon

MIC_ON_ICON = "󰍬"
MIC_OFF_ICON = "󰍭"


class MicrophoneIndicatorWidget(ButtonWidget):
    """A widget to display the current microphone status."""

    def __init__(self, **kwargs):
        super().__init__(name="microphone", **kwargs)

        self.icon = nerd_font_icon(
            icon=MIC_OFF_ICON,
            props={"style_classes": ["panel-font-icon"]},
        )

        self.container_box.add(self.icon)

        if self.config.get("label", True):
            self.mic_label = Label(
                label="",
                style_classes=["panel-text"],
            )
            self.container_box.add(self.mic_label)

        self.audio_service.connect("microphone_changed", self._update_status)
        self._update_status()

    def _update_status(self, *_):
        current_microphone = self.audio_service.microphone

        if current_microphone:
            is_muted = current_microphone.muted
            self.icon.set_label(MIC_OFF_ICON if is_muted else MIC_ON_ICON)

            # Update the label  if enabled
            if self.config.get("label", True):
                self.mic_label.set_label("Off" if is_muted else "On")

            if self.config.get("tooltip", False):
                self.set_tooltip_text(
                    "Microphone is muted" if is_muted else "Microphone is on"
                )

            self.icon.set_visible(True)
        else:
            self.icon.set_visible(False)

        return True
