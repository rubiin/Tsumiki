import json
import os

from fabric.utils import get_relative_path
from loguru import logger

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


class TsumikiConfig:
    "A class to read the configuration file and return the default configuration"

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

        self.config = self.default_config()

        self.theme_config = read_json_file(file_path=self.theme_config_file)

        self.set_css_settings()
        self._initialized = True

    def default_config(self) -> BarConfig:
        # Read the configuration from the JSON file
        check_toml = os.path.exists(self.toml_config_file)
        check_json = os.path.exists(self.json_config_file)

        if not check_json and not check_toml:
            raise FileNotFoundError("Please provide either a json or toml config.")

        parsed_data = (
            read_json_file(file_path=self.json_config_file)
            if check_json
            else read_toml_file(file_path=self.toml_config_file)
        )

        validate_widgets(parsed_data, DEFAULT_CONFIG)

        for key in exclude_keys(DEFAULT_CONFIG, ["$schema"]):
            if key == "widget_groups":
                # For lists, use the user's value or default if not present
                parsed_data[key] = parsed_data.get(key, DEFAULT_CONFIG[key])
            else:
                # For dictionaries, merge with defaults
                parsed_data[key] = deep_merge(
                    parsed_data.get(key, {}), DEFAULT_CONFIG[key]
                )

        return parsed_data

    @run_in_thread
    def set_css_settings(self):
        logger.info("[CONFIG] Applying css settings...")

        css_styles = flatten_dict(exclude_keys(self.theme_config, ["name"]))

        settings = ""

        for setting in css_styles:
            # Convert python boolean to scss boolean
            value = (
                json.dumps(css_styles[setting])
                if isinstance(css_styles[setting], bool)
                else css_styles[setting]
            )
            settings += f"${setting}: {value};\n"

        with open(f"{self.root_dir}/styles/_settings.scss", "w") as f:
            f.write(settings)


configuration = TsumikiConfig()
theme_config = configuration.theme_config
widget_config = configuration.config
