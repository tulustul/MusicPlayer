from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import logging
from typing import List, Tuple

from core.errors import errors
from .component import AbstractComponent, class_registry
import ui

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
        self.mark_for_redraw()
        self.calculate_sizes()

    def add(self, component: AbstractComponent):
        self.childs.append(component)
        component.parent = self
        self.calculate_sizes()
        # self.refresh()
        # ui.win.refresh()

    def remove(self, component: AbstractComponent):
        self.childs.remove(component)
        component.parent = None
        self.calculate_sizes()
        # self.refresh()
        # ui.win.refresh()

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

        visible_childs = self.get_visible_childs()

        fluent_childs = [c for c in visible_childs if not c.desired_size]

        fluent_size = total_size - sum(
            component.desired_size for component in visible_childs
            if component.desired_size
        )

        current_offset = Decimal(0)

        for component in visible_childs:
            decimal_size = Decimal(
                component.desired_size or
                max(fluent_size / len(fluent_childs), 0)
            )
            offset = int(current_offset.to_integral_value(ROUND_HALF_UP))
            size = int(decimal_size.to_integral_value(ROUND_HALF_UP))

            current_offset += decimal_size

            size += int(
                current_offset.to_integral_value(ROUND_HALF_UP)
            ) - offset - size

            if vertical:
                component.set_size(self.x, self.y + offset, self.cols, size)
            else:
                component.set_size(self.x + offset, self.y, size, self.lines)

        for child_layout in self.child_layouts:
            child_layout.calculate_sizes()

    def get_visible_childs(self):
        return [child for child in self.childs if child.visible]

    @property
    def child_layouts(self):
        yield from (
            child for child in self.childs
            if isinstance(child, Layout)
        )

    def draw(self):
        for child in self.get_visible_childs():
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

    @property
    def visible(self):
        return self._visible and list(self.get_visible_childs())

    @visible.setter
    def visible(self, visible):
        self._visible = visible

    @property
    def desired_size(self):
        childs_desired_size = sum(
            c.desired_size or self._desired_size
            for c in self.get_visible_childs()
        )
        return min(self._desired_size, childs_desired_size)

    @desired_size.setter
    def desired_size(self, desired_size):
        self._desired_size = desired_size
