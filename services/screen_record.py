import subprocess
from datetime import datetime

from fabric.core.service import Property, Service, Signal
from fabric.utils import exec_shell_command, exec_shell_command_async
from gi.repository import Gio, GLib
from loguru import logger

import utils.functions as helpers
from utils.icons import icons


class ScreenRecorder(Service):
    """Service to handle screen recording"""

    _instance = None  # Class-level private instance variable

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScreenRecorder, cls).__new__(cls)
        return cls._instance

    @Signal
    def recording(self, value: bool) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def screenrecord_start(self, path, allow_audio, fullscreen=False):
        self.screenrecord_path = f"{GLib.get_home_dir()}/{path}"

        helpers.ensure_directory(self.screenrecord_path)

        if self.is_recording:
            logger.error(
                "[SCREENRECORD] Another instance of wf-recorder is already running."
            )
            return
        time = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"{self.screenrecord_path}/{time}.mp4"

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
                "-i",
                icons["ui"]["camera"],
                "-a",
                "HydePanel Screenshot Utility",
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
                logger.error(
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

    def screenshot(self, path, fullscreen=False, save_copy=True):
        self.screenshot_path = f"{GLib.get_home_dir()}/{path}"

        helpers.ensure_directory(self.screenshot_path)

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
            subprocess.run(command, check=True)
            self.send_screenshot_notification(
                file_path=file_path if file_path else None,
            )
        except Exception:
            logger.error(f"[SCREENSHOT] Failed to run command: {command}")

    def send_screenrecord_notification(self, file_path):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-i",
                icons["ui"]["camera-video"],
                "-a",
                "HyDePanel Recording Utility",
                "Screenrecord Saved",
                f"Saved Screencast at {file_path}",
            ]
        )

        proc: Gio.Subprocess = Gio.Subprocess.new(cmd, Gio.SubprocessFlags.STDOUT_PIPE)

        def do_callback(process: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = process.communicate_utf8_finish(task)
            except Exception:
                logger.error(
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
