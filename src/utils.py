import math


def format_seconds(seconds):
    seconds = int(seconds or 0)

    hours = math.floor(seconds / 3600)
    seconds -= hours * 3600

    minutes = math.floor(seconds / 60)
    seconds -= minutes * 60

    formatted = '{}:{}'.format(minutes, str(seconds).zfill(2))
    if hours:
        formatted = '{}:{}'.format(hours, minutes)

    return formatted
