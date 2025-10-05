from fabric.widgets.box import Box
from fabric.widgets.grid import Grid
from fabric.widgets.label import Label

from utils.keybinds import KeybindLoader


class CheatSheet(Box):
    """
    A cheatsheet widget to display keybindings grouped into categories.
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="cheatsheet",
            orientation="vertical",
            spacing=30,
            **kwargs,
        )

        # Key → Icon map
        self.key_icon_map = {
            "SUPER": "",
            "SHIFT": "󰍃",
            "CTRL": "󰌋",
            "ALT": "󰍂",
            "ENTER": "󰌑",
            "TAB": "󰌒",
            "SPACE": "󱁐",
        }

        # Load keybinds
        self._keybinds = KeybindLoader()
        self._keybinds.load_keybinds()

        # Grid (not homogeneous so columns can have different widths)
        self._grid = Grid(
            homogeneous=False,
            style_classes=["cheatsheet-grid"],
            row_spacing=10,
            column_spacing=40,
        )

        self.children = (
            Label("Cheat Sheet", style_classes=["cheatsheet-title"]),
            self._grid,
        )

        self._populate_grid()

    def _populate_grid(self):
        keybinds = self._keybinds.keybinds

        # Groups
        keybind_groups = {
            "Launcher": [],
            "Workspaces": [],
            "Uncategorized": [],
        }

        # Categorize
        for keybind in keybinds:
            description = keybind.get("description", "").strip().lower()

            match description:
                case _ if "launcher" in description:
                    keybind_groups["Launcher"].append(keybind)
                case _ if "workspace" in description:
                    keybind_groups["Workspaces"].append(keybind)
                case "" | "no description":
                    keybind_groups["Uncategorized"].append(keybind)
                case _:
                    keybind_groups["Uncategorized"].append(keybind)

        # Each group: 2 columns (combo + description)
        for group_index, (group_name, group_keybinds) in enumerate(
            keybind_groups.items()
        ):
            base_col = group_index * 2

            # Group header (spanning both cols)
            self._grid.attach(
                Label(group_name, style_classes=["cheatsheet-group"]),
                base_col,
                0,
                2,
                1,
            )

            # Fill group rows
            for row, keybind in enumerate(group_keybinds, start=1):
                combo = keybind["combo"]
                description = keybind["description"]

                # Replace keys with icons
                for key, icon in self.key_icon_map.items():
                    combo = combo.replace(key, icon)

                combo_label = Label(combo, style_classes=["cheatsheet-key"])
                desc_label = Label(
                    description, style_classes=["cheatsheet-description"]
                )

                # Attach: combo in first col, description in second col
                self._grid.attach(combo_label, base_col, row, 1, 1)
                self._grid.attach(desc_label, base_col + 1, row, 1, 1)
