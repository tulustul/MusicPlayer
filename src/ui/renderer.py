import logging

from .components.layout import Layout

logger = logging.getLogger('ui.toolkit')


class Renderer:

    def __init__(self, screen, root_component):
        self.screen = screen
        self.root_component = root_component

    def redraw(self):
        y, x = self.screen.getmaxyx()
        self.root_component.lines = y
        self.root_component.cols = x
        self.root_component.calculate_sizes()
        self.root_component.draw()

    def update(self):
        self.screen.refresh()
        for component in self.get_components_to_draw(self.root_component):
            component.draw()

    def get_components_to_draw(self, component):
        if component.redraw_requested:
            yield component
            component.redraw_requested = False
        elif isinstance(component, Layout):
            for child in component.childs:
                yield from self.get_components_to_draw(child)
