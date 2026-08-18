from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.i18n import _
from utils.widget_utils import nerd_font_icon


class OverviewButtonWidget(ButtonWidget):
    """A widget to show the overview of all workspaces and windows."""

    def __init__(self, **kwargs):
        super().__init__(name="overview_button", **kwargs)

        if self.config.get("tooltip", False) and self.tooltips_enabled:
            self.set_tooltip_text(_('widget.overview_button.tooltip'))

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon"),
            props={"style_classes": ["panel-font-icon"]},
        )

        if self.config.get("label", True):
            self.container_box.add(Label(label=_('widget.overview_button.label'),
                                          style_classes="panel-text"))

        # Lazy-init overview popup
        self._overview_popup = None
        self.connect("clicked", self.on_click)

    def on_click(self, *_):
        from modules.overview import OverViewOverlay
        from utils.config import tsumiki_config

        if self._overview_popup is None:
            self._overview_popup = OverViewOverlay(tsumiki_config)
        self._overview_popup.toggle_popup()
