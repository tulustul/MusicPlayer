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

        self.visible = True
        self.desired_size = 0

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
        logger.debug(
            '{} draw x:{} y:{} lines:{} cols:{}'
            .format(self, self.x, self.y, self.lines, self.cols)
        )
        self.win.clear()
        self.win.bkgd(' ', self.color)
        self.draw_content()
        self.win.refresh()

    def draw_content(self):
        raise NotImplementedError

    def set_size(self, *args):
        super().set_size(*args)
        self.win = curses.newwin(self.lines, self.cols, self.y, self.x)
