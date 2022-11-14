from ...show_simulation.show_simulation import ShowSimulation
from ...show_trajectory_collision.show_trajectory_collision import (
    DroneTrajectoryCollision,
    ShowTrajectoryCollision,
)


def update_show_simulation_from_drone_trajectory(
    show_simulation: ShowSimulation,
    drone_trajectory_collision: DroneTrajectoryCollision,
) -> None:
    # raise ValueError(show_simulation.show_slices, drone_trajectory_collision.trajectory)
    for show_slice, trajectory_collision in zip(
        show_simulation.show_slices, drone_trajectory_collision.trajectory
    ):
        show_slice.positions[
            drone_trajectory_collision.drone_index
        ] = trajectory_collision.position
        show_slice.in_air_flags[
            drone_trajectory_collision.drone_index
        ] = trajectory_collision.in_air


def STC_to_SS_procedure(
    show_trajectory_collision: ShowTrajectoryCollision,
) -> ShowSimulation:
    show_simulation = ShowSimulation(
        frames=show_trajectory_collision.frames,
        nb_drones=show_trajectory_collision.nb_drones,
    )
    for (
        drone_trajectory_collision
    ) in show_trajectory_collision.drones_trajectory_collision:
        update_show_simulation_from_drone_trajectory(
            show_simulation, drone_trajectory_collision
        )
    return show_simulation
