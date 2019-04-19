import asyncio
import curses
from curses import ascii
import logging
from typing import Optional

from rx.subjects import Subject

from core.keyboard import raw_keys

from .component import Component
from ..colors import colors

logger = logging.getLogger('ui')


class InputComponent(Component):

    def __init__(self):
        super().__init__()

        self.value = Subject()

        self.reset()

        raw_keys.subscribe(self.handle_key)

        self.selected_color = colors['selected']
        self.prompt_color = colors['prompt']

        self.future: Optional[asyncio.Future] = None

        self.prompt = ''

    def reset(self):
        self.set_value('')
        self.cursor = len(self.text) - 1

    def draw_content(self):
        offset = len(self.prompt) + 1

        self.win.addstr(0, 0, self.prompt, self.prompt_color)
        self.win.addstr(0, offset, ''.join(self.text[:self.cursor]))

        offset += self.cursor

        self.win.addstr(0, offset, self.text[self.cursor], self.selected_color)
        self.win.addstr(0, offset + 1, ''.join(self.text[self.cursor + 1:]))

    def handle_key(self, key):
        if not self.future:
            return

        if key == curses.KEY_BACKSPACE:
            target = self.cursor - 1
            if target >= 0:
                self.text.pop(target)
                self.cursor = target
                self.value.on_next(self.text_value)
        elif key == curses.KEY_DC:
            if self.cursor + 1 < len(self.text):
                self.text.pop(self.cursor)
        elif key == curses.KEY_LEFT:
            self.cursor = max(self.cursor - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor = min(self.cursor + 1, len(self.text) - 1)
        elif key in (curses.KEY_UP, curses.KEY_DOWN):
            pass  # ignore
        elif key == curses.KEY_HOME:
            self.cursor = 0
        elif key == curses.KEY_END:
            self.cursor = len(self.text) - 1
        elif key in (ascii.ESC, curses.KEY_EXIT):
            self.finish(None)
        elif key in (ascii.LF, ascii.NL):
            self.finish(self.text_value)
        else:
            key = chr(key)
            if isinstance(key, str):
                self.text.insert(self.cursor, key)
                self.cursor += 1
                self.value.on_next(self.text_value)

        self.mark_for_redraw()

    def finish(self, value: Optional[str]):
        if self.future:
            self.visible = False
            self.future.set_result(value)
            self.future = None

    @property
    def text_value(self):
        return ''.join(self.text[:-1])

    def set_value(self, value):
        self.text = list(value + ' ')
        self.cursor = len(self.text) - 1
        self.value.on_next(self.text_value)
        if self.win:
            self.mark_for_redraw()

    def request_value(self, prompt: str):
        self.prompt = prompt
        self.set_value('')
        self.future = asyncio.get_event_loop().create_future()
        self.mark_for_redraw()
        self.visible = True
        return self.future
