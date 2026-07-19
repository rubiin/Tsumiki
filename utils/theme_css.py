"""Theme and CSS compilation utilities."""

import json

from fabric import Application
from fabric.utils import (
    exec_shell_command,
    get_relative_path,
    idle_add,
    logger,
    os,
)

from utils.colors import Colors
from utils.decorators import run_in_thread, thread
from utils.functions import flatten_dict, read_toml_file, write_toml_file
from utils.shell import check_executable_exists


def _apply_css_to_app():
    try:
        app = Application.get_default()
        if app:
            app.set_stylesheet_from_file(get_relative_path("../dist/main.css"))
            logger.info(f"{Colors.INFO}[Theme] CSS applied to application")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error applying CSS to app: {e}")


def _compile_css():
    """Compile SCSS in background thread."""
    try:
        check_executable_exists("sass")
        logger.info(f"{Colors.INFO}[Theme] Recompiling CSS")
        output = exec_shell_command(
            "sass styles/main.scss dist/main.css --no-source-map"
        )

        if output == "":
            logger.info(f"{Colors.INFO}[Theme] CSS recompiled successfully")
            idle_add(_apply_css_to_app)
        else:
            logger.exception(f"{Colors.ERROR}[Theme] Failed to compile sass!")
            logger.exception(f"{Colors.ERROR}[Theme] {output}")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error recompiling CSS: {e}")


# Function to recompile SCSS and apply the new CSS
def recompile_and_apply_css():
    """Recompile SCSS and apply the new CSS to the application."""

    # Run compilation in background thread
    thread(_compile_css)


# Function to copy the selected theme to the main styles directory
@run_in_thread
def copy_themev2(theme: str, mode: str = "dark"):
    source_theme_dir = get_relative_path("../themes")
    destination_file = f"{get_relative_path('../styles')}/_theme.scss"
    source_file = f"{source_theme_dir}/{theme}.toml"

    if not os.path.exists(source_file):
        logger.warning(
            f"{Colors.WARNING}Warning: The theme file '{theme}.toml' was not found. Using default theme."  # noqa: E501
        )
        source_file = f"{source_theme_dir}/catpuccin-mocha.toml"

    try:
        contents = read_toml_file(source_file)
        if not contents:
            raise FileNotFoundError(source_file)

        selected_theme = contents.get(mode, contents)
        write_css_settings(flatten_dict(selected_theme), destination_file)

    except FileNotFoundError:
        logger.exception(
            f"{Colors.ERROR}Error: The theme file '{source_file}' was not found."
        )
        exit(1)


# Function to update the theme configuration
def update_theme_config(theme_name: str):
    """Update the config.toml file with the new theme name."""
    try:
        config_file = get_relative_path("../config.toml")

        # Read current theme config
        config = read_toml_file(config_file)

        if config is None:
            return

        # Update the theme name
        config["styling"]["theme_name"] = theme_name

        # Write back to file

        write_toml_file(config_file, config)

        logger.info(f"{Colors.INFO}[Theme] Updated theme config to {theme_name}")
    except Exception as e:
        logger.exception(f"{Colors.ERROR}[Theme] Error updating theme config: {e}")


@run_in_thread
def write_css_settings(contents, file):
    """Generate SCSS settings file from theme config."""
    logger.info("[CONFIG] Applying css settings...")

    css_styles = contents

    # Use list comprehension and join for faster string building
    lines = [
        f"${setting}: {json.dumps(value) if isinstance(value, bool) else value};"
        for setting, value in css_styles.items()
    ]

    with open(file, "w") as f:
        f.write("\n".join(lines))
        f.write("\n")
