from typing import List, Tuple, Dict
import numpy as np
from itertools import product
from dwave_solution.ComponentConverter import ComponentConverter
from dwave_solution.Sampler import Sampler
from planner import Component


class SimpleDWavePlanner:
    height: int
    width: int

    item_height: int
    item_width: int

    components: List[Component] = []

    def __init__(self, height: int, width: int, item_height: int, item_width: int):
        self.height = height
        self.width = width
        self.item_width = item_width
        self.item_height = item_height
        self.memory = np.arange(self.memory_size)
        self.memory_cursor = 0

    @property
    def memory_size(self):
        return 2 * self.height * self.width

    def _get_memory(self, shape):
        size = np.product(shape)

        if self.memory_cursor + size > self.memory_size:
            raise ValueError("Out of memory")

        allocated = self.memory[self.memory_cursor: self.memory_cursor + size].reshape(shape)
        self.memory_cursor += size

        return allocated

    def _get_polynomial(self, S, O):
        poly: Dict[Tuple, int] = {}

        # as many rectangles as possible
        for i, j in product(range(self.width), range(self.height)):
            poly[(S[i, j],)] = -1  # some coefficient

        # as small area as possible
        for i, j in product(range(self.width), range(self.height)):
            poly[(S[i, j],)] += np.sqrt(i * j / (self.height * self.width))

        # avoid overlaps
        # and ((abs(i2 - i1) > 0) or (abs(j2 - j1) > 0))
        for i1, j1 in product(range(self.width), range(self.height)):
            for i2, j2 in product(range(self.width), range(self.height)):
                if (abs(i2 - i1) < self.item_width) and (abs(j2 - j1) < self.item_height) \
                        and ((abs(i2 - i1) > 0) or (abs(j2 - j1) > 0)):
                    poly[(S[i1, j1], S[i2, j2])] = 1

        # avoid getting out of the palette
        for i in range(self.width - self.item_width + 1, self.width):
            for j in range(self.height):
                poly[(S[i, j],)] = 1

        for i in range(self.width):
            for j in range(self.height - self.item_height + 1, self.height):
                poly[(S[i, j],)] = 1

        return poly

    def _post_process_data(self, data, S, O):
        for x in range(O.shape[0]):
            for y in range(O.shape[1]):
                data[O[x, y]] = 0

        return data

    def plan(self):
        S = self._get_memory((self.width, self.height))
        O = self._get_memory((self.width, self.height))

        poly = self._get_polynomial(S, O)

        sampler = Sampler(poly)
        result = sampler.get_results()
        result = self._post_process_data(result, S, O)
        converter = ComponentConverter(self.item_width, self.item_height, S, O)
        self.components = converter.get_components(result)
        print([c.orientation for c in self.components])

    def get_components(self):
        return self.components

