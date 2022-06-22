from dataclasses import dataclass

from .....drones_manager.drones_manager import DronesManager
from .....parameter.parameter import IostarParameter
from .dances_size_check_report import ShowSizeCheckReport

INITIAL_IOSTAR_SIZE_MAX = 50


@dataclass
class EventCount:
    def __init__(self):
        self.initial_dance_size: int = INITIAL_IOSTAR_SIZE_MAX
        self.position_size: int = 0
        self.color_size: int = 0
        self.fire_size: int = 0

    @property
    def total_size(self):
        return (
            self.initial_dance_size
            + self.position_size
            + self.color_size
            + self.fire_size
        )


def apply_dance_size_check_procedure(
    drones_manager: DronesManager,
    iostar_parameter: IostarParameter,
    dances_size_check_report: ShowSizeCheckReport,
) -> None:
    event_counts = [EventCount() for _ in range(len(drones_manager.drones))]
    for drone, event_count in zip(drones_manager.drones, event_counts):
        event_count.position_size = drone.position_events.event_size()
        event_count.color_size = drone.color_events.event_size()
        event_count.fire_size = drone.fire_events.event_size()

    for event_count, dance_size_check_report in zip(
        event_counts, dances_size_check_report.dances_size_check_report
    ):
        dance_size_check_report.update(
            event_count.total_size > iostar_parameter.dance_size_max
        )
