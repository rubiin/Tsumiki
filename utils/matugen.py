from fabric.utils import exec_shell_command_async, get_relative_path


class Matugen:
    """
    Matugen is a utility for generating color palettes.
    It can be used to create color schemes for various applications.
    """

    def normalize_contrast(self, contrast: float) -> float:
        return max(-1, min(1, contrast))

    def generate_palette(
        self, wallpaper: str, contrast: float = 0.5, scheme="tonal-spot", mode="dark"
    ) -> list:
        """
        Generate a color palette based on the provided wallpaper and contrast.
        """

        try:
            wallpaper = get_relative_path(wallpaper)
            contrast = self.normalize_contrast(contrast)

            base_command = f'matugen image -q "{wallpaper}" -t scheme-{scheme} --contrast {contrast}'

            # Placeholder for actual palette generation logic
            return exec_shell_command_async(base_command, lambda x: x.get(mode, []))
        except Exception as e:
            print(f"Error generating palette: {e}")
            return []
