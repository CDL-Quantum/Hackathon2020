from dataclasses import dataclass
from enum import Enum, auto


class Orientation(Enum):
    Horizontal = auto()
    Vertical = auto()


@dataclass
class Component:
    height: int
    width: int
    orientation: Orientation = Orientation.Horizontal
    x: int = 0
    y: int = 0

    @property
    def rotated_dimensions(self):
        if self.orientation is Orientation.Horizontal:
            return self.width, self.height
        else:
            return self.height, self.width
