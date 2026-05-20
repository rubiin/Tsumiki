import json
from pathlib import Path

from fabric.utils import exec_shell_command, os, re

from .base import SingletonService


class PrivacyIndicatorService(SingletonService):
    """Detect applications using microphone, camera, or screen sharing."""

    SCREEN_SHARE_PATTERNS = (
        r"^xdph-streaming",
        r"^gsr-default",
        r"^game capture",
        r"^screen",
        r"^desktop",
        r"^display",
        r"^cast",
        r"^webrtc",
        r"^v4l2",
        r"screen-cast",
        r"screen-capture",
        r"desktop-capture",
        r"monitor-capture",
        r"window-capture",
        r"game-capture",
    )
    SCREEN_SHARE_RE = re.compile("|".join(SCREEN_SHARE_PATTERNS))

    def _load_pipewire_objects(self):
        try:
            return json.loads(exec_shell_command("pw-dump"))
        except Exception:
            return []

    def split_pipewire_objects(self, objects):
        nodes = []
        links = []

        for obj in objects:
            obj_type = obj.get("type", "")
            if obj_type.endswith("Node"):
                nodes.append(obj)
            elif obj_type.endswith("Link"):
                links.append(obj)

        return nodes, links

    def _linked_node_ids(self, links):
        node_ids = set()

        for link in links:
            info = link.get("info", {})
            output_id = info.get("output-node-id")
            input_id = info.get("input-node-id")
            if output_id is not None:
                node_ids.add(output_id)
            if input_id is not None:
                node_ids.add(input_id)

        return node_ids

    def has_node_links(self, node_id, links):
        return node_id in self._linked_node_ids(links)

    def get_app_name(self, props):
        return (
            props.get("application.name")
            or props.get("node.nick")
            or props.get("node.name")
            or ""
        )

    def is_screen_share_node(self, props):
        media_class = props.get("media.class", "")

        if "Audio" in media_class:
            return False

        if "Video" not in media_class:
            return False

        media_name = props.get("media.name", "").lower()
        return bool(self.SCREEN_SHARE_RE.search(media_name))

    def _detect_microphone_apps(self, nodes, linked_node_ids, filter_regex=None):
        regex = re.compile(filter_regex) if filter_regex else None
        apps = set()

        for node in nodes:
            info = node.get("info", {})
            props = info.get("props", {})

            if props.get("media.class") != "Stream/Input/Audio":
                continue

            if props.get("stream.capture.sink") == "true":
                continue

            node_id = node.get("id")
            if node_id not in linked_node_ids:
                continue

            app = self.get_app_name(props)
            if regex and regex.search(app):
                continue

            if app:
                apps.add(app)

        return list(apps)

    def _detect_screen_share_apps(self, nodes, linked_node_ids):
        apps = set()

        for node in nodes:
            info = node.get("info", {})
            props = info.get("props", {})
            node_id = node.get("id")

            if node_id not in linked_node_ids:
                continue

            if self.is_screen_share_node(props):
                app = self.get_app_name(props)
                if app:
                    apps.add(app)

        return list(apps)

    def _camera_video_devices(self):
        video_devs = set()

        for dev in Path("/sys/class/video4linux").glob("video*"):
            name_file = dev / "name"
            if not name_file.exists():
                continue

            device_name = name_file.read_text().strip()
            if "Metadata" in device_name:
                continue

            video_devs.add(f"/dev/{dev.name}")

        return video_devs

    def detect_camera_apps(self, filter_regex=None):
        video_devs = self._camera_video_devices()
        if not video_devs:
            return []

        regex = re.compile(filter_regex) if filter_regex else None
        apps = set()

        for proc in Path("/proc").glob("[0-9]*"):
            fd_dir = proc / "fd"
            if not fd_dir.exists():
                continue

            try:
                for fd in fd_dir.iterdir():
                    try:
                        if os.readlink(fd) not in video_devs:
                            continue

                        comm = (proc / "comm").read_text().strip()
                        if regex and regex.search(comm):
                            break

                        apps.add(comm)
                        break
                    except Exception:
                        continue
            except Exception:
                continue

        return list(apps)

    def detect_privacy_usage(self):
        objects = self._load_pipewire_objects()
        nodes, links = self.split_pipewire_objects(objects)
        linked_node_ids = self._linked_node_ids(links)
        return {
            "microphone": self._detect_microphone_apps(nodes, linked_node_ids),
            "camera": self.detect_camera_apps(),
            "screen": self._detect_screen_share_apps(nodes, linked_node_ids),
        }


# print(PrivacyUsageDetector().detect_privacy_usage())
