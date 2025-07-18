import os
from datetime import datetime

from fabric.core.service import Property, Service, Signal
from fabric.utils import exec_shell_command, exec_shell_command_async
from gi.repository import Gio, GLib
from loguru import logger

import utils.functions as helpers
from utils.constants import APPLICATION_NAME
from utils.icons import symbolic_icons


class ScreenRecorderService(Service):
    """Service to handle screen recording"""

    @Signal
    def recording(self, value: bool) -> None: ...

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home_dir = GLib.get_home_dir()

    def screenrecord_start(self, path: str, allow_audio: bool, fullscreen=False):
        """Start screen recording using wf-recorder."""
        if not path:
            logger.exception("[SCREENRECORD] No path provided for screen recording.")
            return

        self.screenrecord_path = os.path.join(self.home_dir, path)

        if self.is_recording:
            logger.exception(
                "[SCREENRECORD] Another instance of wf-recorder is already running."
            )
            return
        time = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.screenrecord_path, f"{time}.mp4")

        self._current_screencast_path = file_path
        area = "" if fullscreen else f"-g '{exec_shell_command('slurp')}'"
        audio = "--audio" if allow_audio else ""
        command = (
            f"wf-recorder {audio} --file={file_path} --pixel-format yuv420p {area}"
        )
        exec_shell_command_async(command, lambda *_: None)
        self.emit("recording", True)

    def send_screenshot_notification(self, file_path=None):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-A",
                "edit=Edit",
                "-t",
                "5000",
                "-i",
                symbolic_icons["ui"]["camera"],
                "-a",
                f"{APPLICATION_NAME} Screenshot Utility",
                "-h",
                f"STRING:image-path:{file_path}",
                "Screenshot Saved",
                f"Saved Screenshot at {file_path}",
            ]
            if file_path
            else ["Screenshot Sent to Clipboard"]
        )

        proc: Gio.Subprocess = Gio.Subprocess.new(cmd, Gio.SubprocessFlags.STDOUT_PIPE)

        def do_callback(process: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = process.communicate_utf8_finish(task)
            except Exception:
                logger.exception(
                    f"[SCREENSHOT] Failed read notification action with error {stderr}"
                )
                return

            match stdout.strip("\n"):
                case "files":
                    exec_shell_command_async(f"xdg-open {self.screenshot_path}")
                case "view":
                    exec_shell_command_async(f"xdg-open {file_path}")
                case "edit":
                    exec_shell_command_async(f"swappy -f {file_path}")

        proc.communicate_utf8_async(None, None, do_callback)

    def screenshot(self, path: str, fullscreen=False, save_copy=True):
        """Take a screenshot using grimblast."""
        if not path:
            logger.exception("[SCREENSHOT] No path provided for screenshot.")
            return

        self.screenshot_path = os.path.join(self.home_dir, path)

        time = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

        file_path = f"{self.screenshot_path}/{time}.png"
        command = (
            ["grimblast", "copysave", "screen", file_path]
            if save_copy
            else ["grimblast", "copyscreen"]
        )
        if not fullscreen:
            command[2] = "area"
        try:
            exec_shell_command_async(
                " ".join(command),
                lambda *_: self.send_screenshot_notification(
                    file_path=file_path if file_path else None,
                ),
            )
        except Exception:
            logger.exception(f"[SCREENSHOT] Failed to run command: {command}")

    def send_screenrecord_notification(self, file_path: str):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-t",
                "5000",
                "-i",
                symbolic_icons["ui"]["camera-video"],
                "-a",
                f"{APPLICATION_NAME} Recording Utility",
                "Screenrecord Saved",
                f"Saved Screencast at {file_path}",
            ]
        )

        proc: Gio.Subprocess = Gio.Subprocess.new(cmd, Gio.SubprocessFlags.STDOUT_PIPE)

        def do_callback(process: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = process.communicate_utf8_finish(task)
            except Exception:
                logger.exception(
                    f"[SCREENRECORD] Failed read notification action with error."
                    f"{stderr}"
                )
                return

            match stdout.strip("\n"):
                case "files":
                    exec_shell_command_async(
                        f"xdg-open {self.screenrecord_path}", lambda *_: None
                    )
                case "view":
                    exec_shell_command_async(f"xdg-open {file_path}", lambda *_: None)

        proc.communicate_utf8_async(None, None, do_callback)

    @Property(bool, "readable", default_value=False)
    def is_recording(self):
        return helpers.is_app_running("wf-recorder")

    def screenrecord_stop(self):
        helpers.kill_process("wf-recorder")
        self.emit("recording", False)
        self.send_screenrecord_notification(self._current_screencast_path)
