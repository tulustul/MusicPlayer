import logging

from .decorator import command
from core import context

logger = logging.getLogger('commands')


@command()
def pop_context():
    context.pop()
