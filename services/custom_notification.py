import json
import os
from typing import List

from fabric import Signal
from fabric.notifications import Notification, Notifications
from loguru import logger

from utils.colors import Colors
from utils.config import widget_config
from utils.constants import NOTIFICATION_CACHE_FILE


class CustomNotifications(Notifications):
    """A service to manage the notifications."""

    @Signal
    def clear_all(self, value: bool) -> None:
        """Signal emitted when notifications are emptied."""
        # Implement as needed for your application

    @Signal
    def notification_count(self, value: int) -> None:
        """Signal emitted when a new notification is added."""
        # Implement as needed for your application

    @Signal
    def dnd(self, value: bool) -> None:
        """Signal emitted when dnd is toggled."""
        # Implement as needed for your application

    @property
    def count(self) -> int:
        """Return the count of notifications."""
        return len(self.all_notifications)

    @property
    def dont_disturb(self) -> bool:
        """Return the pause status."""
        return self._dont_disturb

    @dont_disturb.setter
    def dont_disturb(self, value: bool):
        """Set the pause status."""
        self._dont_disturb = value
        self.emit("dnd", value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_notifications = []
        self._count = 0
        self.deserialized_notifications = []
        self._dont_disturb = False
        self._load_notifications()

    def _load_notifications(self):
        """Read notifications from the cache file."""
        if os.path.exists(NOTIFICATION_CACHE_FILE):
            try:
                with open(NOTIFICATION_CACHE_FILE, "r") as file:
                    self.all_notifications = json.load(file)
                    self._count = len(self.all_notifications)
            except (json.JSONDecodeError, KeyError, ValueError, IndexError) as e:
                logger.error(f"{Colors.INFO}[Notification] {e}")

    def remove_notification(self, id: int):
        """Remove the notification of given id."""
        item = next((p for p in self.all_notifications if p["id"] == id), None)
        if item:
            self.all_notifications.remove(item)
            self._write_notifications(self.all_notifications)
            self.emit("notification_count", len(self.all_notifications))

            # Emit clear_all signal if there are no notifications left
            if len(self.all_notifications) == 0:
                self.emit("clear_all", True)

    def cache_notification(self, data: Notification, max_count: int):
        """Cache the notification."""
        self._count += 1
        new_id = self._count

        # Create the new notification data
        serialized_data = data.serialize()
        serialized_data.update({
            "id": new_id,
            "app_name": data.app_name
        })

        per_app_limits = widget_config.get("notification", {}).get("per_app_limits", {})
        app_limit = per_app_limits.get(data.app_name, max_count)

        # Get current notifications for this app
        app_notifications = [
            n for n in self.all_notifications
            if n["app_name"] == data.app_name
        ]

        # If we'll exceed the limit, remove oldest ones
        if len(app_notifications) >= app_limit:
            # Sort by ID to get oldest first
            app_notifications.sort(key=lambda x: x["id"])
            # Remove enough to stay under limit
            to_remove = len(app_notifications) - app_limit + 1
            for old in app_notifications[:to_remove]:
                self.all_notifications.remove(old)
                self.emit("notification-closed", old["id"], "dismissed-by-limit")

        self.all_notifications.append(serialized_data)

        # Remove oldest notification if total count exceeds max_count
        while len(self.all_notifications) > max_count:
            oldest = self.all_notifications.pop(0)
            self.emit("notification-closed", oldest["id"], "dismissed-by-limit")

        self._write_notifications(self.all_notifications)
        self.emit("notification_count", len(self.all_notifications))

    def clear_all_notifications(self):
        """Empty the notifications."""
        logger.info("[Notification] Clearing all notifications")
        self.all_notifications = []
        self._count = 0
        self._write_notifications(self.all_notifications)
        self.emit("notification_count", len(self.all_notifications))
        self.emit("clear_all", True)

    def _write_notifications(self, data):
        """Write the notifications to the cache file."""
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"{Colors.INFO}[Notification] Notifications written successfully.")

    def get_deserialized(self) -> List[Notification]:
        """Return the notifications."""
        if not self.deserialized_notifications:
            self.deserialized_notifications = [
                Notification.deserialize(data) for data in self.all_notifications
            ]
        return self.deserialized_notifications
