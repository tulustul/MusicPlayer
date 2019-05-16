import curses
import logging

from ui.window import Window
from ui.rect import Rect

from .decorator import command

logger = logging.getLogger("commands.refresh")


@command()
def refresh(window: Window):
    if not window.screen:
        return

    y, x = window.screen.getmaxyx()
    resize = curses.is_term_resized(curses.LINES, curses.COLS)

    if resize is True:
        logger.debug(f"resizing to {y}x{x}")

        window.screen.clear()
        curses.resizeterm(y, x)
        window.screen.refresh()

        window.root_component.set_rect(Rect(0, 0, curses.COLS, curses.LINES))
        window.root_component.mark_for_update()
