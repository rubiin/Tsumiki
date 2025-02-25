import json
import os

from fabric.utils import get_relative_path
from loguru import logger

from .constants import DEFAULT_CONFIG
from .functions import exclude_keys, merge_defaults, validate_widgets
from .widget_settings import BarConfig


class HydeConfig:
    "A class to read the configuration file and return the default configuration"

    instance = None

    @staticmethod
    def get_default():
        if HydeConfig.instance is None:
            HydeConfig.instance = HydeConfig()

        return HydeConfig.instance

    def __init__(self):
        self.default_config()

    # Function to read the configuration file
    def read_config(self) -> dict:
        config_file = get_relative_path("../config.json")
        if not os.path.exists(config_file):
            with open(config_file, "w") as destination_file:
                json.dump(
                    DEFAULT_CONFIG, destination_file, indent=4, ensure_ascii=False
                )
            return DEFAULT_CONFIG

        with open(config_file) as file:
            # Load JSON data into a Python dictionary
            data = json.load(file)
        return data

    def default_config(self) -> BarConfig:
        # Read the configuration from the JSON file
        logger.info("Applying new settings...")
        parsed_data = self.read_config()

        validate_widgets(parsed_data, DEFAULT_CONFIG)

        for key in exclude_keys(DEFAULT_CONFIG, ["$schema"]):
            if key == "module_groups":
                # For lists, use the user's value or default if not present
                parsed_data[key] = parsed_data.get(key, DEFAULT_CONFIG[key])
            else:
                # For dictionaries, merge with defaults
                parsed_data[key] = merge_defaults(
                    parsed_data.get(key, {}), DEFAULT_CONFIG[key]
                )

        self.config = parsed_data

    def set_css_settings(self):
        logger.info("Applying css settings...")

        settings = ""
        # for setting in self.config["css_settings"]:
        for setting in self.try_get_property("css_settings", [], True):
            settings += (
                f"${setting}: {self.try_get_property(setting, 'css_settings')};\n"
            )

        with open(get_relative_path("styles/_settings.scss"), "w") as f:
            f.write(settings)


configuration = HydeConfig().get_default()
widget_config = configuration.config
