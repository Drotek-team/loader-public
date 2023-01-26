from typing import List

from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...report import CollisionInfraction, Contenor
from ...show_env.show_user.show_user import ShowUser
from .collision_math import get_optimized_collision_infractions
from .migration.show_simulation import ShowSimulation, ShowSimulationSlice
from .migration.stc_to_ssc import stc_to_ss
from .migration.test_su_to_stc import su_to_stc


def get_collision_infractions(
    show_simulation_slice: ShowSimulationSlice,
) -> List[CollisionInfraction]:
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
    return on_ground_collision_infractions + in_air_collision_infractions


def get_collision_slice_check_report(
    frame: int, collision_infractions: List[CollisionInfraction]
) -> Contenor:
    collision_slice_contenor = Contenor(
        f"Collision slice check report at frame {frame}"
    )
    for collision_infraction in collision_infractions:
        collision_slice_contenor.add_error_message(collision_infraction)
    return collision_slice_contenor


def su_to_ss(show_user: ShowUser) -> ShowSimulation:
    return stc_to_ss(su_to_stc(show_user))


def apply_show_simulation_collision_check(
    show_user: ShowUser,
) -> Contenor:
    show_simulation_collision_contenor = Contenor("Show simulation collision contenor")
    show_simulation = su_to_ss(show_user)
    for show_simulation_slice in show_simulation.show_slices:
        collision_infractions = get_collision_infractions(show_simulation_slice)
        if collision_infractions:
            show_simulation_collision_contenor.add_error_message(
                get_collision_slice_check_report(
                    show_simulation_slice.frame, collision_infractions
                )
            )
    return show_simulation_collision_contenor
