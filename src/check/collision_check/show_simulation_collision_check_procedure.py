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
    for show_simulation_slice in show_simulation.show_slices:
        on_ground_collision_infractions = get_optimized_collision_infractions(
            show_simulation_slice.on_ground_indices,
            show_simulation_slice.on_ground_positions,
            IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
            in_air=False,
        )
        in_air_collision_infractions = get_optimized_collision_infractions(
            show_simulation_slice.in_air_indices,
            show_simulation_slice.in_air_positions,
            IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
            in_air=True,
        )
        collision_infractions = (
            on_ground_collision_infractions + in_air_collision_infractions
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
