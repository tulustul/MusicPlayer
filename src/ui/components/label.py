from enum import Enum
import logging

from .component import Component
from ..colors import colors

logger = logging.getLogger(name='ui.components.label')


class LabelComponent(Component):

    class Align(Enum):
        left = 1
        center = 2
        right = 3

    def __init__(self, text: str, align=Align.left, color=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.align = align
        self.color = color or colors['normal']

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.mark_for_redraw()

    def draw_content(self):
        message = self.text[:self.rect.width]

        y = int(self.rect.height / 2)

        if self.align == self.Align.left:
            x = 0
        elif self.align == self.Align.center:
            x = int((self.rect.width - len(message)) / 2)
        else:
            x = -len(message)

        self.win.addstr(y, x, message, self.color)
