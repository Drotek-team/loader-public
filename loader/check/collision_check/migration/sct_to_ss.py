from .show_simulation import ShowSimulation
from .show_trajectory_collision import CollisionTrajectory, ShowCollisionTrajectory


def update_show_simulation_from_drone_trajectory(
    show_simulation: ShowSimulation,
    collision_trajectory: CollisionTrajectory,
) -> None:
    for show_slice, collision_position_infos in zip(
        show_simulation.show_slices,
        collision_trajectory.collision_position_infos,
    ):
        show_slice.update_position_air_flag(
            collision_trajectory.drone_index,
            collision_position_infos.position,
            in_air_flag=collision_position_infos.in_air,
        )


def sct_to_ss(
    show_collision_trajectory: ShowCollisionTrajectory,
) -> ShowSimulation:
    show_simulation = ShowSimulation(
        frames=show_collision_trajectory.frames,
        drone_indices=list(range(show_collision_trajectory.drone_number)),
    )
    for collision_trajectory in show_collision_trajectory:
        update_show_simulation_from_drone_trajectory(
            show_simulation,
            collision_trajectory,
        )
    return show_simulation
