import logging

from .decorator import command
import ui

logger = logging.getLogger('commands')


@command()
def hide_current_view():
    ui.win.hide_current_view()
