from functools import wraps, partial
import time
import logging as log


def time_it(func=None, *, arg1=None, arg2=None):
    """Print the runtime of the decorated function"""
    if func is None:
        return partial(time_it, arg1=arg1, arg2=arg2)

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        log.info(f'Finished {func.__name__!r} in {run_time:.4f} secs')
        return value

    return wrapper_timer()
