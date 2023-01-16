from typing import List

from ....show_env.show_user.show_user import ShowUser
from ...simulation.flight_simulation import flight_simulation
from ...simulation.position_simulation import SimulationInfo
from .show_trajectory_collision import *


def get_position_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[CollisionPositionInfo]:
    return [
        CollisionPositionInfo(
            simulation_info.frame, simulation_info.position, simulation_info.in_air
        )
        for simulation_info in simulation_infos
    ]


def su_to_stc_procedure(
    show_user: ShowUser,
) -> CollisionShowTrajectory:
    return CollisionShowTrajectory(
        [
            CollisionTrajectory(
                drone_index,
                get_position_info_from_simulation_infos(
                    flight_simulation(
                        drone_user,
                        show_user.get_last_frame,
                    )
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
