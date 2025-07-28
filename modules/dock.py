import json
import logging
from typing import ClassVar

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import (
    bulk_connect,
    exec_shell_command_async,
    idle_add,
    remove_handler,
)
from fabric.utils.helpers import get_desktop_applications
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Gdk, GLib

from shared.widget_container import BaseWidget
from utils.icon_resolver import IconResolver
from utils.icons import symbolic_icons
from utils.occlusion import check_occlusion


class Dock(Window, BaseWidget):
    """Dock class for managing application buttons and interactions."""

    _instances: ClassVar[list] = []

    def get_desktop_applications(self):
        apps = get_desktop_applications()
        # Filter out apps that are in the ignored_apps list
        ignored_apps = self.config.get("ignored_apps", [])
        filtered_apps = [app for app in apps if app.name not in ignored_apps]

        return filtered_apps

    def __init__(self, config, **kwargs):
        self.config = config["modules"]["dock"]

        super().__init__(
            name="dock-window",
            layer=self.config.get("layer", "overlay"),
            anchor=self.config.get("anchor", "center"),
            margin="-8px 0 -4px 0"
            if self.config.get("anchor", "center") == "bottom-center"
            else "0 -4px 0 -8px",
            exclusivity="none",
            **kwargs,
        )
        # Add this instance to the registry
        Dock._instances.append(self)
        self.conn = get_hyprland_connection()
        self.icon = IconResolver()
        self.pinned = self.config.get("pinned_apps", [])
        self.OCCLUSION = 36 + self.config["icon_size"]
        self.app_map = {}  # Initialize the app map
        self._all_apps = self.get_desktop_applications()  # Get all apps for lookup

        # Create app identifiers mapping
        self.app_identifiers = self._build_app_identifiers_map()
        self.is_hidden = False
        self.hide_id = None
        self._arranger_handler = None
        self._drag_in_progress = False  # Drag lock flag
        self.is_hovered = False

        # Set up UI containers
        self.view = Box(
            name="viewport",
            orientation="h"
            if self.config.get("anchor", "center") == "bottom-center"
            else "v",
            spacing=4,
        )
        self.wrapper = Box(name="dock", orientation="v", children=[self.view])

        # Main dock container with hover handling
        self.dock_eventbox = EventBox()
        self.dock_eventbox.add(self.wrapper)

        bulk_connect(
            self.dock_eventbox,
            {
                "enter-notify-event": self._on_dock_enter,
                "leave-notify-event": self._on_dock_leave,
            },
        )

        # Bottom hover activation area
        self.hover_activator = EventBox()
        self.hover_activator.set_size_request(-1, 1)

        bulk_connect(
            self.hover_activator,
            {
                "enter-notify-event": self._on_hover_enter,
                "leave-notify-event": self._on_hover_leave,
            },
        )

        self.main_box = Box(
            orientation="v", children=[self.dock_eventbox, self.hover_activator]
        )
        self.add(self.main_box)

        # Initialization
        if self.conn.ready:
            self.update_dock()
            GLib.timeout_add(500, self.check_hide)
        else:
            bulk_connect(
                self.conn,
                {"event::ready": self.check_hide},
            )

        for ev in ("activewindow", "openwindow", "closewindow", "changefloatingmode"):
            self.conn.connect(f"event::{ev}", self.update_dock)
        self.conn.connect("event::workspace", self.check_hide)

        GLib.timeout_add(250, self.check_occlusion_state)

    def _build_app_identifiers_map(self):
        """Build a mapping of app identifiers to DesktopApp objects"""
        identifiers = {}
        for app in self._all_apps:
            # Map by name (lowercase)
            if app.name:
                identifiers[app.name.lower()] = app

            # Map by display name
            if app.display_name:
                identifiers[app.display_name.lower()] = app

            # Map by window class if available
            if app.window_class:
                identifiers[app.window_class.lower()] = app

            # Map by executable name if available
            if app.executable:
                exe_basename = app.executable.split("/")[-1].lower()
                identifiers[exe_basename] = app

            # Map by command line if available (without parameters)
            if app.command_line:
                cmd_base = app.command_line.split()[0].split("/")[-1].lower()
                identifiers[cmd_base] = app

        return identifiers

    def _normalize_window_class(self, class_name: str):
        """Normalize window class by removing common suffixes and lowercase."""
        if not class_name:
            return ""

        normalized = class_name.lower()

        # Remove common suffixes
        suffixes = [".bin", ".exe", ".so", "-bin", "-gtk"]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[: -len(suffix)]

        return normalized

    def _classes_match(self, class1: str, class2: str):
        """Check if two window class names match with stricter comparison."""
        if not class1 or not class2:
            return False

        # Normalize both classes
        norm1 = self._normalize_window_class(class1)
        norm2 = self._normalize_window_class(class2)

        # Direct match after normalization
        return norm1 == norm2

    def _on_hover_enter(self, *_):
        """Handle hover over bottom activation area"""
        self.toggle_dock(show=True)

    def _on_hover_leave(self, *_):
        """Handle leave from bottom activation area"""
        self.delay_hide()

    def _on_dock_enter(self, widget, event):
        """Handle hover over dock content"""
        self.is_hovered = True
        self.wrapper.remove_style_class("occluded")
        # Cancel any pending hide operations
        if self.hide_id:
            GLib.source_remove(self.hide_id)
            self.hide_id = None
        self.toggle_dock(show=True)
        return True  # Important: Stop event propagation

    def _on_dock_leave(self, widget, event):
        """Handle leave from dock content"""
        # Only trigger if mouse actually left the entire dock area
        if event.detail == Gdk.NotifyType.INFERIOR:
            return False  # Ignore child-to-child mouse movements

        self.is_hovered = False
        self.delay_hide()
        # Immediate occlusion check on true leave using simplified format

        occlusion_region = (
            ("bottom", self.OCCLUSION)
            if self.config.get("anchor", "center") == "bottom-center"
            else ("right", self.OCCLUSION)
        )
        # Only add occlusion style if not dragging an icon.
        if not self._drag_in_progress and (
            check_occlusion(occlusion_region) or not self.view.get_children()
        ):
            self.wrapper.add_style_class("occluded")
        return True

    # Enhanced app lookup methods
    def find_app(self, app_identifier):
        """Return the DesktopApp object by matching any app identifier.

        If app_identifier is a dict, it will use all available keys for matching.
        """
        if not app_identifier:
            return None

        # If we got a dict object with app data (new format)
        if isinstance(app_identifier, dict):
            # Try to find by all available identifiers in priority order
            for key in [
                "window_class",
                "executable",
                "command_line",
                "name",
                "display_name",
            ]:
                if app_identifier.get(key):
                    app = self.find_app_by_key(app_identifier[key])
                    if app:
                        return app
            return None

        # Simple string identifier (backward compatibility)
        return self.find_app_by_key(app_identifier)

    def find_app_by_key(self, key_value: str):
        """Find app by a single identifier value"""
        if not key_value:
            return None

        # Try direct lookup in our identifiers map
        normalized_id = str(key_value).lower()
        if normalized_id in self.app_identifiers:
            return self.app_identifiers[normalized_id]

        # Try fuzzy matching - find apps where the identifier is part of their names
        for app in self._all_apps:
            if app.name and normalized_id in app.name.lower():
                return app
            if app.display_name and normalized_id in app.display_name.lower():
                return app
            if app.window_class and normalized_id in app.window_class.lower():
                return app
            if app.executable and normalized_id in app.executable.lower():
                return app
            if app.command_line and normalized_id in app.command_line.lower():
                return app

        return None

    # Update the dock's app map using DesktopApp objects from the system.
    def update_app_map(self):
        """Updates the mapping of commands to DesktopApp objects."""
        self._all_apps = self.get_desktop_applications()  # Refresh all apps
        self.app_map = {
            app.name: app for app in self._all_apps if app.name
        }  # Map app names to DesktopApp objects
        self.app_identifiers = (
            self._build_app_identifiers_map()
        )  # Rebuild identifiers map

    def create_button(self, app_identifier, instances):
        """Create dock application button"""
        desktop_app = self.find_app(app_identifier)  # Find app by identifier
        icon_img = None
        display_name = None

        if desktop_app:
            icon_img = desktop_app.get_icon_pixbuf(size=self.config["icon_size"])
            display_name = desktop_app.display_name or desktop_app.name

        # Extract identifier for fallback
        id_value = (
            app_identifier["name"]
            if isinstance(app_identifier, dict)
            else app_identifier
        )

        if not icon_img:
            # Fallback to IconResolver with the app command
            icon_img = self.icon.get_icon_pixbuf(
                id_value, self.config.get("icon_size", 16)
            )  # Use identifier for fallback

        if not icon_img:  # Double check after exec path try
            # Fallback icon if no DesktopApp is found
            icon_img = self.icon.get_icon_pixbuf(
                symbolic_icons["fallback"]["executable"],
                self.config.get("icon_size", 16),
            )
            # Final fallback
            if not icon_img:
                icon_img = self.icon.get_icon_pixbuf(
                    symbolic_icons["fallback"]["image"],
                    self.config.get("icon_size", 16),
                )

        items = [Image(pixbuf=icon_img)]

        tooltip = display_name or (id_value if isinstance(id_value, str) else "Unknown")
        if not display_name and instances and instances[0].get("title"):
            tooltip = instances[0]["title"]

        button = Button(
            child=Box(
                name="dock-icon",
                orientation="v",
                h_align="center",
                children=items,
            ),
            on_clicked=lambda *a: self.handle_app(
                app_identifier, instances, desktop_app
            ),  # Pass desktop_app as well
            tooltip_text=tooltip,
            name="dock-app-button",
        )

        # Store app data with the button for future reference
        button.app_identifier = app_identifier
        button.desktop_app = desktop_app
        button.instances = instances

        if instances:
            button.add_style_class("instance")  # Style running apps

        button.connect("enter-notify-event", self._on_child_enter)
        return button

    # Enhanced app launching with multiple fallbacks
    def handle_app(self, app_identifier, instances, desktop_app=None):
        """Handle application button clicks with improved fallbacks"""
        if not instances:
            # Try to launch the app with multiple fallback methods
            if not desktop_app:
                desktop_app = self.find_app(app_identifier)

            if desktop_app:
                # Try the standard launch method first
                launch_success = desktop_app.launch()

                # If that fails, try command line or executable
                if not launch_success:
                    if desktop_app.command_line:
                        exec_shell_command_async(
                            f"nohup {desktop_app.command_line}",
                            lambda _: None,
                        )
                    elif desktop_app.executable:
                        exec_shell_command_async(
                            f"nohup {desktop_app.executable}",
                            lambda _: None,
                        )
            else:
                # No desktop entry found, try direct execution
                if isinstance(app_identifier, dict):
                    # Try command_line first, then executable, then name as last resort
                    if app_identifier.get("command_line"):
                        exec_shell_command_async(
                            f"nohup {app_identifier['command_line']}",
                            lambda _: None,
                        )
                    elif app_identifier.get("executable"):
                        exec_shell_command_async(
                            f"nohup {app_identifier['executable']}",
                            lambda _: None,
                        )
                    elif app_identifier.get("name"):
                        exec_shell_command_async(
                            f"nohup {app_identifier['name']}",
                            lambda _: None,
                        )
                elif isinstance(app_identifier, str):
                    # Try direct execution with the identifier as fallback
                    exec_shell_command_async(
                        f"nohup {app_identifier}",
                        lambda _: None,
                    )
        else:
            # Handle window switching for running instances
            focused = self.get_focused()
            idx = next(
                (i for i, inst in enumerate(instances) if inst["address"] == focused),
                -1,
            )
            next_inst = instances[(idx + 1) % len(instances)]
            exec_shell_command_async(
                f"hyprctl dispatch focuswindow address:{next_inst['address']}"
            )

    def _on_child_enter(self, widget, event):
        """Maintain hover state when entering child widgets"""
        self.is_hovered = True
        if self.hide_id:
            GLib.source_remove(self.hide_id)
            self.hide_id = None
        return False  # Continue event propagation

    def toggle_dock(self, show):
        """Show or hide the dock immediately"""
        if show:
            if self.is_hidden:
                self.is_hidden = False
                self.wrapper.add_style_class("show-dock")
                self.wrapper.remove_style_class("hide-dock")
            if self.hide_id:
                GLib.source_remove(self.hide_id)
                self.hide_id = None
        else:
            if not self.is_hidden:
                self.is_hidden = True
                self.wrapper.add_style_class("hide-dock")
                self.wrapper.remove_style_class("show-dock")

    def delay_hide(self):
        """Schedule hiding after short delay"""
        if self.hide_id:
            GLib.source_remove(self.hide_id)
        self.hide_id = GLib.timeout_add(1000, self.hide_dock)

    def hide_dock(self):
        """Finalize hiding procedure"""
        self.toggle_dock(show=False)
        self.hide_id = None
        return False

    def check_hide(self, *_):
        """Determine if dock should auto-hide"""
        clients = self.get_clients()
        current_ws = self.get_workspace()
        ws_clients = [w for w in clients if w["workspace"]["id"] == current_ws]

        if not ws_clients:
            self.toggle_dock(show=True)
        elif any(not w.get("floating") and not w.get("fullscreen") for w in ws_clients):
            self.delay_hide()
        else:
            self.toggle_dock(show=True)

    def update_dock(self, *_):
        """Refresh dock contents and clear drag lock."""
        self.update_app_map()  # Update app map before creating buttons
        arranger_handler = getattr(self, "_arranger_handler", None)
        if arranger_handler:
            remove_handler(arranger_handler)
        clients = self.get_clients()

        # Create a mapping of window class to instances
        running_windows = {}
        for c in clients:
            # Try multiple identification methods in order of reliability
            window_id = None

            # Try initialClass first (most reliable)
            if (class_name := c.get("initialClass", "").lower()) or (
                class_name := c.get("class", "").lower()
            ):
                window_id = class_name

            # Use title as last resort if both class identifiers are missing
            elif title := c.get("title", "").lower():
                # Extract app name from title (common format: "App Name - Document")
                possible_name = title.split(" - ")[0].strip()
                if (
                    possible_name and len(possible_name) > 1
                ):  # Avoid single letter app names
                    window_id = possible_name
                else:
                    window_id = title  # Use full title if we can't extract a good name

            # Use generic identifier as absolute fallback
            if not window_id:
                window_id = "unknown-app"

            # Log window for debugging purposes
            logging.debug(
                f"""Window detected: {window_id} (from {c.get("initialClass", "")}/
                {c.get("class", "")}/{c.get("title", "")})"""
            )

            # Add to running windows - store with both original and normalized keys
            running_windows.setdefault(window_id, []).append(c)

            # Also store with normalized key for more flexible matching
            normalized_id = self._normalize_window_class(window_id)
            if normalized_id != window_id:
                running_windows.setdefault(normalized_id, []).extend(
                    running_windows[window_id]
                )

        # Map pinned apps to their running instances
        pinned_buttons = []
        used_window_classes = set()  # Track which window classes we've already assigned

        for app_data in self.pinned:
            app = self.find_app(app_data)

            # Try to find running instances for this pinned app
            instances = []
            matched_class = None

            # Extract all possible identifiers from app_data for matching
            possible_identifiers = []

            if isinstance(app_data, dict):
                for key in [
                    "window_class",
                    "executable",
                    "command_line",
                    "name",
                    "display_name",
                ]:
                    if app_data.get(key):
                        possible_identifiers.extend([app_data[key].lower()])
            elif isinstance(app_data, str):
                possible_identifiers.append(app_data.lower())

            # Add identifiers from DesktopApp if available
            if app:
                if app.window_class:
                    possible_identifiers.append(app.window_class.lower())
                if app.executable:
                    possible_identifiers.append(app.executable.split("/")[-1].lower())
                if app.command_line:
                    cmd_parts = app.command_line.split()
                    if cmd_parts:
                        possible_identifiers.append(cmd_parts[0].split("/")[-1].lower())
                if app.name:
                    possible_identifiers.append(app.name.lower())
                if app.display_name:
                    possible_identifiers.append(app.display_name.lower())

            # Remove duplicates
            possible_identifiers = list(set(possible_identifiers))

            # Try each identifier for matching
            for identifier in possible_identifiers:
                # Try direct match
                if identifier in running_windows:
                    instances = running_windows[identifier]
                    matched_class = identifier
                    break

                # Try normalized version
                normalized = self._normalize_window_class(identifier)
                if normalized in running_windows:
                    instances = running_windows[normalized]
                    matched_class = normalized
                    break

                # Try substring matching for window classes (less reliable but helpful)
                for window_class in running_windows:
                    # For substring matching, ensure the identifier is at least 3 chars
                    # to avoid too broad matches
                    if len(identifier) >= 3 and identifier in window_class:
                        instances = running_windows[window_class]
                        matched_class = window_class
                        logging.debug(
                            f"Substring match: {identifier} in {window_class}"
                        )
                        break

                if matched_class:
                    break

            # Mark the matched class as used
            if matched_class:
                used_window_classes.add(matched_class)
                # Also mark the normalized version as used
                used_window_classes.add(self._normalize_window_class(matched_class))
                logging.debug(
                    f"""Matched pinned app {app_data} to running
                      instances via {matched_class}"""
                )

            # Create button for this pinned app with any found instances
            pinned_buttons.append(self.create_button(app_data, instances))

        # For any remaining window classes that aren't assigned to pinned apps
        open_buttons = []
        for class_name, instances in running_windows.items():
            if class_name not in used_window_classes:
                # Enhanced app identification for running windows
                app = None

                # Try multiple methods to find the correct app
                # 1. Direct lookup by class name
                app = self.app_identifiers.get(class_name)

                # 2. Try with normalized class name
                if not app:
                    norm_class = self._normalize_window_class(class_name)
                    app = self.app_identifiers.get(norm_class)

                # 3. Try with our more robust find_app method
                if not app:
                    app = self.find_app_by_key(class_name)

                # 4. Try using window title which often contains app name
                if not app and instances and instances[0].get("title"):
                    title = instances[0].get("title", "")
                    # Extract app name from title (format: "App Name - Document")
                    potential_name = title.split(" - ")[0].strip()
                    if len(potential_name) > 2:  # Avoid very short names
                        app = self.find_app_by_key(potential_name)

                # Create comprehensive app data if app was found
                if app:
                    app_data = {
                        "name": app.name,
                        "display_name": app.display_name,
                        "window_class": app.window_class,
                        "executable": app.executable,
                        "command_line": app.command_line,
                    }
                    identifier = app_data
                else:
                    # Fallback to just class name
                    identifier = class_name

                open_buttons.append(self.create_button(identifier, instances))

        # Assemble dock layout
        children = pinned_buttons
        # Only add separator if both pinned and open buttons exist
        if pinned_buttons and open_buttons:
            children += [
                Box(
                    orientation="v"
                    if self.config.get("anchor", "center") == "bottom-center"
                    else "h",
                    v_expand=self.config.get("anchor", "center") != "bottom-center",
                    h_expand=self.config.get("anchor", "center") == "bottom-center",
                    name="dock-separator",
                )
            ]
        children += open_buttons

        self.view.children = children
        idle_add(self._update_size)
        self._drag_in_progress = False  # Clear the drag lock

    def _update_size(self):
        """Update window size based on content"""
        width, _ = self.view.get_preferred_width()
        self.set_size_request(width, -1)
        return False

    def get_clients(self):
        """Get current client list"""
        try:
            return json.loads(self.conn.send_command("j/clients").reply.decode())
        except json.JSONDecodeError:
            return []

    def get_focused(self):
        """Get focused window address"""
        try:
            return json.loads(
                self.conn.send_command("j/activewindow").reply.decode()
            ).get("address", "")
        except json.JSONDecodeError:
            return ""

    def get_workspace(self):
        """Get current workspace ID"""
        try:
            return json.loads(
                self.conn.send_command("j/activeworkspace").reply.decode()
            ).get("id", 0)
        except json.JSONDecodeError:
            return 0

    def check_occlusion_state(self):
        """Periodic occlusion check"""
        # Skip occlusion check if hovered or dragging an icon
        if self.is_hovered or self._drag_in_progress:
            self.wrapper.remove_style_class("occluded")
            return True
        occlusion_region = (
            ("bottom", self.OCCLUSION)
            if self.config.get("anchor", "center") == "bottom-center"
            else ("right", self.OCCLUSION)
        )
        if check_occlusion(occlusion_region) or not self.view.get_children():
            self.wrapper.add_style_class("occluded")
        else:
            self.wrapper.remove_style_class("occluded")
        return True

    def _find_drag_target(self, widget):
        """Find valid drag target in viewport"""
        children = self.view.get_children()
        while widget is not None and widget not in children:
            widget = widget.get_parent() if hasattr(widget, "get_parent") else None
        return widget
