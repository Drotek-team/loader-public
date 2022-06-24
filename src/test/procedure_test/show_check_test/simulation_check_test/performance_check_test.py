import numpy as np
import pytest

from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.performance_check.performance_check_procedure import (
    apply_performance_check_procedure,
)
from .....procedure.show_check.simulation_check.performance_check.performance_check_report import (
    PerformanceCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation


@pytest.fixture
def valid_show_simulation():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    show_simulation = ShowSimulation(
        nb_drones=1,
        nb_slices=3,
        position_time_rate=parameter.timecode_parameter.position_rate,
    )
    show_simulation.add_dance_simulation(
        drone_index=0,
        drone_positions=[np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0])],
        drone_in_air_flags=[1, 1, 1],
        drone_in_dance_flags=[1, 1, 1],
    )
    return show_simulation


def test_valid_simulation(valid_show_simulation: ShowSimulation):
    performance_check_report = PerformanceCheckReport()
    parameter = Parameter()
    parameter.load_iostar_parameter()
    apply_performance_check_procedure(
        valid_show_simulation, performance_check_report, parameter.timecode_parameter
    )
    assert performance_check_report.validation
