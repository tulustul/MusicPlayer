from dataclasses import dataclass


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def is_void(self):
        return not (self.width and self.height)
