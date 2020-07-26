from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from typing import List
from .Component import Component

DEFAULT_RECTANGLE_COLOR = [c / 256 for c in (136, 150, 142)]
DEFAULT_FLOOR_COLOR = [c / 256 for c in (236, 250, 242)]
DEFAULT_FLOOR_EDGE_COLOR = [c / 256 for c in (136, 150, 142)]


class FloorPlan:
    width: int = 15
    height: int = 10
    rectangle_color = DEFAULT_RECTANGLE_COLOR
    floor_color = DEFAULT_FLOOR_COLOR
    floor_edge_color = DEFAULT_FLOOR_EDGE_COLOR
    rectangle_alpha = 0.5
    floor_alpha = 1
    margin_horizontal: int = 1
    margin_vertical: int = 1
    components: List[Component] = []

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def append(self, component: Component):
        self.components.append(component)

    def get_xy_on_floor(self, x: int, y: int):
        return self.margin_horizontal + x, self.margin_vertical + y

    def draw(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set(xlim=(0, self.width + 2 * self.margin_horizontal),
               ylim=(0, self.height + 2 * self.margin_vertical))
        ax.axis('off')

        xy = self.get_xy_on_floor(0, 0)
        rect = Rectangle(xy, self.width, self.height,
                         linewidth=1, edgecolor=self.floor_edge_color,
                         facecolor=self.floor_color,
                         alpha=self.floor_alpha)
        ax.add_patch(rect)

        for component in self.components:
            xy = self.get_xy_on_floor(component.x, component.y)
            width, height = component.rotated_dimensions
            rect = Rectangle(xy, width, height,
                             linewidth=1, edgecolor=(0, 0, 0),
                             facecolor=self.rectangle_color,
                             alpha=self.rectangle_alpha)
            ax.add_patch(rect)
        plt.show()


