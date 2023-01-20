from .show_simulation import ShowSimulation
from .show_trajectory_collision import CollisionShowTrajectory, CollisionTrajectory


def update_show_simulation_from_drone_trajectory(
    show_simulation: ShowSimulation,
    collision_trajectory: CollisionTrajectory,
) -> None:
    for show_slice, collision_position_infos in zip(
        show_simulation.show_slices, collision_trajectory.collision_position_infos
    ):
        show_slice.positions[
            collision_trajectory.drone_index
        ] = collision_position_infos.position
        show_slice.in_air_flags[
            collision_trajectory.drone_index
        ] = collision_position_infos.in_air


def stc_to_ss_procedure(
    collision_show_trajectory: CollisionShowTrajectory,
) -> ShowSimulation:
    show_simulation = ShowSimulation(
        frames=collision_show_trajectory.frames,
        nb_drones=collision_show_trajectory.drone_number,
    )
    for collision_trajectory in collision_show_trajectory:
        update_show_simulation_from_drone_trajectory(
            show_simulation, collision_trajectory
        )
    return show_simulation
