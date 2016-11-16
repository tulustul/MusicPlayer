import logging

from .decorator import command

logger = logging.getLogger('commands')


@command()
def search():
    logger.debug('search triggered')


@command()
def commit_search():
    logger.debug('commit search')


@command()
def cancel_search():
    logger.debug('cancel search')
