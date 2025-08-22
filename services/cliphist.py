import os
import re
import threading
from typing import Callable

import gi
import magic
from fabric import Fabricator, Property, Service, Signal
from gi.repository import GdkPixbuf, Gio, GLib
from loguru import logger

gi.require_versions({"Gdk": "3.0", "GdkPixbuf": "2.0"})


SUPPORTED_MIME_TYPES = [
    mime_type for fmt in GdkPixbuf.Pixbuf.get_formats() for mime_type in fmt.mime_types
]
SUPPORTED_FILE_EXTENSIONS = [
    file_extension
    for fmt in GdkPixbuf.Pixbuf.get_formats()
    for file_extension in fmt.extensions
]

# TODO: Assign a fixed number of image loading threads
# TODO: make these cancelable


def get_pixbuf_for_data_threaded(data: bytes, callback: Callable):
    def thread_function():
        try:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(data)
            loader.close()
            pixbuf = loader.get_pixbuf()
            GLib.idle_add(callback, (True, pixbuf))
        except Exception as _:
            logger.error("[CLIPBOARD] Failed make get loader for data")
            GLib.idle_add(callback, (False, None))
        finally:
            GLib.idle_add(thread.join)

    thread = threading.Thread(target=thread_function)
    thread.start()


def get_pixbuf_for_file_threaded(file_path: str, callback: Callable):
    def thread_function():
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
            GLib.idle_add(callback, (True, pixbuf))
        except Exception as _:
            logger.error(f"[CLIPBOARD] Failed make pixbuf for file: {file_path}")
            GLib.idle_add(callback, (False, None))
        finally:
            GLib.idle_add(thread.join)

    thread = threading.Thread(target=thread_function)
    thread.start()


class ClipboardHistory(Service):
    """Manages the clipboard history."""

    @Signal
    def clipboard_deleted(self, cliphist_id: str) -> str: ...

    @Signal
    def clipboard_copied(self, cliphist_id: str) -> str: ...
    @Signal
    def clipboard_data_ready(self, cliphist_id: str) -> str: ...

    def __init__(self, length_cutoff: int = 5000, file_max_size: int = 5000000):
        self._length_cutoff = length_cutoff
        self._file_max_size = file_max_size
        self._clipboard_history = {}
        self._decoded_clipboard_history = {}
        super().__init__()
        self.wl_paste_watcher = Fabricator(
            poll_from="wl-paste --watch bash -c ' sleep 0.5 && echo '",
            stream=True,
            interval=-1,
        )
        self.wl_paste_watcher.connect("changed", lambda *_: self.cliphist_list())

    def cliphist_list(self):
        def callback(proc: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = proc.communicate_utf8_finish(task)
                self._clipboard_history = {
                    key: value[7:] if value.startswith("file://") else value
                    for x in stdout.split("\n")[:-1]
                    for key, value in [x.split("\t", 1)]
                }
                self.notify("clipboard-history")
            except Exception as _:
                logger.error("[CLIPBOARD] Failed to read from `cliphist list`")

        process: Gio.Subprocess = Gio.Subprocess.new(
            ["cliphist", "list"],
            Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        )
        process.communicate_utf8_async(None, None, callback)

    def cliphist_decode(self, cliphist_id: str, callback: Callable):
        process = Gio.Subprocess.new(
            ["cliphist", "decode", str(cliphist_id)],
            Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        )
        process.communicate_async(None, None, callback)

    def cliphist_copy(self, id: str):
        def wl_wait_callback(proc: Gio.Subprocess, task: Gio.Task):
            try:
                x = proc.wait_finish(task)
                print(x)
            except Exception as e:
                logger.error(
                    f"[CLIPBOARD] Failed to copy for id: {id} when sending file {e}"
                )

        def wl_copy_callback(proc: Gio.Subprocess, task: Gio.Task):
            try:
                proc.communicate_finish(task)
                self.emit("clipboard-copied", id)
            except Exception as e:
                logger.error(
                    f"[CLIPBOARD] Failed to copy for id: {id} when sending command {e}"
                )

        def cliphist_decode_callback(proc: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = proc.communicate_finish(task)
                decoded_str: str = stdout.get_data().decode("utf8")

                file_uri = (
                    f"file://{decoded_str}"
                    if not decoded_str.startswith("file://")
                    else decoded_str
                )

                if os.path.exists(file_uri[7:]):
                    self.cliphist_delete(
                        id
                    )  # We're going to end up with copies otherwise
                    proc = Gio.Subprocess.new(
                        ["wl-copy", "--type", "text/uri-list", file_uri],
                        Gio.SubprocessFlags.STDIN_PIPE
                        | Gio.SubprocessFlags.STDERR_PIPE,
                    )
                    proc.wait_async(None, wl_wait_callback)
                else:
                    process.communicate_async(stdout, None, wl_copy_callback)

            except Exception as _:
                print(_)
                logger.error(
                    f"[CLIPBOARD] Failed to copy item with id: {id} after decode"
                )

        process: Gio.Subprocess = Gio.Subprocess.new(
            ["wl-copy"],
            Gio.SubprocessFlags.STDIN_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        )  # type: ignore
        # in_pipe: Gio.OutputStream = process.get_stdin_pipe()
        self.cliphist_decode(id, cliphist_decode_callback)

    def cliphist_delete(self, cliphist_id: str):
        self.cliphist_id = cliphist_id

        process: Gio.Subprocess = Gio.Subprocess.new(
            ["cliphist", "delete"],
            Gio.SubprocessFlags.STDIN_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        )  # type: ignore

        in_pipe: Gio.OutputStream = process.get_stdin_pipe()
        try:
            out_stream: Gio.DataOutputStream = Gio.DataOutputStream.new(in_pipe)
            out_stream.put_string(
                f"{cliphist_id}\t{self._clipboard_history[cliphist_id]}\n", None
            )
            self.emit("clipboard-deleted", self.cliphist_id)
        except Exception as _:
            logger.error(
                f"[CLIPBOARD] Failed to delete item with cliphist id: {cliphist_id}"
            )

    def parse_data_binary(self, id: str):
        preview = self._clipboard_history[id]
        info = preview.split()
        # _size = info[3:5]
        data_type = info[5]
        # image_dimensions = tuple(map(int, info[6].split("x")))

        def callback(pixbuf_loader: GdkPixbuf.Pixbuf, task: Gio.Task):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_stream_finish(task)
                self._decoded_clipboard_history[id] = pixbuf
                self.emit("clipboard-data-ready", id)

            except Exception as _:
                logger.error(
                    f"[CLIPBOARD] Failed to read pixbuf data from cliphist id: {id}"
                )

        process: Gio.Subprocess = Gio.Subprocess.new(
            ["cliphist", "decode", id],
            Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
        )  # type: ignore

        if data_type in SUPPORTED_FILE_EXTENSIONS:
            GdkPixbuf.Pixbuf.new_from_stream_async(
                process.get_stdout_pipe(), None, callback
            )

    def parse_html_tag(self, id: str):
        def on_pixbuf_ready(loader, result):
            try:
                self._decoded_clipboard_history[id] = (
                    GdkPixbuf.Pixbuf.new_from_stream_finish(result)
                )
                self.emit("clipboard-data-ready", id)
            except Exception as e:
                print(e)

        def on_file_read(stream: Gio.InputStream, task: Gio.Task, _):
            try:
                input_stream = stream.read_finish(task)
                GdkPixbuf.Pixbuf.new_from_stream_async(
                    input_stream, None, on_pixbuf_ready
                )
                input_stream.close_async(GLib.PRIORITY_DEFAULT, None, None)
            except Exception as e:
                logger.error(
                    f"[CLIPBOARD] Failed to download html image from id: {id} {e}"
                )

        def decode_callback(proc: Gio.Subprocess, task: Gio.Task):
            # TODO: The image is just read and stored in memory, since the clipboard is
            #   updated on every new `cliphist list`, this could take some time on slow
            # connections...
            #
            #   We can store these images in a cache file instead, will fix copying
            # these since it current is returning an html tag instead
            try:
                _, stdout, stderr = proc.communicate_finish(task)
                img_src = re.search(
                    r'<img[^>]+src="([^"]+)"', stdout.get_data().decode("utf8")
                ).group(1)
                Gio.File.new_for_uri(img_src).read_async(
                    GLib.PRIORITY_DEFAULT, None, on_file_read, None
                )

            except Exception as _:
                logger.error(f"[CLIPBOARD] Failed to decode html image for id: {id}")

        self.cliphist_decode(id, decode_callback)

    def parse_string(self, id: str):
        decoded_string = ""

        def on_pixbuf_ready(results):
            nonlocal decoded_string
            try:
                _, pbuf = results
                self._decoded_clipboard_history[id] = pbuf
                self.emit("clipboard-data-ready", id)
            except Exception as _:
                self._decoded_clipboard_history[id] = decoded_string
                self.emit("clipboard-data-ready", id)
                logger.error(f"[CLIPBOARD] Failed to read pixbuf for: {decoded_string}")

        def callback(proc: Gio.Subprocess, task: Gio.Task):
            nonlocal decoded_string
            try:
                _, stdout, stderr = proc.communicate_finish(task)
                decoded_string = str(stdout.get_data().decode("utf-8"))
                if decoded_string.startswith("file://"):
                    decoded_string = decoded_string[7:]

                # TODO: find alternative for magic
                stdout_contents_detect = magic.detect_from_content(stdout.get_data())
                if (
                    stdout_contents_detect.mime_type in SUPPORTED_MIME_TYPES
                    or "xbm image" in stdout_contents_detect.name
                ):
                    get_pixbuf_for_data_threaded(stdout.get_data(), on_pixbuf_ready)
                    return

                elif not os.path.exists(decoded_string):
                    self._decoded_clipboard_history[id] = decoded_string[
                        : self._length_cutoff
                    ]
                    self.emit("clipboard-data-ready", id)
                    return

                f = Gio.file_new_for_path(decoded_string)
                info = f.query_info(
                    "thumbnail::*,standard::size,standard::content-type",
                    Gio.FileQueryInfoFlags.NONE,
                    None,
                )  # type: ignore

                if info.get_attribute_boolean("thumbnail::is-valid-large"):
                    get_pixbuf_for_file_threaded(
                        info.get_attribute_as_string("thumbnail::path-large"),
                        on_pixbuf_ready,
                    )
                    return
                elif info.get_attribute_boolean("thumbnail::is-valid"):
                    get_pixbuf_for_file_threaded(
                        info.get_attribute_as_string("thumbnail::path"), on_pixbuf_ready
                    )
                    return
                # 5MB limit
                if info.get_size() > self._file_max_size:
                    return

                # FIXME: python 3.13 introduced a new function guess_file_type, use that
                # FIXME: using magic, you can detect xbm files but idc, one less depend
                # detected_filename = magic.detect_from_filename(decoded_string)
                file_type = info.get_content_type()
                if file_type in SUPPORTED_MIME_TYPES:
                    get_pixbuf_for_file_threaded(decoded_string, on_pixbuf_ready)
                else:
                    self._decoded_clipboard_history[id] = decoded_string
                    self.emit("clipboard-data-ready", id)

            except Exception as e:
                print(e)

        self.cliphist_decode(id, callback)

    def decode_clipboard(self):
        pattern = re.compile(r"\[\[ binary data .* \]\]")
        for cliphist_id in self._clipboard_history:
            preview: str = self._clipboard_history[cliphist_id]

            if pattern.match(preview):
                self.parse_data_binary(cliphist_id)
            elif preview.startswith("<meta"):
                self.parse_html_tag(cliphist_id)
            else:
                self.parse_string(cliphist_id)

    @Property(dict, "readable")
    def clipboard_history(self) -> dict:
        return self._clipboard_history

    @Property(dict, "readable")
    def decoded_clipboard_history(self) -> dict:
        return self._decoded_clipboard_history
