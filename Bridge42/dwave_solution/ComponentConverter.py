from typing import Dict
from planner import Component
import numpy as np
from planner.Component import Orientation


class ComponentConverter:
    def __init__(self, width, height, coordinates, orientations):
        self.width = width
        self.height = height
        self.coordinates = coordinates
        self.orientations = orientations

    def _get_component(self, x: int, y: int, o: int):
        orientation = Orientation.Horizontal
        if o:
            orientation = Orientation.Vertical
        return Component(width=self.width,
                         height=self.height,
                         x=x, y=y, orientation=orientation)

    def get_components(self, data: Dict):
        components = []
        for x in range(self.coordinates.shape[0]):
            for y in range(self.coordinates.shape[1]):
                if data[self.coordinates[x, y]]:
                    o = data.get(self.orientations[x, y], 0)
                    components.append(self._get_component(x, y, o))

        return components
