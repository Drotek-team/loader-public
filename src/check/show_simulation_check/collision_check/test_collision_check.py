import os
from re import S

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

EPSILON_DELTA = 1e-2
ROUNDING_ERROR = 0.04


@pytest.fixture
def valid_show_simulation_on_ground() -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    first_drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    second_drone_dev = DroneDev(
        1,
        [
            PositionEventDev(
                0, (parameter.iostar_parameter.security_distance_on_ground, 0, 0)
            ),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    parameter.iostar_parameter.security_distance_on_ground,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return STC_to_SS_procedure(
        SD_to_STC_procedure(
            ShowDev([first_drone_dev, second_drone_dev]),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )


def test_valid_simulation_on_ground(valid_show_simulation_on_ground: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport(
        valid_show_simulation_on_ground.frames
    )
    simulation_check_report.collision_check_report = CollisionCheckReport(
        valid_show_simulation_on_ground.frames
    )
    apply_collision_check_procedure(
        valid_show_simulation_on_ground,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        0
    ].validation
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            1
        ].validation
    )
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            51
        ].validation
    )
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        52
    ].validation


@pytest.fixture
def invalid_show_simulation_on_ground() -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    first_drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    second_drone_dev = DroneDev(
        1,
        [
            PositionEventDev(
                0,
                (
                    parameter.iostar_parameter.security_distance_on_ground
                    - EPSILON_DELTA,
                    0,
                    0,
                ),
            ),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    parameter.iostar_parameter.security_distance_on_ground
                    - EPSILON_DELTA,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return STC_to_SS_procedure(
        SD_to_STC_procedure(
            ShowDev([first_drone_dev, second_drone_dev]),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )


def test_invalid_simulation_on_ground(
    invalid_show_simulation_on_ground: ShowSimulation,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport(
        invalid_show_simulation_on_ground.frames
    )
    simulation_check_report.collision_check_report = CollisionCheckReport(
        invalid_show_simulation_on_ground.frames
    )
    apply_collision_check_procedure(
        invalid_show_simulation_on_ground,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            0
        ].validation
    )
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            52
        ].validation
    )


#####################
###### IN AIR #######
#####################


@pytest.fixture
def valid_show_simulation_in_air() -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    first_drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    second_drone_dev = DroneDev(
        1,
        [
            PositionEventDev(
                0, (parameter.iostar_parameter.security_distance_in_air, 0, 0)
            ),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    parameter.iostar_parameter.security_distance_in_air,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return STC_to_SS_procedure(
        SD_to_STC_procedure(
            ShowDev([first_drone_dev, second_drone_dev]),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )


def test_valid_simulation_in_air(valid_show_simulation_in_air: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport(valid_show_simulation_in_air.frames)
    simulation_check_report.collision_check_report = CollisionCheckReport(
        valid_show_simulation_in_air.frames
    )
    apply_collision_check_procedure(
        valid_show_simulation_in_air,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        1
    ].validation
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        51
    ].validation


@pytest.fixture
def invalid_show_simulation_in_air() -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    first_drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    second_drone_dev = DroneDev(
        1,
        [
            PositionEventDev(
                0,
                (
                    parameter.iostar_parameter.security_distance_in_air - EPSILON_DELTA,
                    0,
                    0,
                ),
            ),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    parameter.iostar_parameter.security_distance_in_air - EPSILON_DELTA,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return STC_to_SS_procedure(
        SD_to_STC_procedure(
            ShowDev([first_drone_dev, second_drone_dev]),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )


def test_invalid_simulation_in_air(
    invalid_show_simulation_in_air: ShowSimulation,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport(
        invalid_show_simulation_in_air.frames
    )
    simulation_check_report.collision_check_report = CollisionCheckReport(
        invalid_show_simulation_in_air.frames
    )
    apply_collision_check_procedure(
        invalid_show_simulation_in_air,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        0
    ].validation
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            1
        ].validation
    )
    assert not (
        simulation_check_report.collision_check_report.collision_slices_check_report[
            51
        ].validation
    )
    assert simulation_check_report.collision_check_report.collision_slices_check_report[
        52
    ].validation
