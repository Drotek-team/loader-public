import numpy as np

from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_simulation.show_simulation import ShowSimulation
from .collision_math import get_optimized_collision_infractions
from .show_simulation_collision_check_report import *


def apply_show_simulation_collision_check_procedure(
    show_simulation: ShowSimulation,
    collision_check_report: ShowSimulationCollisionCheckReport,
) -> None:
    drone_indices = np.array(range(show_simulation.nb_drones))
    for show_simulation_slice in show_simulation.show_slices:
        collision_infractions = get_optimized_collision_infractions(
            drone_indices[np.invert(show_simulation_slice.in_air_flags)],
            show_simulation_slice.positions[
                np.invert(show_simulation_slice.in_air_flags)
            ],
            False,
            IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
        ) + get_optimized_collision_infractions(
            drone_indices[show_simulation_slice.in_air_flags],
            show_simulation_slice.positions[show_simulation_slice.in_air_flags],
            True,
            IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        )
        if collision_infractions:
            collision_check_report.collision_slices_check_report.append(
                CollisionSliceCheckReport(
                    show_simulation_slice.frame, collision_infractions
                )
            )
    collision_check_report.update_contenor_validation
