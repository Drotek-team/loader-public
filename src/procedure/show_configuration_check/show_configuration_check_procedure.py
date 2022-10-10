from src.show_simulation.drone_simulation import DronesSimulation
from ...parameter.parameter import (
    IostarJsonConfigurationParameter,
    FrameParameter,
)
from ...iostar_json.show_configuration import ShowConfiguration
from .show_configuration_check_report import (
    ShowConfigurationCheckReport,
)
from .show_configuration_value_check.show_configuration_value_check_procedure import (
    apply_show_configuration_value_check,
)
from .show_configuration_logic_check.show_configuration_logic_check_procedure import (
    apply_show_configuration_logic_check_procedure,
)


def apply_show_configuration_check_procedure(
    drones_simulation: DronesSimulation,
    show_configuration: ShowConfiguration,
    frame_parameter: FrameParameter,
    iostar_json_configuration_parameter: IostarJsonConfigurationParameter,
    show_configuration_check_report: ShowConfigurationCheckReport,
) -> None:
    apply_show_configuration_value_check(
        show_configuration,
        iostar_json_configuration_parameter,
        show_configuration_check_report.show_configuration_value_check_report,
    )
    apply_show_configuration_logic_check_procedure(
        drones_simulation,
        show_configuration,
        frame_parameter,
        show_configuration_check_report.show_configuration_logic_check_report,
    )
    show_configuration_check_report.update()
