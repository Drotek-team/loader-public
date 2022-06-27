from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int

@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int
    
@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int
    
@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int

@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int
    
@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int

@dataclass(frozen=True)
class PositionInfraction:
    drone_index:int 


class PerformanceSliceCheckReport:
    def __init__(self, drone_index: int):
        self.validation = False
        self.drone_index = drone_index
        self.position_infraction: List[PositionInfraction] = []

    def update(self):
        self.validation = (
            self.position_infraction == []
        )


class PerformanceCheckReport:
    def __init__(self, timecodes: List[int]):
        self.validation = False
        self.performance_slice_check_report = [
            PerformanceSliceCheckReport(timecode) for timecode in  timecodes
        ]

    def update_drones_performance_check_report(
        self,
        performance_infractions: List[PerformanceInfraction],
    ) -> None:
        for performance_infraction in performance_infractions:
            self.drones_performance_check_report[performance_infraction.drone_index].

    def update(self) -> None:
        self.validation = all(
            drone_performance_check_report.validation
            for drone_performance_check_report in self.drones_performance_check_report
        )
