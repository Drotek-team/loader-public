import math
from typing import TYPE_CHECKING, List, Tuple

from pydantic import BaseModel
from pydantic.types import StrictFloat, StrictInt

from loader.parameters import FRAME_PARAMETERS, LAND_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.shows.drone_px4.drone_px4 import DronePx4

from .convex_hull import calculate_convex_hull

if TYPE_CHECKING:
    from loader.shows.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs


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


class ShowUser(BaseModel):
    drones_user: List[DroneUser]

    @classmethod
    def create(cls, nb_drones: int) -> "ShowUser":
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
        for drone_user in self.drones_user:
            drone_user.apply_horizontal_rotation(angle_degree)

    @classmethod
    def from_autopilot_format(cls, autopilot_format: List[DronePx4]) -> "ShowUser":
        return ShowUser(
            drones_user=[drone_px4_to_drone_user(drone_px4) for drone_px4 in autopilot_format],
        )

    @classmethod
    def from_iostar_json_gcs(cls, iostar_json_gcs: "IostarJsonGcs") -> "ShowUser":
        return ShowUser.from_autopilot_format(DronePx4.from_iostar_json_gcs(iostar_json_gcs))


def drone_px4_to_drone_user(drone_px4: DronePx4) -> DroneUser:
    position_events_user = [
        PositionEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                position_event_px4.timecode,
            ),
            xyz=JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(position_event_px4.xyz),
        )
        for position_event_px4 in drone_px4.position_events.specific_events
    ]
    color_events_user = [
        ColorEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                color_event_px4.timecode,
            ),
            rgbw=JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(color_event_px4.rgbw),
        )
        for color_event_px4 in drone_px4.color_events.specific_events
    ]

    fire_events_user = [
        FireEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                fire_event_px4.timecode,
            ),
            chanel=fire_event_px4.chanel,
            duration=fire_event_px4.duration,
        )
        for fire_event_px4 in drone_px4.fire_events.specific_events
    ]

    return DroneUser(
        index=drone_px4.index,
        position_events=position_events_user,
        color_events=color_events_user,
        fire_events=fire_events_user,
    )
