from ...migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure
from ...migration.migration_SU_ST.SU_to_STC_procedure import SU_to_STC_procedure
from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_simulation.show_simulation import ShowSimulation
from ...show_user.show_user import *
from .show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .show_simulation_collision_check_report import ShowSimulationCollisionCheckReport

EPSILON_DELTA = 1e-2
ROUNDING_ERROR = 0.04


def get_show_user(distance_between_drones: float) -> ShowUser:
    first_drone_user = DroneUser(
        position_events=[
            PositionEventUser(position_frame=0, absolute_time=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                absolute_time=TAKEOFF_PARAMETER.takeoff_duration_second,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    second_drone_user = DroneUser(
        position_events=[
            PositionEventUser(
                position_frame=0,
                absolute_time=0,
                xyz=(distance_between_drones, 0.0, 0.0),
            ),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                absolute_time=TAKEOFF_PARAMETER.takeoff_duration_second,
                xyz=(
                    distance_between_drones,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[first_drone_user, second_drone_user])


def test_valid_simulation_on_ground():
    valid_show_user_on_ground = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport()
    apply_show_simulation_collision_check_procedure(
        valid_show_user_on_ground,
        show_simulation_collision_check_report,
    )
    assert (
        len(show_simulation_collision_check_report.collision_slices_check_report) == 50
    )
    assert (
        show_simulation_collision_check_report.collision_slices_check_report[0].name
        == "Collision slice check report at frame 0"
    )


def test_invalid_simulation_on_ground():
    invalid_show_user_on_ground = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground - EPSILON_DELTA
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport()
    apply_show_simulation_collision_check_procedure(
        invalid_show_user_on_ground,
        show_simulation_collision_check_report,
    )
    assert not (
        show_simulation_collision_check_report.collision_slices_check_report[
            0
        ].validation
    )
    assert not (
        show_simulation_collision_check_report.collision_slices_check_report[
            50
        ].validation
    )


def test_valid_simulation_in_air():
    valid_show_user_in_air = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport()
    apply_show_simulation_collision_check_procedure(
        valid_show_user_in_air,
        show_simulation_collision_check_report,
    )
    assert show_simulation_collision_check_report.validation


def test_invalid_simulation_in_air():
    invalid_show_user_in_air = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air - EPSILON_DELTA
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport()
    apply_show_simulation_collision_check_procedure(
        invalid_show_user_in_air,
        show_simulation_collision_check_report,
    )
    assert (
        len(show_simulation_collision_check_report.collision_slices_check_report) == 50
    )
