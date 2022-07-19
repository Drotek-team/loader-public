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
    ### TO DO: Silowski violation => add a new class for that
    # position_events_simulation = PositionEvents()
    # for position_event in position_events:
    #     position_events_simulation.add(
    #         json_convertion_constant.TIMECODE_TO_SECOND_RATIO * position_event.timecode,
    #         json_convertion_constant.from_json_position_to_simulation_position(
    #             position_event.get_values()
    #         ),
    #     )

    show_simulation = ShowSimulation(
        drones_manager.nb_drone,
    )
    show_simulation.update_show_slices(
        drones_manager.last_position_events,
        parameter.timecode_parameter,
        parameter.land_parameter,
    )
    for drone in drones_manager.drones:
        show_simulation.add_dance_simulation(
            drone,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
            parameter.json_convertion_constant,
        )
    apply_simulation_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    show_check_report.update()
