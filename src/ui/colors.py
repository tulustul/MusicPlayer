import logging
import curses

from core.config import theme

logger = logging.getLogger('colors')

colors = {}


def init():
    color_definitions = theme['colors']
    for i, color_name in enumerate(color_definitions.keys()):
        foreground, background = color_definitions[color_name]
        curses.init_pair(i + 1, foreground, background)
        colors[color_name] = curses.color_pair(i + 1)
