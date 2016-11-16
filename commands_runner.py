import sys
import traceback
import logging

from commands import registry
from errors import errors

logger = logging.getLogger('commands_runner')


def run_text_command(text_command):
    tokens = text_command.split()
    command_name = tokens[0]
    args = tokens[1:]

    command = registry.get_by_name(command_name)
    if command:
        run_command(command, *args)
    else:
        logger.warn('Unknown command: {}'.format(command_name))


def run_command(command, *args):
    logger.debug('invoking command: {}'.format(command.name))
    try:
        command.func(*args)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(''.join(traceback.format_exception(
            exc_type, exc_value, exc_traceback,
        )))
        errors.on_next(str(e))
