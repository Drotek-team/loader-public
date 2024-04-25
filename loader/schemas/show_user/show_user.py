"""Show user schema.

This module contains the show user schema and its related schemas.
This is the schema to be used to create, modify and check a show.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import numpy as np
from pydantic import BaseModel, Field
from pydantic.types import StrictFloat, StrictInt
from tqdm import tqdm

from loader.parameters import (
    FRAME_PARAMETERS,
    IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION,
    LAND_PARAMETERS,
    IostarPhysicParameters,
)
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, LandType, MagicNumber
from loader.schemas.drone_px4.drone_px4 import DronePx4
from loader.schemas.metadata import Metadata

from .convex_hull import calculate_convex_hull

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from loader.schemas.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs


class EventUserBase(BaseModel):
    """Base event schema."""

    frame: StrictInt
    """Frame of the event (24 FPS)."""

    @property
    def absolute_time(self) -> float:
        """Absolute time of the event in second."""
        return FRAME_PARAMETERS.from_frame_to_second(self.frame)


class PositionEventUser(EventUserBase):
    """Position event schema."""

    xyz: tuple[StrictFloat, StrictFloat, StrictFloat]
    """Position of the drone in meter and ENU coordinate system."""

    def apply_horizontal_rotation(self, angle: float) -> None:
        c, s = np.cos(angle), np.sin(angle)
        self.xyz = cast(
            tuple[float, float, float],
            tuple(np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]) @ np.array(self.xyz)),
        )


class ColorEventUser(EventUserBase):
    """Color event schema."""

    rgbw: tuple[StrictFloat, StrictFloat, StrictFloat, StrictFloat]
    """Color of the drone in RGBW format (between 0 and 1)."""
    interpolate: bool = False
    """If true, linearly interpolate between this color and the next one."""


class FireEventUser(EventUserBase):
    """Fire event schema."""

    channel: StrictInt
    """Fire event channel (0, 1 or 2)."""
    duration: StrictInt
    """Duration of the event in millisecond"""


class YawEventUser(EventUserBase):
    """Yaw event schema."""

    angle: StrictInt
    """Angle of the yaw event in degrees."""

    def apply_horizontal_rotation(self, angle: float) -> None:
        self.angle = round(self.angle + np.rad2deg(angle))


class DroneUser(BaseModel):
    """Drone class to be used by the user."""

    index: int
    """Index of the drone in the show (0, 1, 2, ...)."""
    position_events: list[PositionEventUser]
    """List of the position events of the drone."""
    color_events: list[ColorEventUser]
    """List of the color events of the drone."""
    fire_events: list[FireEventUser]
    """List of the fire events of the drone."""
    yaw_events: list[YawEventUser]
    """List of the yaw events of the drone."""

    def add_position_event(self, frame: int, xyz: tuple[float, float, float]) -> None:
        """Add a position event to the drone."""
        self.position_events.append(PositionEventUser(frame=frame, xyz=xyz))

    def add_color_event(
        self,
        frame: int,
        rgbw: tuple[float, float, float, float],
        *,
        interpolate: bool = False,
    ) -> None:
        """Add a color event to the drone."""
        self.color_events.append(ColorEventUser(frame=frame, rgbw=rgbw, interpolate=interpolate))

    def add_fire_event(self, frame: int, channel: int, duration: int) -> None:
        """Add a fire event to the drone."""
        self.fire_events.append(FireEventUser(frame=frame, channel=channel, duration=duration))

    def add_yaw_event(self, frame: int, angle: int) -> None:
        """Add a yaw event to the drone."""
        self.yaw_events.append(YawEventUser(frame=frame, angle=angle))

    @property
    def flight_positions(self) -> list[PositionEventUser]:
        """List of the position events of the drone during the flight."""
        return self.position_events[1:]

    @property
    def last_frame(self) -> int:
        """Last frame of the drone."""
        return self.position_events[-1].frame

    @property
    def last_height(self) -> float:
        """Last height of the drone in meter."""
        return self.position_events[-1].xyz[2]

    def apply_horizontal_rotation(self, angle: float) -> None:
        """Apply a horizontal rotation to the drone."""
        for position in self.position_events:
            position.apply_horizontal_rotation(angle)
        for yaw_event in self.yaw_events:
            yaw_event.apply_horizontal_rotation(angle)

    def from_drone_px4(self, drone_px4: DronePx4) -> None:
        """Convert from the DronePx4 schema to the DroneUser schema."""
        for position_event_px4 in drone_px4.position_events:
            self.add_position_event(
                frame=position_event_px4.frame,
                xyz=JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(position_event_px4.xyz),
            )

        for color_event_px4 in drone_px4.color_events:
            self.add_color_event(
                frame=color_event_px4.frame,
                rgbw=JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(color_event_px4.rgbw),
                interpolate=color_event_px4.interpolate,
            )

        for fire_event_px4 in drone_px4.fire_events:
            self.add_fire_event(
                frame=fire_event_px4.frame,
                channel=fire_event_px4.channel,
                duration=fire_event_px4.duration,
            )

        for yaw_event_px4 in drone_px4.yaw_events:
            self.add_yaw_event(
                frame=yaw_event_px4.frame,
                angle=yaw_event_px4.angle,
            )


class ShowUser(BaseModel):
    """Show class to be used by the user."""

    drones_user: list[DroneUser]
    """List of the drones of the show."""
    angle_takeoff: float
    """Angle of the takeoff grid in radian."""
    step: float
    """Distance separating the families during the takeoff in meter."""
    scale: int = Field(1, ge=1, le=4)
    """Position scale of the show, multiply the position of the drones by this value."""
    land_type: LandType = LandType.Land
    """Type of landing at the end of the show."""
    magic_number: MagicNumber = MagicNumber.v3
    """Version of the binary format."""
    physic_parameters: IostarPhysicParameters = IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION
    """Physic parameters of the show."""
    metadata: Metadata = Metadata()
    """Metadata of the show."""

    @classmethod
    def create(
        cls,
        *,
        nb_drones: int,
        angle_takeoff: float,
        step: float,
        metadata: Metadata | None = None,
    ) -> "ShowUser":
        """Create a show user.

        Args:
            nb_drones: Number of drones in the show.
            angle_takeoff: Angle of the takeoff grid in radian.
            step: Distance separating the families during the takeoff in meter.
            metadata: Metadata of the show.
        Raises:
            ValueError: If `nb_drones` is invalid.
        """
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
                    yaw_events=[],
                )
                for drone_index in range(nb_drones)
            ],
            angle_takeoff=angle_takeoff,
            step=round(step, 2),
            metadata=metadata or Metadata(),
            scale=1,
        )

    def __getitem__(self, drone_user_index: int) -> DroneUser:
        return self.drones_user[drone_user_index]

    def __len__(self) -> int:
        return len(self.drones_user)

    @property
    def nb_drones(self) -> int:
        """Number of drones in the show."""
        return len(self.drones_user)

    def update_drones_user_indices(self, indices: list[int]) -> None:
        """Update the indices of the drones.

        Args:
            indices: New indices of the drones, in the same order as the drones.
        Raises:
            ValueError: If `indices` is invalid.
        """
        if len(indices) != len(self.drones_user):
            msg = f"New indices: {len(indices)} must have the same length as the number of drones: {len(self.drones_user)}"
            raise ValueError(msg)
        if len(set(indices)) != len(indices):
            msg = f"Indices: {indices} are not unique"
            raise ValueError(msg)
        for drone_user, index in zip(self.drones_user, indices, strict=True):
            drone_user.index = index

    @property
    def last_frame(self) -> int:
        """Last frame of the show."""
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
    def convex_hull(self) -> list[tuple[float, float]]:
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
    def altitude_range(self) -> tuple[float, float]:
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
        """Number of columns of the matrix."""
        return self.matrix.shape[1]

    @property
    def nb_y(self) -> int:
        """Number of rows of the matrix."""
        return self.matrix.shape[0]

    @property
    def nb_drones_per_family(self) -> int:
        """Number of drones per family."""
        return self.matrix.max()

    @property
    def drones_user_in_matrix(self) -> list[list[list[DroneUser]]]:
        """Get the drones_user in the matrix."""
        grid_infos = MatrixInfos.from_show_user(self)
        return grid_infos.drones_user_in_matrix

    def apply_horizontal_rotation(self, angle: float) -> None:
        """Apply a horizontal rotation to the show."""
        self.angle_takeoff += angle
        for drone_user in tqdm(self.drones_user, desc="Applying horizontal rotation", unit="drone"):
            drone_user.apply_horizontal_rotation(angle)

    @classmethod
    def from_autopilot_format(
        cls,
        autopilot_format: list[DronePx4],
        angle_takeoff: float,
        step: float,
        scale: int,
        land_type: LandType,
    ) -> "ShowUser":
        """Convert from the autopilot format schema to the show user schema."""
        show_user = ShowUser.create(
            nb_drones=len(autopilot_format),
            angle_takeoff=angle_takeoff,
            step=step,
        )
        for drone_user, drone_px4 in tqdm(
            zip(show_user.drones_user, autopilot_format, strict=True),
            desc="Converting autopilot format to show user",
            total=len(autopilot_format),
            unit="drone",
        ):
            drone_user.from_drone_px4(drone_px4)

        if not all(drone_px4.scale == scale for drone_px4 in autopilot_format):
            msg = "All the drones must have the same scale"
            raise ValueError(msg)

        if not all(drone_px4.land_type == land_type for drone_px4 in autopilot_format):
            msg = "All the drones must have the same land type"
            raise ValueError(msg)

        show_user.scale = scale
        show_user.land_type = land_type

        return show_user

    @classmethod
    def from_iostar_json_gcs(cls, iostar_json_gcs: "IostarJsonGcs") -> "ShowUser":
        """Convert from the iostar json gcs schema to the show user schema."""
        show_user = ShowUser.from_autopilot_format(
            DronePx4.from_iostar_json_gcs(iostar_json_gcs),
            angle_takeoff=-np.deg2rad(iostar_json_gcs.show.angle_takeoff),
            step=iostar_json_gcs.show.step / 100,
            scale=iostar_json_gcs.show.scale,
            land_type=iostar_json_gcs.show.land_type,
        )
        if iostar_json_gcs.physic_parameters is not None:
            show_user.physic_parameters = iostar_json_gcs.physic_parameters
        return show_user

    def __eq__(self, other: object) -> bool:  # noqa: C901, PLR0911, PLR0912
        if not isinstance(other, ShowUser):
            return False

        if not is_angles_equal(self.angle_takeoff, other.angle_takeoff):
            return False

        if not np.allclose(self.step, other.step, atol=1e-2):
            return False

        if self.scale != other.scale:
            return False

        if self.land_type != other.land_type:
            return False

        if len(self.drones_user) != len(other.drones_user):
            return False

        for drone_user, new_drone_user in zip(self.drones_user, other.drones_user, strict=True):
            if drone_user.index != new_drone_user.index:
                return False
            if len(drone_user.position_events) != len(new_drone_user.position_events):
                return False
            for position_event, new_position_event in zip(
                drone_user.position_events,
                new_drone_user.position_events,
                strict=True,
            ):
                if position_event.frame != new_position_event.frame:
                    return False
                if not np.allclose(
                    position_event.xyz,
                    new_position_event.xyz,
                    atol=1e-2 * self.scale,
                ):
                    return False
            if drone_user.color_events != new_drone_user.color_events:
                return False
            if drone_user.fire_events != new_drone_user.fire_events:
                return False
            if drone_user.yaw_events != new_drone_user.yaw_events:
                return False
        return True


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def is_angles_equal(first_angle: float, second_angle: float) -> bool:
    """Check if two angles are equal."""
    distance = abs((second_angle - first_angle + np.pi) % (2 * np.pi) - np.pi)
    return distance < 1e-2


@dataclass
class MatrixInfos:
    matrix: "NDArray[np.intp]"
    """Matrix containing the number of drones in each family."""
    drones_user_in_matrix: list[list[list[DroneUser]]]
    """Matrix containing the list of drones in each family."""
    nb_x: int
    """Number of columns of the matrix."""
    nb_y: int
    """Number of rows of the matrix."""
    x_min: float
    """Minimum x coordinate of the matrix."""
    x_max: float
    """Maximum x coordinate of the matrix."""
    y_min: float
    """Minimum y coordinate of the matrix."""
    y_max: float
    """Maximum y coordinate of the matrix."""

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
        drones_user_in_matrix: list[list[list[DroneUser]]] = [
            [[] for _ in range(nb_x)] for _ in range(nb_y)
        ]
        for position_event, drone_user in zip(
            first_position_events, show_user.drones_user, strict=True
        ):
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
