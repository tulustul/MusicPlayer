import curses
import logging

from rx.subjects import Subject

from core.keyboard import raw_keys

from .component import Component
from ..colors import colors

logger = logging.getLogger('ui')


class InputComponent(Component):

    def __init__(self):
        super().__init__()
        self.reset()

        raw_keys.subscribe(self.handle_key)

        self.value = Subject()

        self.commit = Subject()

        self.set_value('scan_local_files /run/media/disk/Muzyka')
        # self.set_value('scan_local_files /mnt/toshiba/Filmy')

        self.selected_color = colors['selected']

    def reset(self):
        self.text = [' ']
        self.cursor = len(self.text) - 1

    def draw_content(self):
        self.win.addstr(
            0, 0, ''.join(self.text[:self.cursor])
        )
        self.win.addstr(
            0, self.cursor, self.text[self.cursor], self.selected_color
        )
        self.win.addstr(
            0, self.cursor + 1, ''.join(self.text[self.cursor + 1:])
        )

    def handle_key(self, key):
        logger.info(key)
        if not self.win:
            return

        if key == '\n':
            self.commit.on_next(self.text_value)
            # self.reset()
        elif key == curses.KEY_BACKSPACE:
            target = self.cursor - 1
            if target >= 0:
                self.text.pop(target)
                self.cursor = target
        elif key == curses.KEY_DC:
            if self.cursor + 1 < len(self.text):
                self.text.pop(self.cursor)
        elif key == curses.KEY_LEFT:
            self.cursor = max(self.cursor - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor = min(self.cursor + 1, len(self.text) - 1)
        elif key == curses.KEY_HOME:
            self.cursor = 0
        elif key == curses.KEY_END:
            self.cursor = len(self.text) - 1
        else:
            key = chr(key)
            if isinstance(key, str):
                self.text.insert(self.cursor, key)
                self.cursor += 1

        # self.win.clear()
        self.mark_for_redraw()

        self.value.on_next(self.text_value)

        logger.info(self.text_value)

    @property
    def text_value(self):
        return ''.join(self.text[:-1])

    def set_value(self, value):
        self.text = list(value + ' ')
        self.cursor = len(self.text) - 1
        if self.win:
            self.mark_for_redraw()
