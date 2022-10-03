from dataclasses import dataclass
from typing import List

from ....report import Contenor, Displayer


@dataclass(frozen=True)
class PerformanceInfraction(Displayer):
    drone_index: int
    performance_value: float

    def get_report(self) -> str:
        return f"The drone {self.drone_index} has the value: {self.performance_value}"


class PerformanceCheckReport(Contenor):
    def __init__(self, name: str):
        self.name = name
        self.performance_infractions: List[PerformanceInfraction] = []

    def add_infraction(self, drone_index: int, performance_value: float) -> None:
        self.performance_infractions.append(
            PerformanceInfraction(drone_index, round(performance_value, 2))
        )

    def update(self) -> None:
        self.validation = len(self.performance_infractions) == 0


class PerformanceSliceCheckReport(Contenor):
    def __init__(self, frame: int):
        self.name = f"Performance Slice {frame} check report"
        self.frame = frame
        self.vertical_position_check_report = PerformanceCheckReport(
            "Vertical Position"
        )
        self.horizontal_velocity_check_report = PerformanceCheckReport(
            "Horizontal Velocity"
        )
        self.horizontal_acceleration_check_report = PerformanceCheckReport(
            "Horizontal Acceleration"
        )
        self.up_force_check_report = PerformanceCheckReport("Up Force")
        self.down_force_check_report = PerformanceCheckReport("Down Force")
        self.thrust_check_report = PerformanceCheckReport("Thrust Limitation")

    def update(self) -> None:
        self.validation = (
            self.vertical_position_check_report.validation
            and self.horizontal_velocity_check_report.validation
            and self.horizontal_acceleration_check_report.validation
            and self.up_force_check_report.validation
            and self.down_force_check_report.validation
        )
