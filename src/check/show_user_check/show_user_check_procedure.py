from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...report import Contenor, Displayer
from ...show_env.show_user.show_user import DroneUser, ShowUser


def apply_takeoff_check(drone_user: DroneUser) -> Contenor:
    takeoff_check_contenor = Contenor("Takeoff")
    takeoff_duration_displayer = Displayer("Takeoff duration")
    takeoff_xyz_displayer = Displayer("Takeoff xyz")
    takeoff_check_contenor.add_error_message(takeoff_duration_displayer)
    takeoff_check_contenor.add_error_message(takeoff_xyz_displayer)

    if drone_user.nb_position_events == 0:
        return takeoff_check_contenor
    if drone_user.nb_position_events == 1:
        first_frame = drone_user.get_position_frame_by_index(0)
        first_position = drone_user.get_xyz_simulation_by_index(0)
        if first_frame == 0:
            takeoff_duration_displayer.validate()
        if first_position[2] == 0.0:
            takeoff_xyz_displayer.validate()
        return takeoff_check_contenor
    first_time = drone_user.get_absolute_time_by_index(0)
    second_time = drone_user.get_absolute_time_by_index(1)
    first_position = drone_user.get_xyz_simulation_by_index(0)
    second_position = drone_user.get_xyz_simulation_by_index(1)
    if (second_time - first_time) == TAKEOFF_PARAMETER.takeoff_duration_second:
        takeoff_duration_displayer.validate()
    if (
        first_position[0] == second_position[0]
        and first_position[1] == second_position[1]
        and first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min
        <= second_position[2]
        and second_position[2]
        <= first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_max
    ):
        takeoff_xyz_displayer.validate()
    return takeoff_check_contenor


# TODO: test this
def apply_minimal_position_events_number_check(drone_user: DroneUser) -> Displayer:
    minimal_position_events_displayer = Displayer(
        "Minimal position event number: must be only 1 for a only led show or at least 3 for a flight"
    )
    if drone_user.nb_position_events == 1 or drone_user.nb_position_events >= 3:
        minimal_position_events_displayer.validate()
    return minimal_position_events_displayer


def apply_drone_user_check_procedure(
    drone_user: DroneUser,
    drone_index: int,
) -> Contenor:
    drone_user_contenor = Contenor(f"Drone user {drone_index} check procedure")
    drone_user_contenor.add_error_message(
        apply_minimal_position_events_number_check(drone_user)
    )
    drone_user_contenor.add_error_message(apply_takeoff_check(drone_user))
    return drone_user_contenor


def apply_show_user_check_procedure(
    show_user: ShowUser,
) -> Contenor:
    show_user_contenor = Contenor("show user check procedure")
    for drone_index, drone_user in enumerate(show_user.drones_user):
        show_user_contenor.add_error_message(
            apply_drone_user_check_procedure(drone_user, drone_index)
        )
    return show_user_contenor
