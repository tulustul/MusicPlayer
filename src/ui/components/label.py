import logging

from .component import Component

logger = logging.getLogger(name='ui')


class LabelComponent(Component):

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.mark_for_redraw()

    def draw_content(self):
        message = self.text[:self.cols]

        y = int((self.cols - len(message)) / 2)
        x = int(self.lines / 2)
        self.win.addstr(x, y, message)
