import subprocess

from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from loguru import logger

from shared.grid import Grid
from shared.widget_container import HoverButton


class ShortcutButton(HoverButton):
    """A button that executes a custom command when clicked."""

    def __init__(self, shortcut_config, **kwargs):
        super().__init__(name="shortcut-button", v_expand=True, **kwargs)

        self.command = shortcut_config["command"]

        box = Box(orientation="v", spacing=4, v_expand=True)

        if "icon" in shortcut_config:
            icon = Image(
                icon_name=shortcut_config["icon"],
                icon_size=shortcut_config["icon_size"],
                v_align="center",
                h_align="center",
            )
            box.add(icon)

        if "label" in shortcut_config:
            label = Label(
                label=shortcut_config["label"],
                v_align="center",
                h_align="center",
                style_classes="shortcut-label",
            )
            box.add(label)

        if "tooltip" in shortcut_config:
            self.set_tooltip_text(shortcut_config["tooltip"])

        self.add(box)
        self.connect("clicked", self.on_clicked)

    def on_clicked(self, *_):
        """Execute the command when clicked."""
        try:
            subprocess.Popen(["hyprctl", "dispatch", "exec", self.command])
        except Exception as e:
            logger.exception(f"Error executing shortcut command: {e}")


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

        for i, shortcut in enumerate(shortcuts_config):
            button = ShortcutButton(shortcut, h_expand=True)

            if num_cols == 1:
                # Single column - stack vertically
                grid.attach(button, 0, i, 1, 1)
            else:
                # 2x2 grid - fill vertically first
                row = i % 2
                col = i // 2
                grid.attach(button, col, row, 1, 1)

        self.add(grid)
