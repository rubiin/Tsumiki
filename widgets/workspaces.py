from fabric.core.widgets import WorkspaceButton
from fabric.hyprland.widgets import HyprlandWorkspaces as Workspaces
from fabric.utils import bulk_connect

from shared.widget_container import BoxWidget
from utils.functions import unique_list


class WorkSpacesWidget(BoxWidget):
    """A widget to display the current workspaces."""

    def __init__(self, **kwargs):
        super().__init__(name="workspaces", **kwargs)

        config = self.config
        self.ignored_ws = {int(x) for x in unique_list(config.get("ignored", []))}
        self.icon_map = config.get("icon_map", {})
        self.default_format = config.get("default_label_format", "{id}")
        self.workspace_count = config.get("count", 8)
        self.hide_unoccupied = config.get("hide_unoccupied", False)
        self.show_numbered = config.get("show_numbered", True)

        # Create a HyperlandWorkspace widget to manage workspace buttons
        self.workspace = Workspaces(
            name="workspaces",
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
        self.children = self.workspace

    def _create_workspace_label(self, ws_id: int) -> str:
        return self.icon_map.get(str(ws_id), self.default_format.format(id=ws_id))

    def _update_empty_state(self, button: WorkspaceButton, *_):
        if button.empty:
            button.add_style_class("unoccupied")
            button.remove_style_class("occupied")
        else:
            button.remove_style_class("unoccupied")
            button.add_style_class("occupied")

    def _setup_button(self, ws_id: int) -> WorkspaceButton:
        button = WorkspaceButton(
            id=ws_id,
            label=self._create_workspace_label(ws_id) if self.show_numbered else None,
            visible=ws_id not in self.ignored_ws,
        )

        # Only add empty state styling when showing all workspaces
        if not self.hide_unoccupied:
            # Connect to state changes
            bulk_connect(
                button,
                {
                    "notify::empty": lambda *args: self._update_empty_state(
                        button, *args
                    ),
                    "notify::active": lambda *args: self._update_empty_state(
                        button, *args
                    ),
                },
            )
            self._update_empty_state(button)
        return button
