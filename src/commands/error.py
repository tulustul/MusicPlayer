import logging

from .decorator import command

from ui.window import Window

logger = logging.getLogger('commands')


@command()
def dismiss_error(window: Window):
    if window.active_component:
        window.active_component.detach()
        window.blur_active_component()
