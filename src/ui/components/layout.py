from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import logging
from typing import List, Tuple, Optional, Set

from core.errors import errors
import ui

from .abstract_component import AbstractComponent
from ..rect import Rect

logger = logging.getLogger(name='ui')


class Layout(AbstractComponent):

    class Direction(Enum):
        horizontal = 1
        vertical = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.childs: List[AbstractComponent] = []
        self.direction = Layout.Direction.vertical

        self.old_desired_size = 0

    def mark_for_update(self):
        if self.renderer:
            self.renderer.schedule_layout_update(self)

    def add(self, component: AbstractComponent):
        self.childs.append(component)
        component.parent = self
        component.renderer = self.renderer
        if not isinstance(component, Layout):
            component.mark_for_redraw()
        self.mark_for_update()

    def remove(self, component: AbstractComponent):
        self.childs.remove(component)
        component.parent = None
        component.renderer = None
        self.mark_for_update()

    def clear(self):
        for child in self.childs:
            child.parent = None
        self.childs = []
        self.refresh()

    def update_layout(self) -> set:
        if self.rect.is_void:
            return set()

        updated_layouts = set([self])

        if self.old_desired_size != self.desired_size:
            self.old_desired_size = self.desired_size
            if self.parent and isinstance(self.parent, Layout):
                updated_layouts |= self.parent.update_layout()

        if self.direction == Layout.Direction.horizontal:
            vertical = False
            total_size = self.rect.width
        elif self.direction == Layout.Direction.vertical:
            vertical = True
            total_size = self.rect.height
        else:
            logger.error('Unknown layout type: {}'.format(self.direction))

        fluent_childs = [c for c in self.childs if not c.desired_size]

        fluent_size = total_size - sum(
            component.desired_size for component in self.childs
            if component.desired_size
        )

        current_offset = Decimal(0)

        for component in self.childs:
            component.mark_for_redraw()

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
                component.set_rect(Rect(
                    self.rect.x, self.rect.y + offset,
                    self.rect.width, size,
                ))
            else:
                component.set_rect(Rect(
                    self.rect.x + offset, self.rect.y,
                    size, self.rect.height,
                ))

        for child_layout in self.child_layouts:
            updated_layouts |= child_layout.update_layout()

        return updated_layouts

    @property
    def child_layouts(self):
        yield from (
            child for child in self.childs
            if isinstance(child, Layout)
        )

    def get_descendants(self):
        for component in self.childs:
            if isinstance(component, Layout):
                yield from component.get_descendants()
            else:
                yield component

    def get_component(self, component_class: type):
        for component in self.get_descendants():
            if isinstance(component, component_class):
                return component

    @property
    def visible(self):
        return bool(self._visible and self.childs)

    @visible.setter
    def visible(self, visible):
        self._visible = visible

    @property
    def desired_size(self):
        logger.error(self.childs)
        childs_desired_size = sum(
            c.desired_size or self._desired_size
            for c in self.childs
        )
        return min(self._desired_size, childs_desired_size)

    @desired_size.setter
    def desired_size(self, desired_size):
        self._desired_size = desired_size
