from functools import wraps
import logging
import math
import time
from typing import Callable

logger = logging.getLogger()


def format_seconds(seconds: int):
    seconds = int(seconds or 0)

    hours = math.floor(seconds / 3600)
    seconds -= hours * 3600

    minutes = math.floor(seconds / 60)
    seconds -= minutes * 60

    formatted = "{}:{}".format(minutes, str(seconds).zfill(2))
    if hours:
        formatted = "{}:{}".format(hours, minutes)

    return formatted


def format_bytes(bytes_count: int):
    B = float(bytes_count)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)


def async_log_time(coroutine: Callable):
    @wraps(coroutine)
    async def wrapper(*args, **kwargs):
        t0 = time.time()
        await coroutine(*args, **kwargs)
        t1 = time.time()
        logger.info('{} took {:.3f}s'.format(coroutine.__name__, t1 - t0))

    return wrapper
