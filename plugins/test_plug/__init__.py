import logging

from . import submodule

logger = logging.getLogger('test')

REQUIRE = []

NAME = 'test plugisasdasq'


def init():
    logger.info(submodule.test())


def destroy():
    ...
