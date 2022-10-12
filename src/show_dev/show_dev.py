from dataclasses import dataclass
from typing import Tuple, List
from ..parameter.parameter import LandParameter, FrameParameter


@dataclass(frozen=True)
class PositionEventDev:
    frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # ENU and meter


class DroneDev:
    def __init__(
        self,
        drone_index: int,
        position_events_dev: List[PositionEventDev],
    ):
        self.drone_index = drone_index
        self.position_events_dev = position_events_dev

    @property
    def nb_position_events_dev(self) -> int:
        return len(self.position_events_dev)

    @property
    def flight_positions(self) -> List[PositionEventDev]:
        return self.position_events_dev[1:]

    @property
    def last_frame(self) -> int:
        return self.position_events_dev[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_events_dev[-1].xyz[2]

    def get_frame_by_index(self, index: int) -> int:
        return self.position_events_dev[index].frame

    def get_xyz_simulation_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_events_dev[index].xyz


class ShowDev:
    def __init__(self, drones_dev: List[DroneDev]):
        self.drones_dev = drones_dev

    def __iter__(self):
        for drone_dev in self.drones_dev:
            yield drone_dev

    def __getitem__(self, drone_dev_index: int):
        return self.drones_dev[drone_dev_index]

    def __len__(self):
        return len(self.drones_dev)

    def get_last_frame(
        self,
        land_parameter: LandParameter,
        frame_parameter: FrameParameter,
    ) -> int:
        return max(
            [
                drone_dev.last_frame
                + int(
                    frame_parameter.json_fps
                    * land_parameter.get_land_second_delta(drone_dev.last_height)
                )
                + 1
                for drone_dev in self.drones_dev
            ]
        )
