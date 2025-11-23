import json

from fabric.utils import exec_shell_command, get_relative_path

from utils.functions import run_in_thread


class Matugen:
    """
    Matugen is a utility for generating color palettes.
    It can be used to create color schemes for various applications.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def normalize_contrast(self, contrast: float) -> float:
        return max(-1, min(1, contrast))

    @run_in_thread
    def generate_css(self, value):
        value = json.loads(value)
        print(value["colors"])

    @run_in_thread
    def generate_palette(
        self, wallpaper: str, contrast: float = 0.5, scheme="tonal-spot", mode="dark"
    ) -> list:
        """
        Generate a color palette based on the provided wallpaper and contrast.
        """

        try:
            wallpaper = get_relative_path(wallpaper)
            contrast = self.normalize_contrast(contrast)

            base_command = (
                f'matugen image -q "{wallpaper}" '
                f"-t scheme-{scheme} "
                f"--contrast {contrast} "
                f"--mode {mode} "
                f"--dry-run "
                f"--json hex"
            )

            # Placeholder for actual palette generation logic
            val = exec_shell_command(base_command)
            self.generate_css(value=val)
        except Exception as e:
            print(f"Error generating palette: {e}")
            return []
