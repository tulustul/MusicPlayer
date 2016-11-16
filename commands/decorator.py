import logging

from . import registry

logger = logging.getLogger('commands')


def command(name=None, display_name=None, visible_in_palette=True):
    def decorator(func):
        nonlocal name, display_name
        if name is None:
            name = func.__name__
        if display_name is None:
            display_name = name
        logger.debug('registering command "{}"'.format(name))
        registry.register(func, name, display_name, visible_in_palette)
        return func
    return decorator
