import logging

logger = logging.getLogger('stream')

streams: dict = {}


def register(name, stream):
    if name not in streams:
        streams[name] = stream
    else:
        logger.error('Stream "{}" is already registered'.format(name))


def get(name):
    return streams[name]
