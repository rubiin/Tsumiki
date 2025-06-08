from fabric.hyprland.widgets import WorkspaceButton, Workspaces

from shared.widget_container import BoxWidget
from utils.functions import unique_list


class WorkSpacesWidget(BoxWidget):
    """A widget to display the current workspaces."""

    def __init__(self, **kwargs):
        super().__init__(name="workspaces", **kwargs)

        config = self.config
        ignored_ws = {int(x) for x in unique_list(config.get("ignored", []))}
        icon_map = config.get("icon_map", {})
        default_format = config.get("default_label_format", "{id}")
        workspace_count = config.get("count", 8)
        hide_unoccupied = config.get("hide_unoccupied", False)

        def create_workspace_label(ws_id: int) -> str:
            return icon_map.get(str(ws_id), default_format.format(id=ws_id))

        def setup_button(ws_id: int) -> WorkspaceButton:
            button = WorkspaceButton(
                id=ws_id,
                label=create_workspace_label(ws_id),
                visible=ws_id not in ignored_ws,
            )

            def update_empty_state(*_):
                button.add_style_class(
                    "unoccupied"
                ) if button.empty else button.remove_style_class("unoccupied")

            button.connect("notify::empty", update_empty_state)
            update_empty_state()
            return button

        # Create a HyperlandWorkspace widget to manage workspace buttons
        self.workspace = Workspaces(
            name="workspaces",
            spacing=4,
            # Create buttons for each workspace if occupied
            buttons=None
            if hide_unoccupied
            else [
                setup_button(ws_id)
                for ws_id in range(1, workspace_count + 1)
                if ws_id not in ignored_ws
            ],
            # Factory function to create buttons for each workspace
            buttons_factory=setup_button,
            invert_scroll=config.get("reverse_scroll", False),
            empty_scroll=config.get("empty_scroll", False),
        )

        # Add the HyperlandWorkspace widget as a child
        self.children = self.workspace
