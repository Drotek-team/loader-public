from dataclasses import dataclass
from typing import Tuple, List
from ...parameter.parameter import LandParameter, FrameParameter


@dataclass(frozen=True)
class PositionEventSimulation:
    frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # ENU and meter


class DroneSimulation:
    def __init__(
        self,
        drone_index: int,
        position_events_simulation: List[PositionEventSimulation],
    ):
        self.drone_index = drone_index
        self.position_events_simulation = position_events_simulation

    @property
    def nb_position_events_simulation(self) -> int:
        return len(self.position_events_simulation)

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

    def get_xyz_simulation_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_events_simulation[index].xyz


class DronesSimulation:
    def __init__(self, drones_simulation: List[DroneSimulation]):
        self.drones_simulation = drones_simulation

    def __iter__(self):
        for drone_simulation in self.drones_simulation:
            yield drone_simulation

    def __getitem__(self, drone_simulation_index: int):
        return self.drones_simulation[drone_simulation_index]

    def __len__(self):
        return len(self.drones_simulation)

    def get_last_frame(
        self,
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
                + 1
                for drone_simulation in self.drones_simulation
            ]
        )
