import logging

from .decorator import command
import context

logger = logging.getLogger('commands')


@command()
def pop_context():
    context.pop()
