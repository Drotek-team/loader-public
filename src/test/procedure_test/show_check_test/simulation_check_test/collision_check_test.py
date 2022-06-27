import numpy as np
import pytest

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
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    show_simulation = ShowSimulation(
        nb_drones=2,
        nb_slices=3,
        position_time_rate=parameter.timecode_parameter.position_rate,
    )
    show_simulation.add_dance_simulation(
        drone_index=0,
        drone_positions=[np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0])],
        drone_in_air_flags=[1, 1, 1],
        drone_in_dance_flags=[1, 1, 1],
    )
    show_simulation.add_dance_simulation(
        drone_index=1,
        drone_positions=[
            np.array([parameter.iostar_parameter.security_distance_in_air, 0, 0]),
            np.array([parameter.iostar_parameter.security_distance_in_air, 0, 0]),
            np.array([parameter.iostar_parameter.security_distance_in_air, 0, 0]),
        ],
        drone_in_air_flags=[1, 1, 1],
        drone_in_dance_flags=[1, 1, 1],
    )
    return show_simulation


def test_valid_simulation(valid_show_simulation: ShowSimulation):
    collision_check_report = CollisionCheckReport(valid_show_simulation.nb_drones)
    parameter = Parameter()
    parameter.load_iostar_parameter()
    apply_collision_check_procedure(
        valid_show_simulation, collision_check_report, parameter.iostar_parameter
    )
    assert collision_check_report.validation
