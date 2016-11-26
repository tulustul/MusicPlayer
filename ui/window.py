import asyncio
import curses
import logging

from . import colors
from .toolkit.renderer import Renderer
from .toolkit.layout import Layout
from config import config
import keyboard

logger = logging.getLogger('ui')


class Window:

    def __init__(self):
        self.views = {}

        self.views_activity = []

        self.current_view = None

        self.screen = None

        self.renderer = None

        self.create()

        colors.init()

    def initialize_view(self):

        self.main_component = Layout.make_from_config(config['layout'])
        self.renderer = Renderer(self.screen, self.main_component)

        # self.sidebar = self.main_component.get_by_id('sidebar')
        self.mainview = self.main_component.get_by_id('mainview')

        self.input_mode = False

        self.running = True

        self.refresh()

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

    async def process_input(self):
        interval = config.get('input_interval', 0.02)
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

    def quit(self):
        self.running = False

    def refresh(self):
        if self.renderer:
            self.renderer.redraw()

    def open_view_in(self, view, container_id):
        container = self.main_component.get_by_id(container_id)
        self.current_view = view
        if view not in container.childs:
            container.add(view)
