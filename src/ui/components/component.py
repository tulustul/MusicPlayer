import logging
import curses
from typing import Optional

from ui.colors import colors

from ..rect import Rect
from ..renderer import Renderer

logger = logging.getLogger('ui')

class_registry = {}


class ComponentMeta(type):

    def __init__(cls, name, bases, dct):
        class_registry[name] = cls


class AbstractComponent(metaclass=ComponentMeta):

    def __init__(self):
        self.id = None

        self.rect = Rect(0, 0, 0, 0)

        self._visible = True
        self._desired_size = 0

        self.parent = None

        self.renderer: Optional[Renderer] = None

    def mark_for_redraw(self):
        pass

    def draw(self):
        raise NotImplementedError

    def set_rect(self, rect: Rect):
        self.rect = rect

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible
        if self.parent:
            self.parent.update_layout()

    @property
    def desired_size(self):
        return self._desired_size

    @desired_size.setter
    def desired_size(self, desired_size):
        self._desired_size = desired_size

    def detach(self):
        if self.parent:
            self.parent.remove(self)


class Component(AbstractComponent):

    def __init__(self, context=None):
        super().__init__()
        self.win = None
        self.color = colors['normal']
        self.context = context

    def mark_for_redraw(self):
        if self.renderer:
            self.renderer.schedule_component_redraw(self)

    def draw(self):
        if self.win:
            self.win.bkgd(' ', self.color)
            self.draw_content()
            self.win.refresh()

    def draw_content(self):
        raise NotImplementedError

    def draw_text(self, text: str, y: int, x: int, length: int, *args):
        if len(text) > length:
            text = text[:length - 1] + '…'
        else:
            text = text + ' ' * (length - len(text))

        # curses disallow to render bottom right corner of a window using
        # addstr. We strip the last value and render it using insch.
        # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
        if y == self.rect.height - 1 and x + len(text) == self.rect.width:
            last_char = text[-1]
            text = text[:-1]
            self.win.insch(
                self.rect.height - 1, self.rect.width - 1, last_char, *args,
            )

        self.win.addstr(y, x, text, *args)

    def set_rect(self, rect: Rect):
        super().set_rect(rect)
        self.win = curses.newwin(rect.height, rect.width, rect.y, rect.x)
        self.mark_for_redraw()
