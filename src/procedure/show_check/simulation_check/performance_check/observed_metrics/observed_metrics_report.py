from dataclasses import dataclass
from typing import List

from .....report import Contenor, Displayer


@dataclass(frozen=True)
class PerformanceIncidence(Displayer):
    drone_index: int
    value: float

    def get_report(self) -> str:
        return f"Drone {self.drone_index} exceeds the performance with {self.value}"


class PerformanceCheckReport(Contenor):
    def __init__(self, type: str):
        self.name = f"Performance check report of type {type}"
        self.performance_check_report: List[PerformanceIncidence] = []

    def update(self) -> None:
        self.validation = self.performance_check_report == []

    def add_incident(self, drone_index: int, value: float) -> None:
        self.performance_check_report.append(PerformanceIncidence(drone_index, value))


class ObservedMetricsCheckReport(Contenor):
    def __init__(self, second: float):
        self.name = f"Observed Metrics check report {second} second"
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

    def update(self) -> None:
        self.validation = (
            self.vertical_position_check_report.validation
            and self.horizontal_velocity_check_report.validation
            and self.horizontal_acceleration_check_report.validation
            and self.up_force_check_report.validation
            and self.down_force_check_report.validation
        )
