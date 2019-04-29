from typing import Optional

from ..rect import Rect
from ..renderer import Renderer


class AbstractComponent:

    def __init__(self, size: Optional[int] = None):
        self.id = None

        self.rect = Rect(0, 0, 0, 0)

        self._visible = True
        self._size = size

        self.renderer: Optional[Renderer] = None

        self.parent: Optional[AbstractComponent] = None

    def mark_for_redraw(self):
        pass

    def draw(self):
        raise NotImplementedError

    def set_rect(self, rect: Rect):
        self.rect = rect

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    def detach(self):
        if self.parent:
            self.parent.remove(self)
