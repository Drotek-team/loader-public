from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Tuple

import numpy as np

from loader.schemas.matrix import get_matrix

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from loader.schemas.show_user.show_user import ShowUser


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def is_angles_equal(first_angle_radian: float, second_angle_radian: float) -> bool:
    first_angle, second_angle = np.degrees(first_angle_radian), np.degrees(second_angle_radian)
    return abs((second_angle - first_angle + 180) % 360 - 180) < 1e-6


@dataclass()
class GridConfiguration:
    matrix: "NDArray[np.intp]" = field(default_factory=get_matrix)  # Matrix of the show
    step: float = 1.5  # Distance separating the families during the takeoff in meter
    angle_takeoff: float = 0.0  # Angle of the takeoff grid in radian
    duration: float = 0.0  # Duration of the show in second
    hull: List[Tuple[float, float]] = field(
        default_factory=list,
    )  # List of the relative coordinate (ENU and meter) symbolysing a convex hull of a show
    altitude_range: Tuple[float, float] = (
        0.0,
        0.0,
    )  # Relative coordinate (ENU and meter) symbolising the range of the z-axis

    @property
    def nb_x(self) -> int:
        """Number of families on the x-axis (west/east) during the takeoff."""
        return self.matrix.shape[0]

    @property
    def nb_y(self) -> int:
        """Number of families on the y-axis (south/north) during the takeoff."""
        return self.matrix.shape[1]

    @property
    def nb_drone_per_family(self) -> int:
        """Number of drones in each families."""
        return self.matrix.max()  # pyright: ignore[reportUnknownMemberType]

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GridConfiguration):
            return False
        return (
            np.array_equal(self.matrix, __o.matrix)
            and np.allclose(self.step, __o.step, rtol=1e-6)
            and is_angles_equal(self.angle_takeoff, __o.angle_takeoff)
            and self.duration == __o.duration
            and self.hull == __o.hull
            and self.altitude_range == __o.altitude_range
        )

    @classmethod
    def from_show_user(cls, show_user: "ShowUser") -> "GridConfiguration":
        return GridConfiguration(
            matrix=show_user.matrix,
            step=show_user.step,
            angle_takeoff=show_user.angle_takeoff,
            duration=show_user.duration,
            hull=show_user.convex_hull,
            altitude_range=show_user.altitude_range,
        )
