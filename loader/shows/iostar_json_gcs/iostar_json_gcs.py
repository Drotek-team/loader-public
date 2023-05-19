from typing import TYPE_CHECKING, List, Tuple

from pydantic import BaseModel

from loader.shows.drone_px4 import DronePx4

from .show_configuration_gcs import ShowConfigurationGcs

if TYPE_CHECKING:
    from loader.shows.show_user import ShowUser


class Dance(BaseModel):
    dance: List[int]  # List of integer symbolising the list of octect


class Family(BaseModel):
    drones: List[Dance]  # List of the drone composing a family
    x: int  # X relative position (NED) of the family in centimeter
    y: int  # Y relative position (NED) of the family in centimeter
    z: int  # Z relative position (NED) of the family in centimeter


class Show(BaseModel):
    families: List[Family]  # List of the families composing the show
    nb_x: int  # Number of families on the x-axis during the takeoff
    nb_y: int  # Number of families on the y-axis during the takeoff
    step: int  # Distance separating the families during the takeoff in centimeter
    angle_takeoff: int  # Angle of the takeoff grid
    duration: int  # Duration of the show in millisecond
    hull: List[
        Tuple[int, int]
    ]  # List of the relative coordinate (XY in NED and centimeter) symbolysing a convex hull of a show
    altitude_range: Tuple[
        int,
        int,
    ]  # Relative coordinate ( z_min and z_max in NED and centimeter) symbolising the range of the z-axis


class IostarJsonGcs(BaseModel):
    show: Show

    @property
    def nb_drones_per_family(self) -> int:
        return len(self.show.families[0].drones)

    @classmethod
    def from_show_user(cls, show_user: "ShowUser") -> "IostarJsonGcs":
        show_configuration = ShowConfigurationGcs.from_show_user(show_user)
        autopilot_format = DronePx4.from_show_user(show_user)
        return IostarJsonGcs(
            show=Show(
                families=[
                    get_family_from_drones_px4(
                        autopilot_format[
                            show_configuration.nb_drone_per_family
                            * family_index : show_configuration.nb_drone_per_family
                            * family_index
                            + show_configuration.nb_drone_per_family
                        ],
                    )
                    for family_index in range(
                        show_configuration.nb_x * show_configuration.nb_y,
                    )
                ],
                duration=show_configuration.duration,
                hull=show_configuration.hull,
                altitude_range=show_configuration.altitude_range,
                step=show_configuration.step,
                nb_x=show_configuration.nb_x,
                nb_y=show_configuration.nb_y,
                angle_takeoff=-show_configuration.angle_takeoff,
            ),
        )


def get_family_from_drones_px4(
    autopilot_format_family: List[DronePx4],
) -> Family:
    return Family(
        drones=[
            Dance(dance=DronePx4.to_binary(drone_px4_family))
            for drone_px4_family in autopilot_format_family
        ],
        x=autopilot_format_family[0].position_events.specific_events[0].xyz[0],
        y=autopilot_format_family[0].position_events.specific_events[0].xyz[1],
        z=autopilot_format_family[0].position_events.specific_events[0].xyz[2],
    )
