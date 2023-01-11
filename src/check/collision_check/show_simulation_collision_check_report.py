from typing import List

from report import *


class CollisionSliceCheckReport(Contenor):
    def __init__(self, frame: int, collision_infractions: List[Displayer]):
        self.name = f"Collision slice check report at frame {frame}"
        self.collision_infractions = collision_infractions


class ShowSimulationCollisionCheckReport(Contenor):
    def __init__(self):
        self.name = "Collision check report"
        self.collision_slices_check_report: List[CollisionSliceCheckReport] = []
