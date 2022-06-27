from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PerformanceIncidence:
    def __init__(self, drone_index: int, value: float):
        self.drone_index = drone_index
        self.value = value


class PerformanceCheckReport:
    def __init__(self, type: str):
        self.validation = True
        self.type = type
        self.performance_check_report: List[PerformanceIncidence] = []

    def update(self) -> None:
        self.validation = self.performance_check_report == []

    def add_incident(self, drone_index: int, value: float) -> None:
        self.performance_check_report.append(PerformanceIncidence(drone_index, value))


class ObservedMetricsSliceCheckReport:
    def __init__(self, timecode: int):
        self.validation = False
        self.timecode = timecode
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
