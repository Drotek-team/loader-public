from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import Parameter
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
    parameter: Parameter,
) -> None:
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
    apply_simulation_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    show_check_report.update()
