import json
import os

from fabric.utils import get_relative_path, logger

from .constants import DEFAULT_CONFIG
from .functions import (
    deep_merge,
    exclude_keys,
    flatten_dict,
    read_json_file,
    read_toml_file,
    run_in_thread,
    validate_widgets,
)
from .widget_settings import BarConfig

# Pre-computed excluded keys for config merging
_EXCLUDED_SCHEMA_KEYS = frozenset(["$schema"])
_LIST_CONFIG_KEYS = frozenset(["widget_groups", "collapsible_groups"])


class TsumikiConfig:
    "A class to read the configuration file and return the default configuration"

    __slots__ = (
        "_initialized",
        "config",
        "json_config_file",
        "root_dir",
        "theme_config",
        "theme_config_file",
        "toml_config_file",
    )

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        # TODO: always read from .config/tsumuki/config.json
        self.root_dir = get_relative_path("..")

        self.json_config_file = f"{self.root_dir}/config.json"
        self.toml_config_file = f"{self.root_dir}/config.toml"
        self.theme_config_file = f"{self.root_dir}/theme.json"

        self.config = self._load_config()
        self.theme_config = read_json_file(file_path=self.theme_config_file)

        self._write_css_settings()
        self._initialized = True

    def _load_config(self) -> BarConfig:
        """Load and merge configuration from JSON or TOML file."""
        check_json = os.path.exists(self.json_config_file)
        check_toml = os.path.exists(self.toml_config_file)

        if not check_json and not check_toml:
            raise FileNotFoundError("Please provide either a json or toml config.")

        # Prefer JSON over TOML
        parsed_data = (
            read_json_file(file_path=self.json_config_file)
            if check_json
            else read_toml_file(file_path=self.toml_config_file)
        )

        validate_widgets(parsed_data, DEFAULT_CONFIG)

        # Merge configuration with defaults
        for key, default_value in DEFAULT_CONFIG.items():
            if key in _EXCLUDED_SCHEMA_KEYS:
                continue

            if key in _LIST_CONFIG_KEYS:
                # For lists, use the user's value or default if not present
                parsed_data[key] = parsed_data.get(key, default_value)
            else:
                # For dictionaries, merge with defaults
                parsed_data[key] = deep_merge(parsed_data.get(key, {}), default_value)

        return parsed_data

    @run_in_thread
    def _write_css_settings(self):
        """Generate SCSS settings file from theme config."""
        logger.info("[CONFIG] Applying css settings...")

        css_styles = flatten_dict(exclude_keys(self.theme_config, ["name"]))

        # Use list comprehension and join for faster string building
        lines = [
            f"${setting}: {json.dumps(value) if isinstance(value, bool) else value};"
            for setting, value in css_styles.items()
        ]

        with open(f"{self.root_dir}/styles/_settings.scss", "w") as f:
            f.write("\n".join(lines))
            f.write("\n")


configuration = TsumikiConfig()
theme_config = configuration.theme_config
widget_config = configuration.config
