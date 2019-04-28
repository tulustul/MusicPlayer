import asyncio
import curses
import logging
from typing import Dict, Optional, List
import os

from core import keyboard
from core.config import config

from . import colors
from .renderer import Renderer
from .components.component import Component
from .components.layout import Layout
from .components.input import InputComponent
from .components.label import LabelComponent
from .rect import Rect

logger = logging.getLogger('ui.window')

os.environ.setdefault('ESCDELAY', '25')


class Window:

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

        self.components: Dict[object, Component] = {}

        self.active_component_stack: List[Component] = []

        self.screen = None

        self.create()

        colors.init()

        self.renderer = Renderer()

        self.root_component = Layout()
        self.root_component.renderer = self.renderer
        self.root_component.set_rect(Rect(0, 0, curses.COLS, curses.LINES))

        self.input_component: Optional[InputComponent] = None
        self.input_container: Optional[Layout] = None

        self.notifications_layout: Optional[Layout] = None

        self.input_mode = False

        self.running = True

    def create(self):
        self.screen = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.screen.nodelay(1)

        try:
            curses.start_color()
        except:
            pass

        self.screen.refresh()

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
                    ch = self.screen.getch()
                    if ch != -1:
                        keyboard.raw_keys.on_next(ch)
                except curses.error as e:
                    logger.error(e)
                except KeyboardInterrupt:
                    self.hide_view(self.active_component)

    def get_component(self, component_class: type):
        return self.root_component.get_component(component_class)

    def focus(self, component: Component):
        self.active_component_stack.append(component)

    def blur_active_component(self):
        self.active_component_stack.pop()

    @property
    def active_component(self):
        if self.active_component_stack:
            return self.active_component_stack[-1]
        return None

    def quit(self):
        self.running = False

    async def input(self, prompt: str):
        if not self.input_container:
            return

        self.input_component = InputComponent()
        self.input_container.add(self.input_component)

        self.input_mode = True
        result = await self.input_component.request_value(prompt)
        self.input_component.detach()
        self.input_component = None
        self.input_mode = False
        return result

    def add_notification(self, component: Component):
        if self.notifications_layout:
            self.notifications_layout.add(component)
            self.root_component.update_layout()

    def show_error(self, text: str):
        error_component = LabelComponent(
            text,
            align=LabelComponent.Align.left,
            color=colors.colors['error'],
            context='error',
        )
        self.add_notification(error_component)
        self.focus(error_component)
