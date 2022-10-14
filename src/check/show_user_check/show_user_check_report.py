from dataclasses import dataclass
from ...report import Contenor, Displayer
from typing import List


### TO DO: maybe specify a little more the class, it could be useful in the future
@dataclass(frozen=True)
class IncoherenceRelativeAbsoluteFrame(Displayer):
    relative_frame: int
    absolute_frame: int
    event_name: int
    event_ratio: int

    def get_report(self) -> str:
        return f"The relative frame {self.relative_frame} and the absolute frame {self.absolute_frame} do not respect the ratio {self.event_ratio} of the event {self.event_name}"


class DroneUserCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Drone {drone_index} user check report"
        self.incoherence_relative_absolute_frame: List[IncoherenceRelativeAbsoluteFrame]


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
