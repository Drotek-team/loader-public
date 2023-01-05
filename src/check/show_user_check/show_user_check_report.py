from dataclasses import dataclass
from typing import List

from ...report import Contenor, Displayer


@dataclass(frozen=True)
class IncoherenceRelativeAbsoluteFrame(Displayer):
    relative_frame: int
    absolute_time: float
    event_name: int
    event_ratio: int

    def get_report(self) -> str:
        return f"The relative frame {self.relative_frame} and the absolute frame {self.absolute_time} do not respect the ratio {self.event_ratio} of the event {self.event_name}"


class FrameCoherenceCheckReport(Contenor):
    def __init__(self):
        self.name = "Frame Coherence Check Report"
        self.incoherence_relative_absolute_time: List[IncoherenceRelativeAbsoluteFrame]


class TakeoffDurationCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Duration Check Report"


class TakeoffPositionCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Position Check Report"


class TakeoffCheckReport(Contenor):
    def __init__(self):
        self.name = "Takeoff Check Report"
        self.takeoff_duration_check_report = TakeoffDurationCheckReport()
        self.takeoff_xyz_check_report = TakeoffPositionCheckReport()

    def update(self):
        self.validation = (
            self.takeoff_duration_check_report.validation
            and self.takeoff_xyz_check_report.validation
        )


class DroneUserCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Drone {drone_index} user check report"
        self.frame_coherence_check_report = FrameCoherenceCheckReport()
        self.takeoff_check_report = TakeoffCheckReport()

    def update(self):
        self.validation = (
            self.frame_coherence_check_report.validation
            and self.takeoff_check_report.validation
        )


class ShowUserCheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show user check report"
        self.drones_user_check_report = [
            DroneUserCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = all(
            drone_user_check_report.validation
            for drone_user_check_report in self.drones_user_check_report
        )
