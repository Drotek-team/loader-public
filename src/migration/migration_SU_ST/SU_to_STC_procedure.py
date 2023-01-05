from typing import List

from ...show_trajectory_collision.show_trajectory_collision import (
    DroneTrajectoryCollision,
    ShowTrajectoryCollision,
    TrajectoryCollisionInfo,
)
from ...show_user.show_user import ShowUser
from .simulation.flight_simulation import flight_simulation
from .simulation.position_simulation import SimulationInfo


def get_trajectory_collision_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[TrajectoryCollisionInfo]:
    return [
        TrajectoryCollisionInfo(
            simulation_info.frame, simulation_info.position, simulation_info.in_air
        )
        for simulation_info in simulation_infos
    ]


def SU_to_STC_procedure(
    show_user: ShowUser,
) -> ShowTrajectoryCollision:
    return ShowTrajectoryCollision(
        [
            DroneTrajectoryCollision(
                drone_index,
                get_trajectory_collision_info_from_simulation_infos(
                    flight_simulation(
                        drone_user,
                        show_user.get_last_frame,
                    )
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
