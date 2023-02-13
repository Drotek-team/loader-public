import itertools
from typing import List, Optional

from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.report import BaseReport
from loader.show_env.show_user.show_user import ShowUser

from .collision_math import CollisionInfraction, get_optimized_collision_infractions
from .migration.show_simulation import ShowSimulation, ShowSimulationSlice
from .migration.stc_to_ssc import stc_to_ss
from .migration.su_to_stc import su_to_stc


def get_collision_infractions(
    show_simulation_slice: ShowSimulationSlice,
) -> List[CollisionInfraction]:
    on_ground_collision_infractions = get_optimized_collision_infractions(
        show_simulation_slice.frame,
        show_simulation_slice.on_ground_indices,
        show_simulation_slice.on_ground_positions,
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
        in_air=False,
    )
    in_air_collision_infractions = get_optimized_collision_infractions(
        show_simulation_slice.frame,
        show_simulation_slice.in_air_indices,
        show_simulation_slice.in_air_positions,
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        in_air=True,
    )
    return on_ground_collision_infractions + in_air_collision_infractions


def get_collision_infractions_from_show_simulation(
    show_simulation: ShowSimulation,
) -> List[CollisionInfraction]:
    global_collision_infractions: List[CollisionInfraction] = []
    for show_simulation_slice in show_simulation.show_slices:
        local_collision_infractions = get_collision_infractions(show_simulation_slice)
        if local_collision_infractions:
            global_collision_infractions += local_collision_infractions

    return list(
        itertools.chain.from_iterable(
            [
                get_collision_infractions(show_simulation_slice)
                for show_simulation_slice in show_simulation.show_slices
            ],
        ),
    )


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []


def su_to_ss(show_user: ShowUser) -> ShowSimulation:
    return stc_to_ss(su_to_stc(show_user))


def get_collision_report(
    show_user: ShowUser,
) -> Optional[CollisionReport]:
    collision_infractions = get_collision_infractions_from_show_simulation(
        su_to_ss(show_user),
    )
    if collision_infractions:
        return CollisionReport(collision_infractions=collision_infractions)
    return None