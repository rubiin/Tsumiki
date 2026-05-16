from fabric.core.widgets import WorkspaceButton
from fabric.hyprland.widgets import HyprlandWorkspaces

from shared.widget_container import BoxWidget
from utils.functions import get_distro_icon, unique_list
from utils.widget_utils import nerd_font_icon


class WorkSpacesWidget(BoxWidget):
    """A widget to display the current workspaces."""

    def __init__(self, **kwargs):
        super().__init__(name="workspaces", spacing=1, **kwargs)

        workspace = HyprlandWorkspaces

        self.ignored_ws = {int(x) for x in unique_list(self.config.get("ignored", []))}
        self.icon_map = self.config.get("icon_map", {})
        self.default_format = self.config.get("default_label_format", "{id}")
        self.workspace_count = self.config.get("count", 8)
        self.hide_unoccupied = self.config.get("hide_unoccupied", False)
        self.show_numbered = self.config.get("show_numbered", True)

        self.icon = nerd_font_icon(
            icon=get_distro_icon(),
            props={"style_classes": ["panel-font-icon"]},
        )

        # Create a HyperlandWorkspace widget to manage workspace buttons
        self.workspace = workspace(
            name="workspaces_widget",
            spacing=4,
            # Create buttons for each workspace if occupied
            buttons=None
            if self.hide_unoccupied
            else [
                self._setup_button(ws_id)
                for ws_id in range(1, self.workspace_count + 1)
                if ws_id not in self.ignored_ws
            ],
            # Factory function to create buttons for each workspace
            buttons_factory=self._setup_button,
            invert_scroll=self.config.get("reverse_scroll", False),
            empty_scroll=self.config.get("empty_scroll", False),
        )

        # Add the HyperlandWorkspace widget as a child
        self.children = (self.icon, self.workspace)

    def _create_workspace_label(self, ws_id: int) -> str:
        return self.icon_map.get(str(ws_id), self.default_format.format(id=ws_id))

    def _setup_button(self, ws_id: int) -> WorkspaceButton:
        button = WorkspaceButton(
            id=ws_id,
            label=self._create_workspace_label(ws_id) if self.show_numbered else None,
            visible=ws_id not in self.ignored_ws,
        )

        return button
