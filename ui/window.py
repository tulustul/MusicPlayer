import asyncio
import curses
import logging

from . import colors
from .errors import Errors
from .bar import Bar
from .welcome_view import WelcomeView
# from .layout import Layout
from .palette import Palette
from .playlist import Playlist
from .toolkit.renderer import Renderer
from .toolkit.layout import Layout
from config import config
from errors import errors
import keyboard
import context

logger = logging.getLogger('ui')


class Window:

    def __init__(self):
        context.register('playlist')

        self.views = {}

        self.views_activity = []

        self.current_view = 'playlist'

        self.screen = None

        self.create()

        colors.init()

        self.init_views()

        main_component = Layout.make_from_config(config['layout'])
        self.renderer = Renderer(self.screen, main_component)

        # self.sidebar = main_component.get_by_id('sidebar')
        self.mainview = main_component.get_by_id('mainview')
        self.palette = main_component.get_by_id('palette')

        self.palette.visible = False

        # self.sidebar.add(WelcomeView())
        self.mainview.add(self.views['playlist'])

        # errors.subscribe(lambda e: self.show_view('errors'))

        self.input_mode = False

        self.running = True

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
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        self.screen.keypad(0)
        self.screen.nodelay(0)
        curses.endwin()

    def init_views(self):
        self.views = {
            'playlist': Playlist(),
            'palette': Palette(),
            # 'errors': Errors(),
        }

    async def process_input(self):
        interval = config.get('input_interval', 0.02)
        self.renderer.redraw()
        while self.running:
            self.renderer.update()
            await asyncio.sleep(interval)
            ch = 0
            while ch != -1:
                try:
                    if self.input_mode:
                        ch = self.screen.get_wch()
                    else:
                        ch = self.screen.getch()
                    if ch != -1:
                        keyboard.raw_keys.on_next(ch)
                except curses.error as e:
                    logger.error(e)
                except KeyboardInterrupt:
                    self.hide_view(self.current_view)

    def get_focused_view(self):
        return self.views[self.current_view]

    def show_view(self, view):
        widget = self.views[view]
        # self.layout.add(widget)
        self.views_activity.append(self.current_view)
        self.current_view = view

    def hide_view(self, view):
        widget = self.views[view]
        if self.views_activity:
            # self.layout.remove(widget)
            self.current_view = self.views_activity.pop()

    def hide_current_view(self):
        self.hide_view(self.current_view)

    def quit(self):
        self.running = False

    def refresh(self):
        self.renderer.redraw()
