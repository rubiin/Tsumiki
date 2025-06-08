from fabric.hyprland.widgets import WorkspaceButton as WsButton
from fabric.hyprland.widgets import Workspaces

from shared.widget_container import BoxWidget
from utils.functions import unique_list
from utils.widget_utils import setup_cursor_hover


class WorkspaceButton(WsButton):
    """A button to represent a workspace."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the hover hand
        setup_cursor_hover(self)


class WorkSpacesWidget(BoxWidget):
    """A widget to display the current workspaces."""

    def __init__(self, **kwargs):
        super().__init__(name="workspaces", **kwargs)

        # Convert ignored workspace IDs to integers
        ignored_ws = [int(x) for x in unique_list(self.config["ignored"])]
        default_format = self.config.get("default_label_format", "{id}")

        def create_workspace_label(ws_id: int) -> str:
            # First check icon_map for custom label/icon
            str_id = str(ws_id)
            if str_id in self.config.get("icon_map", {}):
                return self.config["icon_map"][str_id]

            # Otherwise use default format
            return default_format.format(id=ws_id)

        def setup_button_empty_state(button):
            """Set up empty state tracking for workspace button"""

            def update_empty_state(*_):
                if button.get_empty():
                    button.add_style_class("unoccupied")
                else:
                    button.remove_style_class("unoccupied")

            button.connect("notify::empty", update_empty_state)

            # Set initial state
            update_empty_state()
            return button

        # Create a HyperlandWorkspace widget to manage workspace buttons
        self.workspace = Workspaces(
            name="workspaces",
            spacing=4,
            # Create buttons for each workspace if occupied
            buttons=None  # sending None to buttons will create occupied workspaces only
            if self.config["hide_unoccupied"]
            else [
                setup_button_empty_state(
                    WorkspaceButton(id=i, label=create_workspace_label(i))
                )
                for i in range(1, self.config["count"] + 1)
                if i not in ignored_ws
            ],
            # Factory function to create buttons for each workspace
            buttons_factory=lambda ws_id: setup_button_empty_state(
                WorkspaceButton(
                    id=ws_id,
                    label=create_workspace_label(ws_id),
                    visible=ws_id not in ignored_ws,
                )
            ),
            invert_scroll=self.config["reverse_scroll"],
            empty_scroll=self.config["empty_scroll"],
        )

        # Add the HyperlandWorkspace widget as a child
        self.children = self.workspace
