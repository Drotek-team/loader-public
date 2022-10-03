import os

import pytest

from .collision_check_report import (
    CollisionCheckReport,
)

from ....drones_px4.drones_px4 import DronePx4, DronesPx4
from ....parameter.parameter import Parameter
from .collision_check_procedure import (
    apply_collision_check_procedure,
)
from ..simulation_check_report import (
    SimulationCheckReport,
)
from ....show_simulation.show_simulation import ShowSimulation
from ...migration_DP_SS.DP_to_SS_procedure import DP_to_SS_procedure

from typing import List
from ....drones_px4.drone_px4.events.position_events import PositionEvent
from ...migration_DP_DU.data_convertion_format import XyzConvertionStandard
from ....show_simulation.drone_simulation import (
    DroneSimulation,
    PositionEventSimulation,
)

EPSILON_DELTA = 1e-3


def get_show_simulation(
    drones_simulation: List[DroneSimulation],
) -> ShowSimulation:
    parameter = Parameter()
    xyz_convertion_standard = XyzConvertionStandard()
    parameter.load_parameter(os.getcwd())
    drones_px4 = []
    for drone_index, drone_simulation in enumerate(drones_simulation):
        drone_px4 = DronePx4(drone_index)
        first_position_event = xyz_convertion_standard.from_user_xyz_to_px4_xyz(
            drone_simulation.position_events_simulation[0].xyz
        )
        drone_px4.add_position(0, (first_position_event[0], first_position_event[1], 0))
        drone_px4.add_position(
            int(
                parameter.frame_parameter.json_fps
                * parameter.takeoff_parameter.takeoff_duration_second
            ),
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                (
                    drone_simulation.position_events_simulation[0].xyz[0],
                    drone_simulation.position_events_simulation[0].xyz[1],
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                )
            ),
        )
        for position_event_simulation in drone_simulation.position_events_simulation:
            position_simulation = position_event_simulation.xyz
            drone_px4.add_position(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                )
                + position_event_simulation.frame,
                xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                    (
                        position_simulation[0],
                        position_simulation[1],
                        parameter.takeoff_parameter.takeoff_altitude_meter
                        + position_simulation[2],
                    )
                ),
            )
        drones_px4.append(drone_px4)
    show_simulation = DP_to_SS_procedure(
        DronesPx4(drones_px4),
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )
    return show_simulation


@pytest.fixture
def valid_collision_show():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    drone_1 = DroneSimulation(6, [PositionEventSimulation(6, (0, 0, 0))])
    drone_2 = DroneSimulation(
        6,
        [
            PositionEventSimulation(
                6, (parameter.iostar_parameter.security_distance_in_air, 0, 0)
            )
        ],
    )
    return get_show_simulation([drone_1, drone_2])


def test_valid_simulation(valid_collision_show: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.collision_check_report = CollisionCheckReport(
        valid_collision_show.frames
    )
    apply_collision_check_procedure(
        valid_collision_show,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert simulation_check_report.collision_check_report.validation


@pytest.fixture
def invalid_collision_show():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    drone_1 = DroneSimulation(6, [PositionEventSimulation(6, (0, 0, 0))])
    drone_2 = DroneSimulation(
        6,
        [
            PositionEventSimulation(
                6,
                (
                    parameter.iostar_parameter.security_distance_in_air - EPSILON_DELTA,
                    0,
                    0,
                ),
            )
        ],
    )
    return get_show_simulation([drone_1, drone_2])


def test_invalid_simulation(invalid_collision_show: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.collision_check_report = CollisionCheckReport(
        invalid_collision_show.frames
    )
    apply_collision_check_procedure(
        invalid_collision_show,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert not (simulation_check_report.collision_check_report.validation)
