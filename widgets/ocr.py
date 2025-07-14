import os
import subprocess

import gi
from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.label import Label
from gi.repository import Gdk, Gtk

from shared.widget_container import ButtonWidget
from utils.functions import ttl_lru_cache
from utils.widget_utils import nerd_font_icon

gi.require_versions({"Gtk": "3.0"})


class OCRWidget(ButtonWidget):
    """A widget that provides Optical Character Recognition functionality.

    Left-click to select an area and copy recognized text to clipboard.
    Right-click to select the OCR language from available tesseract language packs.
    """

    def __init__(self, **kwargs):
        super().__init__(name="ocr", **kwargs)

        self.current_lang = "eng"  # default
        self.initialized = False

        if self.config.get("show_icon", True):
            # Create a TextIcon with the specified icon and size
            self.icon = nerd_font_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-font-icon"},
            )
            self.box.add(self.icon)

        if self.config.get("label", True):
            self.box.add(Label(label="Ocr", style_classes="panel-text"))

        # Left click for OCR
        self.connect("button-press-event", self.on_button_press)

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Left click to OCR, right click to select language")

    def lazy_init(self):
        if not self.initialized:
            self.script_file = get_relative_path("../assets/scripts/ocr.sh")
            if not os.path.isfile(self.script_file):
                self.set_sensitive(False)
                self.set_tooltip_text("Script not found")
                return
            self.initialized = True

    def on_button_press(self, _, event):
        self.lazy_init()

        if not self.initialized:
            return  # Early exit if script not available

        base_command = f"{self.script_file} --lang {self.current_lang}"

        if self.config.get("quiet", False):
            base_command += " --no-notify"

        if event.button == 3:  # Right click
            self.show_language_menu()
        else:  # Left click
            exec_shell_command_async(base_command, lambda *_: None)

    def show_language_menu(self):
        menu = Gtk.Menu(visible=True)
        menu.set_name("ocr-menu")  # For CSS targeting

        # Get available languages
        langs = self.get_available_languages()

        for lang in langs:
            if lang != "osd":  # Skip the OSD option
                item = Gtk.MenuItem(label=lang, visible=True)
                label = item.get_child()
                label.set_name("ocr-menu-item")  # For CSS targeting
                if lang == self.current_lang:
                    label.get_style_context().add_class("selected")
                item.connect("activate", self.on_language_selected, lang)
                menu.append(item)

        menu.popup_at_widget(self, Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, None)

    @ttl_lru_cache(600, 10)
    def get_available_languages(self):
        # Run the command synchronously to get output
        try:
            result = subprocess.check_output(["tesseract", "--list-langs"], text=True)
            # Skip first line (header) and filter empty lines
            return [lang.strip() for lang in result.split("\n")[1:] if lang.strip()]
        except subprocess.CalledProcessError:
            return ["eng"]  # fallback to English if command fails

    def on_language_selected(self, _, lang):
        self.current_lang = lang
        self.set_tooltip_text(f"OCR ({lang})")
