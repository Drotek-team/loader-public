from dataclasses import dataclass
from typing import Tuple, List
from ..parameter.parameter import LandParameter, FrameParameter


@dataclass(frozen=True)
class PositionEventSimulation:
    frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # NED/ meter


@dataclass
class DroneSimulation:
    drone_index: int
    position_events_simulation: List[PositionEventSimulation]

    @property
    def flight_positions(self) -> List[PositionEventSimulation]:
        return self.position_events_simulation[1:]

    @property
    def last_frame(self) -> int:
        return self.position_events_simulation[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_events_simulation[-1].xyz[2]

    def get_frame_by_index(self, index: int) -> int:
        return self.position_events_simulation[index].frame

    def get_position_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_events_simulation[index].xyz


def get_last_frame(
    drones_simulation: List[DroneSimulation],
    land_parameter: LandParameter,
    frame_parameter: FrameParameter,
) -> int:
    return max(
        [
            drone_simulation.last_frame
            + int(
                frame_parameter.json_fps
                * land_parameter.get_land_second_delta(drone_simulation.last_height)
            )
            for drone_simulation in drones_simulation
        ]
    )
