import asyncio
import curses
import logging

from . import colors
from .errors import Errors
from .bar import Bar
from .layout import Layout
from .palette import Palette
from .playlist import Playlist
from config import config
from errors import errors
import keyboard

logger = logging.getLogger('ui')


class Window:

    def __init__(self):
        self.views = {}

        self.views_activity = []

        self.current_view = 'playlist'

        self.screen = None

        self.create()

        colors.init()

        self.init_views()

        self.layout = Layout(self.screen)

        self.layout.add(self.get_focused_view())
        self.layout.add(Bar())

        errors.subscribe(lambda e: self.show_view('errors'))

    def create(self):
        self.screen = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.screen.nodelay(True)

        try:
            curses.start_color()
        except:
            pass

    def destroy(self):
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(0)
        self.screen.nodelay(0)
        curses.endwin()

    def init_views(self):
        self.views = {
            'playlist': Playlist(),
            'palette': Palette(),
            'errors': Errors(),
        }

    async def process_input(self):
        interval = config.get('input_interval', 0.1)
        while True:
            await asyncio.sleep(interval)
            try:
                ch = self.screen.get_wch()
                if ch == 'q':
                    self.screen.refresh()
                    return
                if ch != -1:
                    keyboard.raw_keys.on_next(ch)
            except curses.error:
                pass
            except KeyboardInterrupt:
                self.hide_view(self.current_view)

    def get_focused_view(self):
        return self.views[self.current_view]

    def show_view(self, view):
        widget = self.views[view]
        self.layout.add(widget)
        self.views_activity.append(self.current_view)
        self.current_view = view

    def hide_view(self, view):
        widget = self.views[view]
        if self.views_activity:
            self.layout.remove(widget)
            self.current_view = self.views_activity.pop()

    def hide_current_view(self):
        self.hide_view(self.current_view)
