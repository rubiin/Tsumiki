import os

from fabric.core.service import Service, Signal
from fabric.utils import exec_shell_command, exec_shell_command_async, logger

import utils.functions as helpers
from utils.config import theme_config

# Config path constant
_CONFIG_PATH = os.path.expanduser("~/.config/tsumiki/assets/matugen/config.toml")


class MatugenService(Service):
    """Service to generate Material You color schemes using Matugen."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @Signal
    def colors_generated(self) -> None:
        """Signal emitted when colors are successfully generated."""

    @Signal
    def generation_failed(self, error: str) -> None:
        """Signal emitted when color generation fails."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        helpers.check_executable_exists("matugen")
        self._config = theme_config.get("matugen", {})

    def _build_cmd(self, image_path: str) -> str:
        """Build matugen command from config."""
        cfg = self._config
        scheme = cfg.get("scheme", "scheme-tonal-spot")
        mode = cfg.get("mode", "dark")
        contrast = cfg.get("contrast", 0.0)

        return (
            f"matugen image -q {image_path} -t {scheme} "
            f"--mode {mode} --contrast {contrast} --config {_CONFIG_PATH}"
        )

    def generate(self, image_path: str | None = None) -> None:
        """Generate colors from an image asynchronously."""
        image_path = image_path or os.path.expanduser(
            self._config.get("wallpaper", "")
        )

        if not os.path.exists(image_path):
            self.emit("generation_failed", f"Image not found: {image_path}")
            return

        cmd = self._build_cmd(image_path)
        logger.info(f"[Matugen] Running: {cmd}")

        def on_complete(result):
            if result is not None:
                logger.info("[Matugen] Colors generated successfully")
                self.emit("colors_generated")
            else:
                self.emit("generation_failed", "Matugen returned no result")

        exec_shell_command_async(cmd, on_complete)

    def generate_sync(self, image_path: str | None = None) -> bool:
        """Generate colors from an image synchronously."""
        image_path = image_path or os.path.expanduser(
            self._config.get("wallpaper", "")
        )

        if not os.path.exists(image_path):
            self.emit("generation_failed", f"Image not found: {image_path}")
            return False

        cmd = self._build_cmd(image_path)
        logger.info(f"[Matugen] Running: {cmd}")

        try:
            exec_shell_command(cmd)
            logger.info("[Matugen] Colors generated successfully")
            self.emit("colors_generated")
            return True
        except Exception as e:
            self.emit("generation_failed", str(e))
            return False
