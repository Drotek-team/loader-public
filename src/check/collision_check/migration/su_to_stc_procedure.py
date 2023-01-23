from ....show_env.show_user.show_user import ShowUser
from ...simulation.flight_simulation import get_flight_simulation
from .show_trajectory_collision import CollisionShowTrajectory, CollisionTrajectory


def su_to_stc_procedure(
    show_user: ShowUser,
) -> CollisionShowTrajectory:
    return CollisionShowTrajectory(
        [
            CollisionTrajectory(
                drone_index,
                get_flight_simulation(
                    drone_user,
                    show_user.last_frame,
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
