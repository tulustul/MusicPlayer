import logging
import curses

from ui.colors import colors

logger = logging.getLogger('ui.toolkit')

class_registry = {}


class ComponentMeta(type):

    def __init__(cls, name, bases, dct):
        class_registry[name] = cls


class AbstractComponent(metaclass=ComponentMeta):

    def __init__(self):
        self.id = None

        self.redraw_requested = False

        self.x = 0
        self.y = 0
        self.lines = 0
        self.cols = 0

        self._visible = True
        self._desired_size = 0

        self.parent = None

    @classmethod
    def make_from_config(cls, config):
        component = cls()
        component.id = config.get('id')
        component.desired_size = config.get('desired_size', 0)
        return component

    def refresh(self):
        self.redraw_requested = True

    def draw(self):
        raise NotImplementedError

    def set_size(self, x, y, cols, lines):
        self.x = x
        self.y = y
        self.lines = lines
        self.cols = cols

    def __str__(self):
        return '<{}> {}'.format(self.__class__.__name__, self.id)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible

    @property
    def desired_size(self):
        return self._desired_size

    @desired_size.setter
    def desired_size(self, desired_size):
        self._desired_size = desired_size


class Component(AbstractComponent):

    def __init__(self):
        super().__init__()
        self.win = None
        self.color = colors['normal']

    @classmethod
    def make_from_config(cls, config):
        component = super().make_from_config(config)
        component.color = colors[config.get('color')]
        return component

    def draw(self):
        self.win.bkgd(' ', self.color)
        self.draw_content()
        self.win.refresh()

    def draw_content(self):
        raise NotImplementedError

    def draw_text(self, text, x, y, length, *args):
        if len(text) > length:
            text = text[:length - 1] + '…'
        else:
            text = text + ' ' * (length - len(text))
        self.win.addstr(y, x, text, *args)

    def set_size(self, *args):
        super().set_size(*args)
        self.win = curses.newwin(self.lines, self.cols, self.y, self.x)
