from dataclasses import dataclass
from typing import List, Tuple

from ..parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ..parameter.iostar_flight_parameter.iostar_land_parameter import LAND_PARAMETER


@dataclass(frozen=True)
class PositionEventUser:
    frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # ENU and meter


class DroneUser:
    def __init__(
        self,
        drone_index: int,
        position_events_user: List[PositionEventUser],
    ):
        self.drone_index = drone_index
        self.position_events_user = position_events_user

    @property
    def nb_position_events_user(self) -> int:
        return len(self.position_events_user)

    @property
    def flight_positions(self) -> List[PositionEventUser]:
        return self.position_events_user[1:]

    @property
    def last_frame(self) -> int:
        return self.position_events_user[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_events_user[-1].xyz[2]

    def get_frame_by_index(self, index: int) -> int:
        return self.position_events_user[index].frame

    def get_xyz_simulation_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_events_user[index].xyz


class ShowUser:
    def __init__(self, drones_user: List[DroneUser]):
        self.drones_user = drones_user

    def __iter__(self):
        yield from self.drones_user

    def __getitem__(self, drone_user_index: int):
        return self.drones_user[drone_user_index]

    def __len__(self):
        return len(self.drones_user)

    @property
    def nb_drones(self) -> int:
        return len(self.drones_user)

    @property
    def get_last_frame(
        self,
    ) -> int:
        return max(
            [
                drone_user.last_frame
                + int(
                    FRAME_PARAMETER.position_fps
                    * LAND_PARAMETER.get_land_second_delta(drone_user.last_height)
                )
                for drone_user in self.drones_user
            ]
        )
