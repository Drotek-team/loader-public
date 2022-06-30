import numpy as np
import pytest

from .....drones_manager.drones_manager import Drone, DronesManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.collision_check.collision_check_procedure import (
    apply_collision_check_procedure,
)
from .....procedure.show_check.simulation_check.collision_check.collision_check_report import (
    CollisionCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation


@pytest.fixture
def valid_show_simulation():
    parameter = Parameter()
    parameter.load_parameter()
    nb_drones = 2
    show_simulation = ShowSimulation(nb_drones, parameter.timecode_parameter)
    first_drone, second_drone = Drone(0), Drone(1)
    first_drone.add_position(0, (0, 0, 0))
    first_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, parameter.takeoff_parameter.takeoff_altitude),
    )
    second_drone.add_position(0, (2, 2, 0))
    second_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (2, 2, parameter.takeoff_parameter.takeoff_altitude),
    )
    drones_manager = DronesManager([first_drone, second_drone])
    show_simulation.update_show_slices(
        drones_manager.last_position_events,
        parameter.land_parameter,
        parameter.json_convention_constant,
    )
    for drone in drones_manager.drones:
        show_simulation.add_dance_simulation(
            drone,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
            parameter.json_convention_constant,
        )
    return show_simulation


def test_valid_simulation(valid_show_simulation: ShowSimulation):
    parameter = Parameter()
    parameter.load_iostar_parameter()
    collision_check_report = CollisionCheckReport()
    apply_collision_check_procedure(
        valid_show_simulation, collision_check_report, parameter.iostar_parameter
    )
    assert collision_check_report.validation


# def test_invalid_simulation(valid_show_simulation: ShowSimulation):
#     parameter = Parameter()
#     parameter.load_iostar_parameter()
#     valid_show_simulation.add_dance_simulation(
#         drone_index=0,
#         drone_positions=[np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0])],
#         drone_in_air_flags=[1, 1, 1],
#         drone_in_dance_flags=[1, 1, 1],
#     )
#     valid_show_simulation.add_dance_simulation(
#         drone_index=1,
#         drone_positions=[
#             np.array(
#                 [0.99 * parameter.iostar_parameter.security_distance_in_air, 0, 0]
#             ),
#             np.array(
#                 [0.99 * parameter.iostar_parameter.security_distance_in_air, 0, 0]
#             ),
#             np.array(
#                 [0.99 * parameter.iostar_parameter.security_distance_in_air, 0, 0]
#             ),
#         ],
#         drone_in_air_flags=[1, 1, 1],
#         drone_in_dance_flags=[1, 1, 1],
#     )
#     collision_check_report = CollisionCheckReport()
#     apply_collision_check_procedure(
#         valid_show_simulation, collision_check_report, parameter.iostar_parameter
#     )
#     assert not (collision_check_report.validation)
