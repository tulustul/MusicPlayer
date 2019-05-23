import logging
import curses

from ui.colors import colors

from .abstract_component import AbstractComponent
from ..rect import Rect

logger = logging.getLogger("ui")


class Component(AbstractComponent):
    def __init__(self, context=None, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        self.color = colors["normal"]
        self.context = context

    def mark_for_redraw(self):
        if self.renderer:
            self.renderer.schedule_component_redraw(self)

    def draw(self):
        if self.win:
            self.win.bkgd(" ", self.color)
            self.draw_content()
            self.win.refresh()

    def draw_content(self):
        raise NotImplementedError

    def draw_text(self, text: str, y: int, x: int, length: int, *args):
        if len(text) > length:
            text = text[: length - 1] + "…"
        else:
            text = text + " " * (length - len(text))

        # curses disallow to render bottom right corner of a window using
        # addstr. We strip the last value and render it using insch.
        # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
        if y == self.rect.height - 1 and x + len(text) == self.rect.width:
            last_char = text[-1]
            text = text[:-1]
            try:
                self.win.insch(
                    self.rect.height - 1, self.rect.width - 1, last_char, *args
                )
            except OverflowError:
                # The error is raised when dealing with unicode characters.
                # Just ignore for now.
                pass

        self.win.addstr(y, x, text, *args)

    def set_rect(self, rect: Rect):
        super().set_rect(rect)
        self.win = curses.newwin(rect.height, rect.width, rect.y, rect.x)
        self.mark_for_redraw()
