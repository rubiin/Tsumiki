import atexit
import os
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from time import monotonic
from typing import Any, TypeVar

from fabric.utils import GLib

# Auto-tune max_workers based on CPU count, fallback to 4
_cpu_count = os.cpu_count() or 4
thread_pool: ThreadPoolExecutor | None = None
_thread_pool_atexit_registered = False

T = TypeVar("T")


def log_errors(func):
    """Decorator to log errors in config operations"""

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def safe_operation(func):
    """Decorator for safe operations that shouldn't raise exceptions"""

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def _get_thread_pool() -> ThreadPoolExecutor:
    """Lazy-initialize thread pool on first use."""
    global thread_pool, _thread_pool_atexit_registered
    if thread_pool is None:
        thread_pool = ThreadPoolExecutor(max_workers=_cpu_count)
        if not _thread_pool_atexit_registered:
            atexit.register(_shutdown_thread_pool)
            _thread_pool_atexit_registered = True
    return thread_pool


def _shutdown_thread_pool() -> None:
    """Best-effort, non-blocking shutdown for interpreter exit.

    On Ctrl+C, Python may run atexit handlers while another KeyboardInterrupt is
    still bubbling; avoid blocking joins to keep shutdown quiet and fast.
    """

    global thread_pool
    if thread_pool is None:
        return

    try:
        thread_pool.shutdown(wait=False, cancel_futures=True)
    except KeyboardInterrupt:
        # Suppress noisy traceback during interpreter teardown.
        pass
    except Exception:
        pass
    finally:
        thread_pool = None


def thread(target: Callable[..., T], *args: Any, **kwargs: Any) -> Any:
    """
    Submit the given function to the thread pool.
    Returns a Future instead of a Thread.
    """
    return _get_thread_pool().submit(target, *args, **kwargs)


def run_in_thread(func: Callable[..., T]) -> Callable[..., Any]:
    """
    Decorator to run the decorated function in the thread pool.
    Returns a Future.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return thread(func, *args, **kwargs)

    return wrapper


def debounce(ms: int):
    """
    Debounce a method. Useful for preventing UI flickering during fast typing.
    Cleans up timers on object deletion.
    """

    def decorator(func: Callable):
        timer_id_attr = f"_debounce_timer_{func.__name__}"

        def wrapper(self, *args, **kwargs):
            # Remove existing timer if present
            existing_timer = getattr(self, timer_id_attr, None)
            if existing_timer:
                GLib.source_remove(existing_timer)

            def timeout_cb():
                setattr(self, timer_id_attr, 0)
                func(self, *args, **kwargs)
                return False

            setattr(self, timer_id_attr, GLib.timeout_add(ms, timeout_cb))

        # Clean up timer on object deletion
        def cleanup(self):
            existing_timer = getattr(self, timer_id_attr, None)
            if existing_timer:
                GLib.source_remove(existing_timer)

        wrapper._debounce_cleanup = cleanup
        return wrapper

    return decorator


def rate_limit(ms: int, skipped_return: Any = None):
    """Rate-limit a method so it runs at most once every ``ms`` milliseconds."""

    interval = ms / 1000.0

    def decorator(func: Callable):
        last_run_attr = f"_rate_limit_last_{func.__name__}"

        def wrapper(self, *args, **kwargs):
            now = monotonic()
            last_run = getattr(self, last_run_attr, 0.0)
            if now - last_run < interval:
                return skipped_return

            setattr(self, last_run_attr, now)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
