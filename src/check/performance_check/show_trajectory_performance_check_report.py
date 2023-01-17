from dataclasses import dataclass

from ...report import *


@dataclass(frozen=True)
class PerformanceInfraction(ErrorMessage):
    name: str
    frame: int
    value: float
    threshold: float
    metric_convention: bool

    @property
    def user_validation(self) -> bool:
        return False

    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        metric_convention_name = "max" if self.metric_convention else "min"
        return (
            f"{indentation_level * indentation_type}The performance {self.name} has the value: {self.value:.2f}"
            f" ({metric_convention_name}: {self.threshold}) at the frame {self.frame}"
        )


class ShowTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, nb_drone: int):
        self.name = "Performance check report"
        self.drones_trajectory_performance_check_report = [
            ErrorMessageList(f"{drone_index}", []) for drone_index in range(nb_drone)
        ]
