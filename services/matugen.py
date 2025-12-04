import os

from fabric.core.service import Property, Service, Signal
from fabric.utils import exec_shell_command, exec_shell_command_async
from loguru import logger

import utils.functions as helpers
from utils.colors import Colors
from utils.config import theme_config


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

        # Ensure matugen config exists (copy from assets if needed)
        helpers.ensure_matugen_config()

        # Load configuration from theme.json
        matugen_config = theme_config.get("matugen", {})

        # Configuration with theme.json values as defaults
        self._enabled: bool = matugen_config.get("enabled", False)
        self._image_path: str = os.path.expanduser(matugen_config.get("image", ""))
        self._scheme: str = matugen_config.get("scheme", "tonal-spot")
        self._contrast: float = matugen_config.get("contrast", 0.0)
        self._mode: str = matugen_config.get("mode", "dark")
        self._config_path: str = os.path.expanduser(
            "~/.config/tsumiki/assets/matugen/config.toml"
        )

        logger.info(f"{Colors.INFO}Matugen service initialized")


    @Property(bool, "read-write", default_value=False)
    def enabled(self) -> bool:
        """Whether matugen is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @Property(str, "read-write")
    def image_path(self) -> str:
        """Path to the source image for color extraction."""
        return self._image_path

    @image_path.setter
    def image_path(self, value: str):
        self._image_path = os.path.expanduser(value)

    @Property(str, "read-write")
    def scheme(self) -> str:
        """Color scheme type.

        Available schemes:
        - scheme-content
        - scheme-expressive
        - scheme-fidelity
        - scheme-fruit-salad
        - scheme-monochrome
        - scheme-neutral
        - scheme-rainbow
        - scheme-tonal-spot (default)
        """
        return self._scheme

    @scheme.setter
    def scheme(self, value: str):
        valid_schemes = [
            "content",
            "expressive",
            "fidelity",
            "fruit-salad",
            "monochrome",
            "neutral",
            "rainbow",
            "tonal-spot",
        ]
        if value not in valid_schemes:
            logger.warning(
                f"{Colors.WARNING}Invalid scheme '{value}'. "
                f"Valid options: {', '.join(valid_schemes)}"
            )
            return
        self._scheme = f"scheme-{value}"

    @Property(float, "read-write")
    def contrast(self) -> float:
        """Contrast level (-1.0 to 1.0)."""
        return self._contrast

    @contrast.setter
    def contrast(self, value: float):
        if not -1.0 <= value <= 1.0:
            logger.warning(
                f"{Colors.WARNING}Contrast must be between -1.0 and 1.0. Got: {value}"
            )
            value = max(-1.0, min(1.0, value))
        self._contrast = value

    @Property(str, "read-write")
    def mode(self) -> str:
        """Color mode: 'dark' or 'light'."""
        return self._mode

    @mode.setter
    def mode(self, value: str):
        if value not in ["dark", "light"]:
            logger.warning(
                f"{Colors.WARNING}Invalid mode '{value}'. Must be 'dark' or 'light'."
            )
            return
        self._mode = value

    @Property(str, "read-write")
    def config_path(self) -> str:
        """Path to the matugen config.toml file."""
        return self._config_path

    @config_path.setter
    def config_path(self, value: str):
        self._config_path = os.path.expanduser(value)

    def generate(self, image_path: str | None = None) -> None:
        """Generate colors from an image asynchronously."""
        try:
            cmd = f"matugen image -q {image_path} -t {self._scheme}"
            cmd += f" --mode {self._mode} --contrast {self._contrast}"

            logger.info(f"{Colors.INFO}Running matugen: {cmd}")

            def on_complete(result):
                if result is not None:
                    logger.info(
                        f"{Colors.OKGREEN}Matugen colors generated successfully"
                    )
                    self.emit("colors_generated")
                else:
                    error_msg = "Matugen command returned no result"
                    logger.error(f"{Colors.ERROR}{error_msg}")
                    self.emit("generation_failed", error_msg)

            exec_shell_command_async(cmd, on_complete)

        except ValueError as e:
            error_msg = str(e)
            logger.error(f"{Colors.ERROR}Matugen error: {error_msg}")
            self.emit("generation_failed", error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(f"{Colors.ERROR}Matugen error: {error_msg}")
            self.emit("generation_failed", error_msg)

    def generate_sync(self, image_path: str | None = None) -> bool:
        """Generate colors from an image synchronously."""
        try:
            cmd = f"matugen image -q {image_path} -t {self._scheme}"
            cmd += f" --mode {self._mode} --contrast {self._contrast}"

            logger.info(f"{Colors.INFO}Running matugen: {cmd}")

            exec_shell_command(cmd)
            logger.info(f"{Colors.OKGREEN}Matugen colors generated successfully")
            self.emit("colors_generated")
            return True

        except ValueError as e:
            error_msg = str(e)
            logger.error(f"{Colors.ERROR}Matugen error: {error_msg}")
            self.emit("generation_failed", error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(f"{Colors.ERROR}Matugen error: {error_msg}")
            self.emit("generation_failed", error_msg)
            return False

    def generate_from_config(
        self,
        image_path: str,
        scheme: str | None = None,
        contrast: float | None = None,
        mode: str | None = None,
        quiet: bool | None = None,
    ) -> None:
        """Generate colors with all parameters specified at once.

        Args:
            image_path: Path to the source image.
            scheme: Color scheme type (optional, uses current if not provided).
            contrast: Contrast level -1.0 to 1.0 (optional).
            mode: 'dark' or 'light' (optional).
            quiet: Whether to run in quiet mode (optional).
        """
        # Temporarily update settings
        if scheme is not None:
            self.scheme = scheme
        if contrast is not None:
            self.contrast = contrast
        if mode is not None:
            self.mode = mode
        if quiet is not None:
            self.quiet = quiet

        self.generate(image_path)
