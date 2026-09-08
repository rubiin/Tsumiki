import os
import tempfile
import unittest
from unittest import mock

from fabric.notifications import Notification
from gi.repository import GLib

from services.custom_notification import CustomNotifications


def make_notification(
    *,
    notification_id: int = 1,
    replaces_id: int = 0,
    app_name: str = "test-app",
    summary: str = "summary",
    body: str = "body",
    sync_hint: str | None = None,
    sync_value: str = "progress-key",
) -> Notification:
    """Build a Notification without DBus/GTK, optionally with a sync hint."""
    data = {
        "id": notification_id,
        "replaces-id": replaces_id,
        "app-name": app_name,
        "app-icon": "",
        "summary": summary,
        "body": body,
        "timeout": 5000,
        "urgency": 1,
        "actions": [],
        "image-file": None,
        "image-pixmap": None,
        "time": 100.0,
    }
    notification = Notification.deserialize(data)
    hints = {}
    if sync_hint is not None:
        hints[sync_hint] = GLib.Variant("s", sync_value)
    notification._hints = GLib.Variant("a{sv}", hints)
    return notification


class CustomNotificationsTest(unittest.TestCase):
    """Test replace_id / sync-hint replacement in the notification service."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._cache_file = os.path.join(self._tmpdir.name, "notifications.json")

        patchers = [
            mock.patch(
                "services.custom_notification.NOTIFICATION_CACHE_FILE",
                self._cache_file,
            ),
            # Avoid owning the real DBus name in tests.
            mock.patch("gi.repository.Gio.bus_own_name", return_value=1),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self._tmpdir.cleanup)

        self.service = CustomNotifications()

    def test_replaces_id_updates_in_place(self):
        self.service.cache_notification({}, make_notification(summary="old"), 100)

        replacement = make_notification(replaces_id=1, summary="new", body="updated")
        self.service.cache_notification({}, replacement, 100)

        self.assertEqual(len(self.service.all_notifications), 1)
        entry = self.service.all_notifications[0]
        self.assertEqual(entry["id"], 1)
        self.assertEqual(entry["summary"], "new")
        self.assertEqual(entry["body"], "updated")

    def test_replaces_id_missing_target_appends(self):
        self.service.cache_notification({}, make_notification(summary="first"), 100)

        self.service.cache_notification(
            {}, make_notification(replaces_id=999, summary="orphan"), 100
        )

        self.assertEqual(len(self.service.all_notifications), 2)
        self.assertEqual(self.service.all_notifications[1]["id"], 2)
        self.assertEqual(self.service._count, 2)

    def test_sync_hint_replaces_in_place(self):
        self.service.cache_notification(
            {}, make_notification(sync_hint="synchronous", summary="old"), 100
        )
        self.service.cache_notification(
            {}, make_notification(sync_hint="synchronous", summary="new"), 100
        )

        self.assertEqual(len(self.service.all_notifications), 1)
        self.assertEqual(self.service.all_notifications[0]["id"], 1)
        self.assertEqual(self.service.all_notifications[0]["summary"], "new")
        self.assertEqual(self.service._synchronous_ids["progress-key"], 1)

    def test_private_sync_hint_keys_also_replace(self):
        for hint in ("private-synchronous", "x-canonical-private-synchronous"):
            with self.subTest(hint=hint):
                service = CustomNotifications()
                service.cache_notification(
                    {}, make_notification(sync_hint=hint, summary="old"), 100
                )
                service.cache_notification(
                    {}, make_notification(sync_hint=hint, summary="new"), 100
                )
                self.assertEqual(len(service.all_notifications), 1)
                self.assertEqual(service.all_notifications[0]["summary"], "new")

    def test_replacement_does_not_advance_count(self):
        self.service.cache_notification({}, make_notification(summary="old"), 100)
        self.assertEqual(self.service._count, 1)

        self.service.cache_notification(
            {}, make_notification(replaces_id=1, summary="new"), 100
        )
        self.assertEqual(self.service._count, 1)
        self.assertEqual(len(self.service.all_notifications), 1)

        self.service.cache_notification({}, make_notification(summary="fresh"), 100)
        self.assertEqual(self.service._count, 2)
        self.assertEqual(len(self.service.all_notifications), 2)
        self.assertEqual(self.service.all_notifications[1]["id"], 2)

    def test_replacement_respects_per_app_limit(self):
        widget_config = {"notification": {"per_app_limits": {"test-app": 1}}}

        self.service.cache_notification(
            widget_config, make_notification(summary="old"), 100
        )
        self.service.cache_notification(
            widget_config, make_notification(replaces_id=1, summary="new"), 100
        )

        # The in-place update is already counted - no extra eviction.
        self.assertEqual(len(self.service.all_notifications), 1)
        self.assertEqual(self.service.all_notifications[0]["summary"], "new")

    def test_notification_count_emitted_on_replacement(self):
        counts = []
        self.service.connect(
            "notification_count", lambda *args: counts.append(args[-1])
        )

        self.service.cache_notification({}, make_notification(summary="old"), 100)
        self.service.cache_notification(
            {}, make_notification(replaces_id=1, summary="new"), 100
        )

        self.assertEqual(counts[-1], 1)
        self.assertEqual(self.service.count, 1)

    def test_sync_map_restored_from_cache(self):
        self.service.cache_notification(
            {}, make_notification(sync_hint="synchronous", summary="old"), 100
        )

        restored = CustomNotifications()
        self.assertEqual(restored._synchronous_ids, {"progress-key": 1})

        restored.cache_notification(
            {}, make_notification(sync_hint="synchronous", summary="new"), 100
        )
        self.assertEqual(len(restored.all_notifications), 1)
        self.assertEqual(restored.all_notifications[0]["id"], 1)
        self.assertEqual(restored.all_notifications[0]["summary"], "new")

    def test_drop_registry_entry_leaves_history_untouched(self):
        self.service._notifications = {1: make_notification()}
        self.service.all_notifications = [
            {
                "id": 1,
                "replaces-id": 0,
                "app-name": "test-app",
                "app-icon": "",
                "summary": "s",
                "body": "b",
                "timeout": 5000,
                "urgency": 1,
                "actions": [],
                "image-file": None,
                "image-pixmap": None,
                "time": 100.0,
            }
        ]

        self.service.drop_registry_entry(1)

        self.assertNotIn(1, self.service._notifications)
        self.assertEqual(len(self.service.all_notifications), 1)


if __name__ == "__main__":
    unittest.main()
