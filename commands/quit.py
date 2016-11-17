import logging

from .decorator import command
import ui

logger = logging.getLogger('commands')


@command()
def quit():
    ui.win.quit()
