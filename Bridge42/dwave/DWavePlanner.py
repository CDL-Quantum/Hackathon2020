from collections import defaultdict
from typing import List, Tuple, Dict
import numpy as np
from itertools import product
from dwave.SimpleDWavePlanner import SimpleDWavePlanner


class DWavePlanner(SimpleDWavePlanner):
    def _post_process_data(self, data, S, O):
        return data

    def _get_polynomial(self, S, O):
        poly: Dict[Tuple, int] = defaultdict(int)

        # # as many rectangles as possible
        for i, j in product(range(self.width), range(self.height)):
            poly[(S[i, j],)] += -2  # some coefficient

        # # as small area as possible
        for i, j in product(range(self.width), range(self.height)):
            poly[(S[i, j], )] += np.sqrt(i * j / (self.height * self.width))

        # avoid overlaps
        for i1, j1 in product(range(self.width), range(self.height)):
            for i2, j2 in product(range(self.width), range(self.height)):
                if (abs(i2 - i1) < self.item_width) and (abs(j2 - j1) < self.item_height) \
                        and ((abs(i2 - i1) > 0) or (abs(j2 - j1) > 0)):
                    poly[(S[i1, j1], S[i2, j2], O[i1, j1])] = 1

            for i2, j2 in product(range(self.width), range(self.height)):
                if (abs(j2 - j1) < self.item_width) and (abs(i2 - i1) < self.item_height) \
                        and ((abs(i2 - i1) > 0) or (abs(j2 - j1) > 0)):
                    poly[(S[i1, j1], S[i2, j2], O[i1, j1])] = -1
                    poly[(S[i1, j1], S[i2, j2])] = 1


        # # avoid getting out of the palette
        for i in range(self.width - self.item_width + 1, self.width):
            for j in range(self.height):
                poly[(S[i, j], O[i, j])] += 1

        for i in range(self.width - self.item_height + 1, self.width):
            for j in range(self.height):
                poly[(S[i, j], O[i, j])] += -1
                poly[(S[i, j],)] += 1

        for i in range(self.width):
            for j in range(self.height - self.item_height + 1, self.height):
                poly[(S[i, j], O[i, j])] += 1
        #
        for i in range(self.width):
            for j in range(self.height - self.item_width + 1, self.height):
                poly[(S[i, j], O[i, j])] += -1
                poly[(S[i, j],)] += 1

        return poly

