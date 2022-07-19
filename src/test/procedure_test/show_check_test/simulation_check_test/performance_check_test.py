from typing import List
from webbrowser import get

from .....drones_manager.drone.events.position_events import PositionEvent
from .....drones_manager.drones_manager import Drone, DronesManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.performance_check.performance_check_procedure import (
    apply_performance_check_procedure,
)
from .....procedure.show_check.simulation_check.performance_check.performance_check_report import (
    PerformanceCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter()
    drone = Drone(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, -parameter.takeoff_parameter.takeoff_altitude),
    )
    for position_event in position_events:
        position = position_event.get_values()
        drone.add_position(
            parameter.takeoff_parameter.takeoff_duration + position_event.timecode,
            (
                position[0],
                position[1],
                -parameter.takeoff_parameter.takeoff_altitude + position[2],
            ),
        )

    drones_manager = DronesManager([drone])
    trajectory_simulation_manager = drones_manager.get_trajectory_simulation_manager(
        parameter.json_convertion_constant
    )
    show_simulation = ShowSimulation(
        len(trajectory_simulation_manager.trajectories_simulation),
        trajectory_simulation_manager.get_last_second(parameter.land_parameter),
    )
    show_simulation.update_show_slices(
        parameter.timecode_parameter,
    )
    for trajectory_simulation in trajectory_simulation_manager.trajectories_simulation:
        show_simulation.add_dance_simulation(
            trajectory_simulation,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    show_simulation.update_slices_implicit_values(parameter.timecode_parameter)
    return show_simulation


def test_valid_simulation():
    position_event_1 = PositionEvent(250, 0, 0, 0)
    position_event_2 = PositionEvent(500, 0, 0, 0)
    position_event_3 = PositionEvent(750, 0, 0, 0)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    performance_check_report = PerformanceCheckReport()
    parameter = Parameter()
    parameter.load_iostar_parameter()
    apply_performance_check_procedure(
        valid_show_simulation,
        performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert performance_check_report.validation


def test_invalid_simulation():
    position_event_1 = PositionEvent(250, 0, 0, -100)
    position_event_2 = PositionEvent(500, 0, 0, -100)
    position_event_3 = PositionEvent(750, 0, 0, -500)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    performance_check_report = PerformanceCheckReport()
    parameter = Parameter()
    parameter.load_iostar_parameter()
    apply_performance_check_procedure(
        valid_show_simulation,
        performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (performance_check_report.validation)


def test_invalid_velocity_simulation():
    position_event_1 = PositionEvent(250, 0, 0, -100)
    position_event_2 = PositionEvent(500, 0, 0, -100)
    position_event_3 = PositionEvent(750, 0, 0, -200)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    performance_check_report = PerformanceCheckReport()
    parameter = Parameter()
    parameter.load_iostar_parameter()
    apply_performance_check_procedure(
        valid_show_simulation,
        performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (performance_check_report.validation)
