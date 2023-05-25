from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from loader.schemas.grid_configuration import GridConfiguration, is_angles_equal
from loader.schemas.grid_configuration.grid import Grid
from loader.schemas.show_user import ShowUser


@dataclass()
class ShowConfiguration(GridConfiguration):
    duration: float = 0.0  # Duration of the show in second
    hull: List[Tuple[float, float]] = field(
        default_factory=list,
    )  # List of the relative coordinate (ENU and meter) symbolysing a convex hull of a show
    altitude_range: Tuple[float, float] = (
        0.0,
        0.0,
    )  # Relative coordinate (ENU and meter) symbolising the range of the z-axis

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ShowConfiguration):
            return False
        return (
            self.nb_x == __o.nb_x
            and self.nb_y == __o.nb_y
            and self.nb_drone_per_family == __o.nb_drone_per_family
            and np.allclose(self.step, __o.step, rtol=1e-6)
            and is_angles_equal(self.angle_takeoff, __o.angle_takeoff)
            and self.duration == __o.duration
            and self.hull == __o.hull
            and self.altitude_range == __o.altitude_range
        )

    @classmethod
    def from_show_user(cls, show_user: ShowUser) -> "ShowConfiguration":
        grid = Grid.from_show_user(show_user)
        nb_drone_per_family = grid.get_nb_drone_per_family()
        step = grid.get_step()
        angle_takeoff = show_user.angle_takeoff
        nb_x, nb_y = grid.get_nb_x_nb_y(nb_drone_per_family, angle_takeoff)
        return ShowConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
            step=step,
            angle_takeoff=angle_takeoff,
            duration=show_user.duration,
            hull=show_user.convex_hull,
            altitude_range=show_user.altitude_range,
        )
