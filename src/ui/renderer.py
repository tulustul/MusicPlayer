import logging
from typing import Set

logger = logging.getLogger('ui.renderer')


class Renderer:

    def __init__(self):
        self._layouts_to_update = set()
        self._components_to_draw = set()

    def update(self):
        while self._layouts_to_update:
            layout = self._layouts_to_update.pop()
            self._layouts_to_update -= layout.update_layout()

        while self._components_to_draw:
            self._components_to_draw.pop().draw()

    def schedule_layout_update(self, layout):
        self._layouts_to_update.add(layout)

    def schedule_component_redraw(self, component):
        self._components_to_draw.add(component)
