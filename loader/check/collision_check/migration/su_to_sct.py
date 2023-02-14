from loader.check.simulation.flight_simulation import get_flight_simulation
from loader.show_env.show_user import ShowUser

from .show_trajectory_collision import CollisionTrajectory, ShowCollisionTrajectory


def su_to_sct(
    show_user: ShowUser,
) -> ShowCollisionTrajectory:
    return ShowCollisionTrajectory(
        [
            CollisionTrajectory(
                drone_user.index,
                get_flight_simulation(
                    drone_user,
                    show_user.last_frame,
                ),
            )
            for drone_user in show_user.drones_user
        ],
    )
