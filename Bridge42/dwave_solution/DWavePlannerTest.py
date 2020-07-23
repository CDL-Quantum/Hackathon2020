import unittest

from planner import FloorPlan
from .DWavePlanner import DWavePlanner


class DWavePlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.planner = DWavePlanner(16, 16, 5, 2)
        self.planner.plan()

    def test_something(self):
        floor_plan = FloorPlan(16, 16)
        for c in self.planner.get_components():
            floor_plan.append(c)

        floor_plan.draw()


if __name__ == '__main__':
    unittest.main()
