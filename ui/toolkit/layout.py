import logging
from enum import Enum

from .component import AbstractComponent, class_registry
from errors import errors

logger = logging.getLogger(name='ui')


class Layout(AbstractComponent):

    class Direction(Enum):
        horizontal = 1
        vertical = 2

    def __init__(self):
        super().__init__()
        self.childs = []
        self.direction = Layout.Direction.horizontal

    @classmethod
    def make_from_config(cls, config):
        layout = super().make_from_config(config)
        layout.direction = Layout.Direction[
            config.get('direction', 'vertical')
        ]
        for child in config.get('components', []):
            component_class = class_registry[child['class']]
            if not component_class:
                errors.on_next(
                    'unknown component class: {}'.format(component_class)
                )
                return
            layout.add(component_class.make_from_config(child))
        return layout

    def refresh(self):
        super().refresh()
        self.calculate_sizes()

    def add(self, component):
        self.childs.append(component)
        component.parent = self
        self.calculate_sizes()
        self.refresh()

    def remove(self, component):
        self.childs.remove(component)
        component.parent = None
        self.calculate_sizes()
        self.refresh()

    def clear(self):
        for child in self.childs:
            child.parent = None
        self.childs = []
        self.refresh()

    def calculate_sizes(self):
        if not self.lines or not self.cols:
            return

        if self.direction == Layout.Direction.horizontal:
            vertical = False
            total_size = self.cols
        elif self.direction == Layout.Direction.vertical:
            vertical = True
            total_size = self.lines
        else:
            logger.error('Unknown layout type: {}'.format(self.direction))

        current_offset = 0

        fluent_size = total_size - sum(
            component.desired_size for component in self.visible_childs
            if component.desired_size
        )

        for component in self.visible_childs:
            size = component.desired_size or max(fluent_size, 0)

            if vertical:
                component.set_size(0, current_offset, self.cols, size)
            else:
                component.set_size(current_offset, 0, size, self.lines)

            current_offset += size

        for child_layout in self.child_layouts:
            child_layout.calculate_sizes()

    @property
    def visible_childs(self):
        return (child for child in self.childs if child.visible)

    @property
    def child_layouts(self):
        yield from (
            child for child in self.childs
            if isinstance(child, Layout)
        )

    def draw(self):
        for child in self.visible_childs:
            child.draw()

    def get_by_id(self, component_id):
        result = None
        if self.id == component_id:
            result = self
        else:
            for component in self.childs:
                if component.id == component_id:
                    result = component
                elif isinstance(component, Layout):
                    result = component.get_by_id(component_id)
                if result:
                    break
        return result
