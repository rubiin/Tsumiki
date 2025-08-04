import os

import pyjson5 as json
import pytomlpp as toml
from fabric.utils import get_relative_path
from loguru import logger

from .constants import DEFAULT_CONFIG
from .functions import (
    deep_merge,
    exclude_keys,
    flatten_dict,
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

        self.json_config_file = get_relative_path(
            "../config.json"
        )  # TODO: always read from .config/tsumuki/config.json
        self.toml_config_file = get_relative_path("../config.toml")
        self.theme_config_file = get_relative_path("../theme.json")

        self.config = self.default_config()

        self.theme_config = self.read_json(self.theme_config_file)

        self.set_css_settings()
        self._initialized = True

    def read_json(self, file) -> dict:
        logger.info(f"[Config] Reading json config from {file}")
        try:
            with open(file, "r") as file:
                # Load JSON data into a Python dictionary
                data = json.load(file)
        except Exception as e:
            logger.error(f"[Config] Failed to read json config from {file}: {e}")
            return {}
        return data

    def read_config_toml(self) -> dict:
        logger.info(f"[Config] Reading toml config from {self.toml_config_file}")
        try:
            with open(self.toml_config_file, "r") as file:
                # Load JSON data into a Python dictionary
                data = toml.load(file)
        except Exception as e:
            logger.error(
                f"[Config] Failed to read toml config from {self.toml_config_file}: {e}"
            )
            return {}
        return data

    def default_config(self) -> BarConfig:
        # Read the configuration from the JSON file
        check_toml = os.path.exists(self.toml_config_file)
        check_json = os.path.exists(self.json_config_file)

        if not check_json and not check_toml:
            raise FileNotFoundError("Please provide either a json or toml config.")

        parsed_data = (
            self.read_json(file=self.json_config_file)
            if check_json
            else self.read_config_toml()
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

        with open(get_relative_path("../styles/_settings.scss"), "w") as f:
            f.write(settings)


configuration = TsumikiConfig()
theme_config = configuration.theme_config
widget_config = configuration.config
