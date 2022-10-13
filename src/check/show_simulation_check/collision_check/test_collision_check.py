import os

import pytest
from .collision_check_report import (
    CollisionCheckReport,
)
from ....parameter.parameter import Parameter
from .collision_check_procedure import (
    apply_collision_check_procedure,
)
from ..simulation_check_report import (
    SimulationCheckReport,
)
from ....show_simulation.show_simulation import ShowSimulation
from typing import List
from ....show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ....migration.migration_SD_ST.SD_to_STC_procedure import SD_to_STC_procedure
from ....migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure

EPSILON_DELTA = 1e-3
ROUNDING_ERROR = 0.04


@pytest.fixture
def valid_show_simulation() -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    drone_1 = DroneDev(0, [PositionEventDev(6, (0, 0, 0))])
    drone_2 = DroneDev(
        1,
        [
            PositionEventDev(
                6,
                (
                    parameter.iostar_parameter.security_distance_in_air
                    + ROUNDING_ERROR,
                    0,
                    0,
                ),
            )
        ],
    )
    show_dev = ShowDev([drone_1, drone_2])
    return STC_to_SS_procedure(
        SD_to_STC_procedure(
            show_dev,
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )


def test_valid_simulation_in_air(valid_collision_show_in_air: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport(valid_collision_show_in_air.frames)
    simulation_check_report.collision_check_report = CollisionCheckReport(
        valid_collision_show_in_air.frames
    )
    apply_collision_check_procedure(
        valid_collision_show_in_air,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    raise ValueError(len(valid_collision_show_in_air.show_slices))
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        40
    ].validation


# @pytest.fixture
# def valid_collision_show_on_ground():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())

#     drone_1 = DroneDev(6, [PositionEventDev(6, (0, 0, 0))])
#     drone_2 = DroneDev(
#         6,
#         [
#             PositionEventDev(
#                 6,
#                 (
#                     parameter.iostar_parameter.security_distance_on_ground
#                     + ROUNDING_ERROR,
#                     0,
#                     0,
#                 ),
#             )
#         ],
#     )
#     return get_show_simulation([drone_1, drone_2])


# def test_valid_simulation_on_ground(valid_collision_show_on_ground: ShowSimulation):
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     simulation_check_report = SimulationCheckReport()
#     simulation_check_report.collision_check_report = CollisionCheckReport(
#         valid_collision_show_on_ground.frames
#     )
#     apply_collision_check_procedure(
#         valid_collision_show_on_ground,
#         simulation_check_report.collision_check_report,
#         parameter.iostar_parameter,
#     )
#     assert simulation_check_report.collision_check_report.collision_slices_check_report[
#         0
#     ].validation


# @pytest.fixture
# def invalid_collision_show_in_air():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())

#     drone_1 = DroneDev(6, [PositionEventDev(6, (0, 0, 0))])
#     drone_2 = DroneDev(
#         6,
#         [
#             PositionEventDev(
#                 6,
#                 (
#                     parameter.iostar_parameter.security_distance_in_air - EPSILON_DELTA,
#                     0,
#                     0,
#                 ),
#             )
#         ],
#     )
#     return get_show_simulation([drone_1, drone_2])


# def test_invalid_simulation(invalid_collision_show_in_air: ShowSimulation):
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     simulation_check_report = SimulationCheckReport()
#     simulation_check_report.collision_check_report = CollisionCheckReport(
#         invalid_collision_show_in_air.frames
#     )
#     apply_collision_check_procedure(
#         invalid_collision_show_in_air,
#         simulation_check_report.collision_check_report,
#         parameter.iostar_parameter,
#     )
#     assert not (simulation_check_report.collision_check_report.validation)


# @pytest.fixture
# def invalid_collision_show_on_ground():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())

#     drone_1 = DroneDev(6, [PositionEventDev(6, (0, 0, 0))])
#     drone_2 = DroneDev(
#         6,
#         [
#             PositionEventDev(
#                 6,
#                 (
#                     parameter.iostar_parameter.security_distance_on_ground
#                     - EPSILON_DELTA,
#                     0,
#                     0,
#                 ),
#             )
#         ],
#     )
#     return get_show_simulation([drone_1, drone_2])


# def test_invalid_simulation_on_ground(invalid_collision_show_on_ground: ShowSimulation):
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     simulation_check_report = SimulationCheckReport()
#     simulation_check_report.collision_check_report = CollisionCheckReport(
#         invalid_collision_show_on_ground.frames
#     )
#     apply_collision_check_procedure(
#         invalid_collision_show_on_ground,
#         simulation_check_report.collision_check_report,
#         parameter.iostar_parameter,
#     )
#     assert not (
#         simulation_check_report.collision_check_report.collision_slices_check_report[
#             0
#         ].validation
#     )
