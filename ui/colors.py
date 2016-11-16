import curses

_NORMAL = 1
_SELECTED = 2
_ERROR = 3

NORMAL = None
SELECTED = None
ERROR = None


def init():
    global NORMAL
    global SELECTED
    global ERROR

    curses.init_pair(_NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(_SELECTED, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(_ERROR, curses.COLOR_WHITE, curses.COLOR_RED)

    NORMAL = curses.color_pair(_NORMAL)
    SELECTED = curses.color_pair(_SELECTED)
    ERROR = curses.color_pair(_ERROR)
