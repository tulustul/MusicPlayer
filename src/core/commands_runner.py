import asyncio
import sys
import traceback
import logging
import inspect

from commands.registry import Command, get_by_name

from .errors import errors
from .dependency_injection import Injector

logger = logging.getLogger('commands_runner')


class CommandsRunner:

    def __init__(self, loop: asyncio.AbstractEventLoop, injector: Injector):
        self.loop = loop
        self.injector = injector

    def run_text_command(self, text_command: str):
        tokens = text_command.split()
        command_name = tokens[0]
        args = tokens[1:]

        command = get_by_name(command_name)
        if command:
            self.run_command(command, args)
        else:
            logger.warn('Unknown command: {}'.format(command_name))

    def run_command(self, command: Command, *args):
        # logger.debug('invoking command: {} {}'.format(command.name, args))

        args_iterator = args.__iter__()

        kwargs = {}

        for param, annotation in command.func.__annotations__.items():
            if annotation not in (str, int, float, list, dict):
                kwargs[param] = self.injector.get(annotation)
            else:
                kwargs[param] = next(args_iterator)

        try:
            if inspect.iscoroutinefunction(command.func):
                self.loop.create_task(command.func(**kwargs))
            else:
                command.func(**kwargs)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(''.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback,
            )))
            errors.on_next(str(e))
