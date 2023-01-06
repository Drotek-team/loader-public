from typing import List

from ....migration.migration_SU_ST.simulation.flight_simulation import flight_simulation
from ....migration.migration_SU_ST.simulation.position_simulation import SimulationInfo
from ....show_trajectory_collision.show_trajectory_collision import *
from ....show_user.show_user import ShowUser


def get_position_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[CollisionPositionInfo]:
    return [
        CollisionPositionInfo(
            simulation_info.frame, simulation_info.position, simulation_info.in_air
        )
        for simulation_info in simulation_infos
    ]


def SU_to_STC_procedure(
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
