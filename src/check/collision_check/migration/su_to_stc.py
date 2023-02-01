from ....show_env.show_user.show_user import ShowUser
from ...simulation.flight_simulation import get_flight_simulation
from .show_trajectory_collision import CollisionShowTrajectory, CollisionTrajectory


def su_to_stc(
    show_user: ShowUser,
) -> CollisionShowTrajectory:
    return CollisionShowTrajectory(
        [
            CollisionTrajectory(
                drone_user.index,
                get_flight_simulation(
                    drone_user,
                    show_user.last_frame,
                ),
            )
            for drone_user in show_user.drones_user
        ]
    )
