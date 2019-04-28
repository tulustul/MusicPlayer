from typing import Optional

from ..rect import Rect
from ..renderer import Renderer


class AbstractComponent:

    def __init__(self, desired_size: int = 0):
        self.id = None

        self.rect = Rect(0, 0, 0, 0)

        self._visible = True
        self._desired_size = desired_size

        self.renderer: Optional[Renderer] = None

        self.parent: Optional[AbstractComponent] = None

    def mark_for_redraw(self):
        pass

    def draw(self):
        raise NotImplementedError

    def set_rect(self, rect: Rect):
        self.rect = rect

    @property
    def desired_size(self):
        return self._desired_size

    @desired_size.setter
    def desired_size(self, desired_size):
        self._desired_size = desired_size

    def detach(self):
        if self.parent:
            self.parent.remove(self)
