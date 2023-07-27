from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Tuple

import numpy as np
from pydantic import BaseModel
from pydantic.types import StrictFloat, StrictInt
from tqdm import tqdm

from loader import __version__
from loader.parameters import (
    FRAME_PARAMETERS,
    IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION,
    LAND_PARAMETERS,
    IostarPhysicParameters,
)
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.schemas.drone_px4.drone_px4 import DronePx4

from .convex_hull import calculate_convex_hull

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from loader.schemas.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs


class EventUserBase(BaseModel):
    frame: StrictInt  # 24 fps

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETERS.from_frame_to_second(self.frame)


class PositionEventUser(EventUserBase):
    xyz: Tuple[StrictFloat, StrictFloat, StrictFloat]  # ENU and meter

    def apply_horizontal_rotation(self, angle: float) -> None:
        c, s = np.cos(angle), np.sin(angle)
        self.xyz = tuple(np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]) @ np.array(self.xyz))


class ColorEventUser(EventUserBase):
    rgbw: Tuple[StrictFloat, StrictFloat, StrictFloat, StrictFloat]  # between 0 and 1


class FireEventUser(EventUserBase):
    channel: StrictInt  # Chanel of the drone between 0 and 2
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
        channel: int,
        duration: int,
    ) -> None:
        self.fire_events.append(
            FireEventUser(frame=frame, channel=channel, duration=duration),
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

    def apply_horizontal_rotation(self, angle: float) -> None:
        for position in self.position_events:
            position.apply_horizontal_rotation(angle)

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
                channel=fire_event_px4.channel,
                duration=fire_event_px4.duration,
            )


class ShowUser(BaseModel):
    drones_user: List[DroneUser]
    angle_takeoff: float  # Angle of the takeoff grid in radian
    step: float  # Distance separating the families during the takeoff in meter
    physic_parameters: IostarPhysicParameters = IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION
    loader_version: str = __version__

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
            step=round(step, 2),
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
        """Duration of the show in second."""
        return FRAME_PARAMETERS.from_frame_to_second(self.last_frame)

    @property
    def convex_hull(self) -> List[Tuple[float, float]]:
        """List of the relative coordinate (ENU and meter) symbolysing a convex hull of a show."""
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
        """Relative coordinate (ENU and meter) symbolising the range of the z-axis."""
        z_positions = [
            position_event.xyz[2]
            for drone in self.drones_user
            for position_event in drone.position_events
        ]
        return (min(z_positions), max(z_positions))

    @property
    def matrix(self) -> "NDArray[np.intp]":
        """Matrix of the show."""
        grid_infos = MatrixInfos.from_show_user(self)
        return grid_infos.matrix

    @property
    def nb_x(self) -> int:
        return self.matrix.shape[1]

    @property
    def nb_y(self) -> int:
        return self.matrix.shape[0]

    @property
    def nb_drones_per_family(self) -> int:
        return self.matrix.max()  # pyright: ignore[reportUnknownMemberType]

    @property
    def drones_user_in_matrix(self) -> List[List[List[DroneUser]]]:
        """Get the drones_user in the matrix."""
        grid_infos = MatrixInfos.from_show_user(self)
        return grid_infos.drones_user_in_matrix

    def apply_horizontal_rotation(self, angle: float) -> None:
        self.angle_takeoff += angle
        for drone_user in tqdm(self.drones_user, desc="Applying horizontal rotation", unit="drone"):
            drone_user.apply_horizontal_rotation(angle)

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
        for drone_user, drone_px4 in tqdm(
            zip(show_user.drones_user, autopilot_format),
            desc="Converting autopilot format to show user",
            total=len(autopilot_format),
            unit="drone",
        ):
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

        if not np.allclose(self.step, other.step, atol=1e-2):
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


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def is_angles_equal(first_angle: float, second_angle: float) -> bool:
    distance = abs((second_angle - first_angle + np.pi) % (2 * np.pi) - np.pi)
    return distance < 1e-2


@dataclass
class MatrixInfos:
    matrix: "NDArray[np.intp]"
    drones_user_in_matrix: List[List[List[DroneUser]]]
    nb_x: int
    nb_y: int
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    @classmethod
    def from_show_user(cls, show_user: ShowUser) -> "MatrixInfos":
        first_position_events = [
            drone_user.position_events[0].model_copy() for drone_user in show_user.drones_user
        ]
        for position_event in first_position_events:
            position_event.apply_horizontal_rotation(-show_user.angle_takeoff)

        x_min = min(position.xyz[0] for position in first_position_events)
        x_max = max(position.xyz[0] for position in first_position_events)
        y_min = min(position.xyz[1] for position in first_position_events)
        y_max = max(position.xyz[1] for position in first_position_events)
        nb_x = int(round((x_max - x_min) / show_user.step) + 1)
        nb_y = int(round((y_max - y_min) / show_user.step) + 1)

        matrix = np.zeros((nb_y, nb_x), dtype=np.intp)
        drones_user_in_matrix: List[List[List[DroneUser]]] = [
            [[] for _ in range(nb_x)] for _ in range(nb_y)
        ]
        for position_event, drone_user in zip(first_position_events, show_user.drones_user):
            x_index = int(round((position_event.xyz[0] - x_min) / show_user.step))
            y_index = int(round((position_event.xyz[1] - y_min) / show_user.step))
            matrix[y_index, x_index] += 1
            drones_user_in_matrix[y_index][x_index].append(drone_user)

        return MatrixInfos(
            matrix=matrix,
            drones_user_in_matrix=drones_user_in_matrix,
            nb_x=nb_x,
            nb_y=nb_y,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
