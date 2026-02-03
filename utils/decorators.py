from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from gi.repository import GLib

# Create a shared thread pool
thread_pool = ThreadPoolExecutor(max_workers=4)


def thread(target: Callable, *args, **kwargs):
    """
    Submit the given function to the thread pool.
    Returns a Future instead of a Thread.
    """
    return thread_pool.submit(target, *args, **kwargs)


def run_in_thread(func: Callable) -> Callable:
    """
    Decorator to run the decorated function in the thread pool.
    """

    def wrapper(*args, **kwargs):
        return thread(func, *args, **kwargs)

    return wrapper


def debounce(ms: int):
    """
    Debounce a function.
    Useful for preventing UI flickering during fast typing.
    """

    def decorator(func: Callable):
        timer_id_attr = f"_debounce_timer_{func.__name__}"

        def wrapper(self, *args, **kwargs):
            if existing_timer := getattr(self, timer_id_attr, None):
                GLib.source_remove(existing_timer)

            def timeout_cb():
                setattr(self, timer_id_attr, 0)
                func(self, *args, **kwargs)
                return False

            setattr(self, timer_id_attr, GLib.timeout_add(ms, timeout_cb))

        return wrapper
