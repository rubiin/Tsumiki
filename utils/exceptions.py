from utils import Colors


class ExecutableNotFoundError(ImportError):
    """Raised when an executable is not found."""

    def __init__(self, executable_name: str):
        super().__init__(
            f"{Colors.ERROR}Executable {Colors.UNDERLINE}{executable_name}{Colors.RESET} not found. Please install it using your package manager."  # noqa: E501
        )
