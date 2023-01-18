import numpy as np

from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...report import Contenor
from ...show_env.show_user.show_user import ShowUser
from .collision_math import get_optimized_collision_infractions
from .migration.stc_to_ssc_procedure import stc_to_ss_procedure
from .migration.test_su_to_stc_procedure import su_to_stc_procedure


def apply_show_simulation_collision_check_procedure(
    show_user: ShowUser,
) -> Contenor:
    show_simulation_collision_contenor = Contenor("Show simulation collision contenor")
    show_trajectory_collision = su_to_stc_procedure(
        show_user,
    )
    show_simulation = stc_to_ss_procedure(
        show_trajectory_collision,
    )
    drone_indices = np.array(range(show_simulation.nb_drones))
    for show_simulation_slice in show_simulation.show_slices:
        collision_infractions = get_optimized_collision_infractions(
            drone_indices[np.invert(show_simulation_slice.in_air_flags)],
            show_simulation_slice.positions[
                np.invert(show_simulation_slice.in_air_flags)
            ],
            IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
            in_air=False,
        ) + get_optimized_collision_infractions(
            drone_indices[show_simulation_slice.in_air_flags],
            show_simulation_slice.positions[show_simulation_slice.in_air_flags],
            IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
            in_air=True,
        )
        if collision_infractions:
            collision_slice_contenor = Contenor(
                f"Collision slice check report at frame {show_simulation_slice.frame}"
            )
            for collision_infraction in collision_infractions:
                collision_slice_contenor.add_error_message(collision_infraction)
            show_simulation_collision_contenor.add_error_message(
                collision_slice_contenor
            )
    return show_simulation_collision_contenor
