from typing import List

from ..iostar_json.iostar_json_gcs import Dance, Family, IostarJsonGcs, Show
from ..migration_dp_binary.drone_encoding_procedure import encode_drone
from ..migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ..show_px4.drone_px4.drone_px4 import DronePx4
from ..show_user.show_user import ShowUser
from .su_to_scg_procedure import su_to_scg_procedure


def get_family_from_drones_px4(
    show_px4_family: List[DronePx4],
) -> Family:
    return Family(
        drones=[
            Dance(
                dance=encode_drone(
                    drone_px4_family,
                )
            )
            for drone_px4_family in show_px4_family
        ],
        x=show_px4_family[0].position_events.specific_events[0].xyz[0],
        y=show_px4_family[0].position_events.specific_events[0].xyz[1],
        z=show_px4_family[0].position_events.specific_events[0].xyz[2],
    )


def su_to_ijg_procedure(show_user: ShowUser) -> IostarJsonGcs:
    show_configuration = su_to_scg_procedure(show_user)
    show_px4 = su_to_sp_procedure(show_user)
    return IostarJsonGcs(
        show=Show(
            families=[
                get_family_from_drones_px4(
                    show_px4[
                        show_configuration.nb_drone_per_family
                        * family_index : show_configuration.nb_drone_per_family
                        * family_index
                        + show_configuration.nb_drone_per_family
                    ],
                )
                for family_index in range(
                    show_configuration.nb_x * show_configuration.nb_y
                )
            ],
            duration=show_configuration.duration,
            hull=show_configuration.hull,
            altitude_range=show_configuration.altitude_range,
            step=show_configuration.step,
            nb_x=show_configuration.nb_x,
            nb_y=show_configuration.nb_y,
            angle_takeoff=show_configuration.angle_takeoff,
        )
    )
