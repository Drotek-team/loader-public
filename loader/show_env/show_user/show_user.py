import math
from typing import List, Tuple

from pydantic import BaseModel
from pydantic.types import StrictFloat, StrictInt

from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_flight_parameter.iostar_land_parameter import (
    LAND_PARAMETER,
)

from .convex_hull import calculate_convex_hull


class PositionEventUser(BaseModel):
    frame: StrictInt  # 24 fps
    xyz: Tuple[StrictFloat, StrictFloat, StrictFloat]  # ENU and meter

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_frame_to_second(self.frame)

    def apply_horizontal_rotation(self, angle_degree: int) -> None:
        c, s = math.cos(math.radians(angle_degree)), math.sin(
            math.radians(angle_degree),
        )
        self.xyz = (
            c * self.xyz[0] - s * self.xyz[1],
            s * self.xyz[0] + c * self.xyz[1],
            self.xyz[2],
        )


class ColorEventUser(BaseModel):
    frame: StrictInt  # 24 fps
    rgbw: Tuple[StrictFloat, StrictFloat, StrictFloat, StrictFloat]  # between 0 and 1

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_frame_to_second(self.frame)


class FireEventUser(BaseModel):
    frame: StrictInt  # 24 fps
    chanel: StrictInt  # Chanel of the drone between 0 and 2
    duration_frame: StrictInt  # Duration of the event in frame

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_frame_to_second(self.frame)


class DroneUser(BaseModel):
    index: int
    position_events: List[PositionEventUser]
    color_events: List[ColorEventUser]
    fire_events: List[FireEventUser]

    def add_position_event(self, frame: int, xyz: Tuple[float, float, float]) -> None:
        self.position_events.append(PositionEventUser(frame=frame, xyz=xyz))

    def add_color_event(
        self,
        frame: int,
        rgbw: Tuple[float, float, float, float],
    ) -> None:
        self.color_events.append(ColorEventUser(frame=frame, rgbw=rgbw))

    def add_fire_event(
        self,
        frame: int,
        chanel: int,
        duration_frame: int,
    ) -> None:
        self.fire_events.append(
            FireEventUser(frame=frame, chanel=chanel, duration_frame=duration_frame),
        )

    @property
    def flight_positions(self) -> List[PositionEventUser]:
        return self.position_events[1:]

    @property
    def last_frame(self) -> int:
        return self.position_events[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_events[-1].xyz[2]

    def apply_horizontal_rotation(self, angle_degree: int) -> None:
        for position in self.position_events:
            position.apply_horizontal_rotation(angle_degree)

    @property
    def first_horizontal_position(self) -> Tuple[float, float]:
        return (
            self.position_events[0].xyz[0],
            self.position_events[0].xyz[1],
        )


class ShowUser(BaseModel):
    drones_user: List[DroneUser]

    def __getitem__(self, drone_user_index: int) -> DroneUser:
        return self.drones_user[drone_user_index]

    def __len__(self) -> int:
        return len(self.drones_user)

    @property
    def nb_drones(self) -> int:
        return len(self.drones_user)

    @property
    def drones_user_indices(self) -> List[int]:
        return [drone_user.index for drone_user in self.drones_user]

    def update_drones_user_indices(self, indices: List[int]) -> None:
        if len(indices) != len(self.drones_user):
            msg = f"Indices length {len(indices)} != drones_user length {len(self.drones_user)}"
            raise IndexError(msg)
        for drone_user, index in zip(self.drones_user, indices):
            drone_user.index = index

    @property
    def last_frame(
        self,
    ) -> int:
        return max(
            drone_user.last_frame
            + FRAME_PARAMETER.from_second_to_frame(
                LAND_PARAMETER.get_land_second_delta(drone_user.last_height),
            )
            + 1
            for drone_user in self.drones_user
        )

    @property
    def duration(self) -> float:
        return FRAME_PARAMETER.from_frame_to_second(self.last_frame)

    @property
    def convex_hull(self) -> List[Tuple[float, float]]:
        return calculate_convex_hull(
            [drone_user.first_horizontal_position for drone_user in self.drones_user],
        )

    @property
    def altitude_range(self) -> Tuple[float, float]:
        z_positions = [
            position_event.xyz[2]
            for drone in self.drones_user
            for position_event in drone.position_events
        ]
        return (min(z_positions), max(z_positions))

    def apply_horizontal_rotation(self, angle_degree: int) -> None:
        for drone_user in self.drones_user:
            drone_user.apply_horizontal_rotation(angle_degree)
        return
