from typing import List

from loader.shows.drone_px4 import DronePx4
from loader.shows.iostar_json_gcs.iostar_json_gcs import (
    Dance,
    Family,
    IostarJsonGcs,
    Show,
)
from loader.shows.migration_dp_binary.dp_to_binary import encode_drone
from loader.shows.migration_sp_su.su_to_sp import su_to_sp
from loader.shows.show_user import ShowUser

from .su_to_scg import su_to_scg


def get_family_from_drones_px4(
    autopilot_format_family: List[DronePx4],
) -> Family:
    return Family(
        drones=[
            Dance(
                dance=encode_drone(
                    drone_px4_family,
                ),
            )
            for drone_px4_family in autopilot_format_family
        ],
        x=autopilot_format_family[0].position_events.specific_events[0].xyz[0],
        y=autopilot_format_family[0].position_events.specific_events[0].xyz[1],
        z=autopilot_format_family[0].position_events.specific_events[0].xyz[2],
    )


def su_to_ijg(show_user: ShowUser) -> IostarJsonGcs:
    show_configuration = su_to_scg(show_user)
    autopilot_format = su_to_sp(show_user)
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
