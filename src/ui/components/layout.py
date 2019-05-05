from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import logging
from typing import List, Tuple, Optional, Set

from core.errors import errors
from ui.renderer import Renderer

from .abstract_component import AbstractComponent
from ..rect import Rect

logger = logging.getLogger(name='ui')


class AbstractLayout(AbstractComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.childs: List[AbstractComponent] = []

    def update_layout(self) -> set:
        raise NotImplemented

    def mark_for_update(self):
        if self.renderer:
            self.renderer.schedule_layout_update(self)

    def set_renderer(self, renderer: Optional[Renderer]):
        super().set_renderer(renderer)
        for child in self.childs:
            child.set_renderer(renderer)

    @property
    def child_layouts(self):
        yield from (
            child for child in self.childs
            if isinstance(child, AbstractLayout)
        )

    def get_descendants(self):
        for component in self.childs:
            if isinstance(component, AbstractLayout):
                yield from component.get_descendants()
            else:
                yield component

    def get_component(self, component_class: type):
        for component in self.get_descendants():
            if isinstance(component, component_class):
                return component


class Layout(AbstractLayout):

    class Direction(Enum):
        horizontal = 1
        vertical = 2

    def __init__(self, direction=Direction.vertical, **kwargs):
        super().__init__(**kwargs)
        self.direction = direction
        self.old_size = 0

    def insert(self, index: int, component: AbstractComponent):
        self.childs.insert(index, component)
        self._on_new_child(component)

    # TODO rename to "append"
    def add(self, component: AbstractComponent):
        self.childs.append(component)
        self._on_new_child(component)

    def _on_new_child(self, component: AbstractComponent):
        component.parent = self
        component.set_renderer(self.renderer)
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

        if self.old_size != self.size:
            self.old_size = self.size
            if self.parent and isinstance(self.parent, AbstractLayout):
                updated_layouts |= self.parent.update_layout()

        if self.direction == Layout.Direction.horizontal:
            vertical = False
            total_size = self.rect.width
        elif self.direction == Layout.Direction.vertical:
            vertical = True
            total_size = self.rect.height
        else:
            logger.error('Unknown layout type: {}'.format(self.direction))

        fluent_childs = [c for c in self.childs if c.size is None]

        fluent_size = total_size - sum(
            component.size for component in self.childs
            if component.size
        )

        current_offset = Decimal(0)

        for component in self.childs:
            component.mark_for_redraw()

            decimal_size = Decimal(
                max(fluent_size / len(fluent_childs), 0)
                if component.size is None
                else component.size
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
    def size(self):
        have_fluent_childs = any(c.size is None for c in self.childs)
        if have_fluent_childs:
            return None

        return sum(c.size for c in self.childs if c.size)

    @size.setter
    def size(self, size):
        self._size = size
