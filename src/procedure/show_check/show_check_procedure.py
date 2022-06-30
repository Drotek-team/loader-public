from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import Parameter
from ...show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    convert_drone_to_dance_simulation,
)
from ...show_simulation.show_simulation import ShowSimulation
from ..show_check.simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .drone_check.drone_check_procedure import apply_drone_check_procedure
from .family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .show_check_report import ShowCheckReport


def apply_show_check_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    show_check_report: ShowCheckReport,
) -> None:
    parameter = Parameter()
    parameter.load_parameter()
    for drone, drone_check_report in zip(
        drones_manager.drones, show_check_report.drones_check_report
    ):
        apply_drone_check_procedure(drone, drone_check_report, parameter)
    apply_family_check_procedure(
        drones_manager,
        family_manager,
        parameter.family_parameter,
        show_check_report.family_check_report,
    )
    last_position_events = drones_manager.last_position_events
    show_simulation = ShowSimulation(
        drones_manager.nb_drone,
        parameter.timecode_parameter,
    )
    for drone in drones_manager:
        show_simulation.add_dance_simulation(convert_drone_to_dance_simulation(drone))
    apply_simulation_check_procedure(
        show_simulation, show_check_report.simulation_check_report
    )
