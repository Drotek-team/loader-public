from dataclasses import dataclass
from typing import List

from .....report import Contenor, Displayer


@dataclass(frozen=True)
class PerformanceIncidence(Displayer):
    drone_index: int
    value: float

    def get_report(self) -> str:
        return (
            f"Drone {self.drone_index} exceed the performance with value {self.value}"
        )


class PerformanceCheckReport:
    def __init__(self, type: str):
        self.type = type
        self.performance_check_report: List[PerformanceIncidence] = []

    def update(self) -> None:
        self.validation = self.performance_check_report == []

    def add_incident(self, drone_index: int, value: float) -> None:
        self.performance_check_report.append(PerformanceIncidence(drone_index, value))


class ObservedMetricsCheckReport(Contenor):
    def __init__(self, second: float):
        self.second = second
        self.vertical_position_check_report = PerformanceCheckReport(
            "vertical position"
        )
        self.horizontal_velocity_check_report = PerformanceCheckReport(
            "horizontal velocity"
        )
        self.horizontal_acceleration_check_report = PerformanceCheckReport(
            "horizontal acceleration"
        )
        self.up_force_check_report = PerformanceCheckReport("up force")
        self.down_force_check_report = PerformanceCheckReport("down force")

    def update(self) -> None:
        self.validation = (
            self.vertical_position_check_report.validation
            and self.horizontal_velocity_check_report.validation
            and self.horizontal_acceleration_check_report.validation
            and self.up_force_check_report.validation
            and self.down_force_check_report.validation
        )
