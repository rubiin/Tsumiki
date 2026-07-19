"""Process and shell command utilities."""

import ctypes
import subprocess

from fabric.utils import GLib, cooldown, exec_shell_command, exec_shell_command_async

from utils.exceptions import ExecutableNotFoundError
from utils.functions import ttl_lru_cache


# Function to set the process name
def set_process_name(name: str):
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(15, name.encode("utf-8"), 0, 0, 0)  # 15 = PR_SET_NAME


# Function to check if an app is running
def is_app_running(app_name: str) -> bool:
    return bool(exec_shell_command(f"pidof {app_name}"))


## Function to execute a shell command asynchronously
def kill_process(process_name: str):
    exec_shell_command_async(f"pkill {process_name}", lambda *_: None)


# Function to toggle a shell command
def toggle_command(command: str, full_command: str):
    if is_app_running(command):
        kill_process(command)
    else:
        subprocess.Popen(
            full_command.split(" "),
            stdin=subprocess.DEVNULL,  # No input stream
            stdout=subprocess.DEVNULL,  # Optionally discard the output
            stderr=subprocess.DEVNULL,  # Optionally discard the error output
            start_new_session=True,  # This prevents the process from being killed
        )


# Function to check if an executable exists
@ttl_lru_cache(600, 10)
def check_executable_exists(executable_name):
    executable_path = GLib.find_program_in_path(executable_name)
    if not executable_path:
        raise ExecutableNotFoundError(
            executable_name
        )  # Raise an error if the executable is not found and exit the application


# Function to play sound
@cooldown(1)
def play_sound(file: str):
    exec_shell_command_async(f"pw-play {file}", lambda *_: None)
