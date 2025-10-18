from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import logger
from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label

from shared.buttons import HoverButton
from utils.widget_utils import nerd_font_icon


class ShortcutButton(HoverButton):
    """A button that executes a custom command when clicked."""

    def __init__(self, shortcut_config: dict, **kwargs):
        super().__init__(name="shortcut-button", v_expand=True, **kwargs)

        self.command = shortcut_config.get("command", "")

        box = Box(orientation="v", spacing=4, v_expand=True)

        self._hyprland_connection = get_hyprland_connection()

        if "icon" in shortcut_config:
            icon = nerd_font_icon(
                icon=shortcut_config.get("icon", "󰒲"),
                props={
                    "style_classes": ["panel-font-icon", "shortcut-icon"],
                    "style": f"font-size: {shortcut_config.get('icon_size', 16)}px;",
                },
            )

            box.add(icon)

        if "label" in shortcut_config:
            label = Label(
                label=shortcut_config.get("label", ""),
                v_align="center",
                h_align="center",
                style_classes=["shortcut-label"],
            )
            box.add(label)

        if "tooltip" in shortcut_config:
            self.set_tooltip_text(shortcut_config.get("tooltip", ""))

        self.add(box)
        self.connect("clicked", self.on_click)

    def on_click(self, *_):
        """Execute the command when clicked."""
        try:
            self._hyprland_connection.send_command_async(
                f"dispatch exec {self.command}", lambda _: None
            )
        except Exception as e:
            logger.exception(f"Error executing shortcut command: {e}")


# TODO: type


class ShortcutsContainer(Box):
    """A container for the shortcuts grid with styling support."""

    def __init__(self, shortcuts_config, **kwargs):
        super().__init__(
            orientation="v", spacing=4, h_expand=True, v_expand=True, **kwargs
        )

        if not shortcuts_config:
            return

        num_shortcuts = len(shortcuts_config)

        # Create grid for shortcuts
        grid = Grid(
            row_spacing=10,
            column_spacing=10,
            h_expand=True,
            v_expand=True,
        )

        # Use single column for 1-2 shortcuts, 2x2 grid for 3-4
        num_cols = 2 if num_shortcuts > 2 else 1

        grid.attach_flow(
            children=[
                ShortcutButton(shortcut, h_expand=True) for shortcut in shortcuts_config
            ],
            columns=num_cols,
        )

        self.add(grid)
