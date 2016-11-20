import logging

from .layout import Layout

logger = logging.getLogger('ui.toolkit')


class Renderer:

    def __init__(self, screen, main_component):
        self.screen = screen
        self.main_component = main_component

    def redraw(self):
        self.screen.refresh()
        y, x = self.screen.getmaxyx()
        self.main_component.lines = y
        self.main_component.cols = x
        self.main_component.calculate_sizes()
        self.main_component.draw()

    def update(self):
        self.screen.refresh()
        for component in self.get_components_to_draw(self.main_component):
            component.draw()

    def get_components_to_draw(self, component):
        if component.redraw_requested:
            yield component
            component.redraw_requested = False
        elif isinstance(component, Layout):
            for child in component.childs:
                yield from self.get_components_to_draw(child)
