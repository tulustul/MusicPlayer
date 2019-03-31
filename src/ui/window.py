import os
import asyncio
import curses
import logging
import typing

from core import keyboard
from core.config import config

from . import colors
from .renderer import Renderer
from .components.component import Component
from .components.layout import Layout
from .components.input import InputComponent

logger = logging.getLogger('ui')

os.environ.setdefault('ESCDELAY', '25')


class Window:

    def __init__(self):
        self.views = {}

        self.views_activity = []

        self.current_view: Optional[Component] = None

        self.screen = None

        self.create()

        colors.init()

        self.root_component = Layout()
        self.root_component.set_size(0, 0, curses.COLS, curses.LINES)

        self.input_component: InputComponent = None

        self.renderer = Renderer(self.screen, self.root_component)

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

    def input(self):
        # if not self.input_component:
        #     return

        self.input_component.mark_for_redraw()
        self.input_component.visible = True
        # self.input_mode = True

        # yield '-'


    # def refresh(self):
    #     if self.renderer:
    #         self.renderer.redraw()

    # def open_view_in(self, view, container_id):
    #     container = self.root_component.get_by_id(container_id)
    #     self.current_view = view
    #     if view not in container.childs:
    #         container.add(view)

    # def remove_view_from(self, view, container_id):
    #     container = self.root_component.get_by_id(container_id)
    #     if view in container.childs:
    #         container.remove(view)
