import datetime

from fabric.core.service import Property, Service, Signal
from fabric.utils import exec_shell_command, exec_shell_command_async
from gi.repository import Gio, GLib
from loguru import logger

import utils.functions as helpers
from utils import BarConfig


class ScreenRecorder(Service):
    """Service to handle screen recording"""

    instance = None

    @staticmethod
    def get_default():
        if ScreenRecorder.instance is None:
            ScreenRecorder.instance = ScreenRecorder()

        return ScreenRecorder.instance

    @Signal
    def recording(self, value: bool) -> None: ...

    def __init__(self, widget_config: BarConfig, **kwargs):
        self.config = widget_config["recorder"]
        self.screenrecord_path = f"{GLib.get_home_dir()}/{self.config['path']}"

        helpers.ensure_dir_exists(self.screenrecord_path)

        super().__init__(**kwargs)

    def screencast_start(self, fullscreen=False):
        if self.is_recording:
            logger.error(
                "[SCREENRECORD] Another instance of wf-recorder is already running."
            )
            return
        time = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"{self.screenrecord_path}/{time}.mp4"

        self._current_screencast_path = file_path
        area = "" if fullscreen else f"-g '{exec_shell_command('slurp')}'"
        audio = "--audio" if self.config["audio"] else ""
        command = (
            f"wf-recorder {audio} --file={file_path} --pixel-format yuv420p {area}"
        )
        exec_shell_command_async(command)
        self.emit("recording", True)

    def screencast_stop(self):
        exec_shell_command_async("killall -INT wf-recorder", lambda *_: None)
        self.emit("recording", False)
        self.send_screencast_notification(self._current_screencast_path)

    def send_screencast_notification(self, file_path):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-i",
                "camera-video-symbolic",
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
