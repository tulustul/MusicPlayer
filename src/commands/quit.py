import logging

from .decorator import command

from ui.window import Window

logger = logging.getLogger('commands')


@command()
def quit(window: Window):
    window.quit()
