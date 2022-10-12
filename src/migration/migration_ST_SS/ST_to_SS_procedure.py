from ...show_simulation.show_simulation import ShowSimulation
from ...show_trajectory.show_trajectory import DroneTrajectory, ShowTrajectory


def update_show_simulation_from_drone_trajectory(
    show_simulation: ShowSimulation,
    drone_trajectory: DroneTrajectory,
) -> None:
    ### TO DO: maybe an enum will do the trick here
    for frame_index in range(len(show_simulation.frames)):
        show_simulation.show_slices[frame_index].positions[
            drone_trajectory.drone_index
        ] = drone_trajectory.drone_positions[frame_index]
        show_simulation.show_slices[frame_index].velocities[
            drone_trajectory.drone_index
        ] = drone_trajectory.drone_velocities[frame_index]
        show_simulation.show_slices[frame_index].accelerations[
            drone_trajectory.drone_index
        ] = drone_trajectory.drone_accelerations[frame_index]
        show_simulation.show_slices[frame_index].in_air_flags[
            drone_trajectory.drone_index
        ] = drone_trajectory.drone_in_air[frame_index]
        show_simulation.show_slices[frame_index].in_dance_flags[
            drone_trajectory.drone_index
        ] = drone_trajectory.drone_in_dance[frame_index]


def ST_to_SS_procedure(
    show_trajectory: ShowTrajectory,
) -> ShowSimulation:
    show_simulation = ShowSimulation(
        frames=show_trajectory.frames,
        nb_drones=show_trajectory.nb_drones,
    )
    for drone_trajectory in show_trajectory.drones_trajectory:
        update_show_simulation_from_drone_trajectory(show_simulation, drone_trajectory)
    return show_simulation
