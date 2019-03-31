import logging

from commands.decorator import command
from ui.window import Window

logger = logging.getLogger('plugins.test')


@command()
def test_input(window: Window):
    text = window.input()
    logger.info(f'test_input: {text}')
