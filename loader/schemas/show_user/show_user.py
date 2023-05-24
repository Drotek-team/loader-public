import math
from typing import TYPE_CHECKING, List, Tuple

import numpy as np
from pydantic import BaseModel
from pydantic.types import StrictFloat, StrictInt

from loader.parameters import FRAME_PARAMETERS, LAND_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.schemas.drone_px4.drone_px4 import DronePx4
from loader.schemas.grid_configuration.grid_configuration import is_angles_equal

from .convex_hull import calculate_convex_hull

if TYPE_CHECKING:
    from loader.schemas.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs


class EventUserBase(BaseModel):
    frame: StrictInt  # 24 fps

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETERS.from_frame_to_second(self.frame)


class PositionEventUser(EventUserBase):
    xyz: Tuple[StrictFloat, StrictFloat, StrictFloat]  # ENU and meter

    def apply_horizontal_rotation(self, angle_degree: int) -> None:
        c, s = math.cos(math.radians(angle_degree)), math.sin(
            math.radians(angle_degree),
        )
        self.xyz = (
            c * self.xyz[0] - s * self.xyz[1],
            s * self.xyz[0] + c * self.xyz[1],
            self.xyz[2],
        )


class ColorEventUser(EventUserBase):
    rgbw: Tuple[StrictFloat, StrictFloat, StrictFloat, StrictFloat]  # between 0 and 1


class FireEventUser(EventUserBase):
    chanel: StrictInt  # Chanel of the drone between 0 and 2
    duration: StrictInt  # Duration of the event in millisecond


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
        duration: int,
    ) -> None:
        self.fire_events.append(
            FireEventUser(frame=frame, chanel=chanel, duration=duration),
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

    def from_drone_px4(self, drone_px4: DronePx4) -> None:
        for position_event_px4 in drone_px4.position_events.specific_events:
            self.add_position_event(
                frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                    position_event_px4.timecode,
                ),
                xyz=JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(position_event_px4.xyz),
            )

        for color_event_px4 in drone_px4.color_events.specific_events:
            self.add_color_event(
                frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                    color_event_px4.timecode,
                ),
                rgbw=JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(color_event_px4.rgbw),
            )

        for fire_event_px4 in drone_px4.fire_events.specific_events:
            self.add_fire_event(
                frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                    fire_event_px4.timecode,
                ),
                chanel=fire_event_px4.chanel,
                duration=fire_event_px4.duration,
            )


class ShowUser(BaseModel):
    drones_user: List[DroneUser]
    angle_takeoff: float
    step: float

    @classmethod
    def create(cls, *, nb_drones: int, angle_takeoff: float, step: float) -> "ShowUser":
        if nb_drones <= 0:
            msg = f"nb_drones must be positive, not {nb_drones}"
            raise ValueError(msg)
        return ShowUser(
            drones_user=[
                DroneUser(
                    index=drone_index,
                    position_events=[],
                    color_events=[],
                    fire_events=[],
                )
                for drone_index in range(nb_drones)
            ],
            angle_takeoff=angle_takeoff,
            step=step,
        )

    def __getitem__(self, drone_user_index: int) -> DroneUser:
        return self.drones_user[drone_user_index]

    def __len__(self) -> int:
        return len(self.drones_user)

    @property
    def nb_drones(self) -> int:
        return len(self.drones_user)

    def update_drones_user_indices(self, indices: List[int]) -> None:
        if len(indices) != len(self.drones_user):
            msg = f"New indices: {len(indices)} must have the same length as the number of drones: {len(self.drones_user)}"
            raise ValueError(msg)
        if len(set(indices)) != len(indices):
            msg = f"Indices: {indices} are not unique"
            raise ValueError(msg)
        for drone_user, index in zip(self.drones_user, indices):
            drone_user.index = index

    @property
    def last_frame(
        self,
    ) -> int:
        return max(
            drone_user.last_frame
            + FRAME_PARAMETERS.from_second_to_frame(
                LAND_PARAMETERS.get_land_second_delta(drone_user.last_height),
            )
            + 1
            for drone_user in self.drones_user
        )

    @property
    def duration(self) -> float:
        return FRAME_PARAMETERS.from_frame_to_second(self.last_frame)

    @property
    def convex_hull(self) -> List[Tuple[float, float]]:
        return calculate_convex_hull(
            list(
                {
                    position_event.xyz[:2]
                    for drone_user in self.drones_user
                    for position_event in drone_user.position_events
                },
            ),
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
        self.angle_takeoff += np.deg2rad(angle_degree)
        for drone_user in self.drones_user:
            drone_user.apply_horizontal_rotation(angle_degree)

    @classmethod
    def from_autopilot_format(
        cls,
        autopilot_format: List[DronePx4],
        angle_takeoff: float,
        step: float,
    ) -> "ShowUser":
        show_user = ShowUser.create(
            nb_drones=len(autopilot_format),
            angle_takeoff=angle_takeoff,
            step=step,
        )
        for drone_user, drone_px4 in zip(show_user.drones_user, autopilot_format):
            drone_user.from_drone_px4(drone_px4)
        return show_user

    @classmethod
    def from_iostar_json_gcs(cls, iostar_json_gcs: "IostarJsonGcs") -> "ShowUser":
        return ShowUser.from_autopilot_format(
            DronePx4.from_iostar_json_gcs(iostar_json_gcs),
            angle_takeoff=-np.deg2rad(iostar_json_gcs.show.angle_takeoff),
            step=iostar_json_gcs.show.step / 100,
        )

    def __eq__(self, other: object) -> bool:  # noqa: C901, PLR0911
        if not isinstance(other, ShowUser):
            return False

        if not is_angles_equal(self.angle_takeoff, other.angle_takeoff):
            return False

        if not np.allclose(self.step, other.step):
            return False

        if len(self.drones_user) != len(other.drones_user):
            return False

        for drone_user, new_drone_user in zip(self.drones_user, other.drones_user):
            if drone_user.index != new_drone_user.index:
                return False
            if len(drone_user.position_events) != len(new_drone_user.position_events):
                return False
            for position_event, new_position_event in zip(
                drone_user.position_events,
                new_drone_user.position_events,
            ):
                if position_event.frame != new_position_event.frame:
                    return False
                if not np.allclose(position_event.xyz, new_position_event.xyz, atol=1e-2):
                    return False
            if drone_user.color_events != new_drone_user.color_events:
                return False
            if drone_user.fire_events != new_drone_user.fire_events:
                return False
        return True
