import unittest
from . import FloorPlan, Component
from .Component import Orientation


class FloorPlanDrawTest(unittest.TestCase):
    plan: FloorPlan

    def setUp(self) -> None:
        self.plan = FloorPlan(10, 15)
        self.plan.append(Component(height=3, width=5, x=0, y=15))
        self.plan.append(Component(height=3, width=5, x=1, y=7))
        self.plan.append(Component(height=2, width=6, x=7, y=2, orientation=Orientation.Vertical))

    def test_draws_rectangles(self):
        self.plan.draw()


if __name__ == '__main__':
    unittest.main()
