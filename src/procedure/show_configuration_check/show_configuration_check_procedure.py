from ...drones_px4.drones_px4 import DronesPx4
from ...parameter.parameter import (
    IostarJsonConfigurationParameter,
    FrameParameter,
)
from ...iostar_json.show_configuration import ShowConfiguration
from .show_configuration_check_report import (
    IostarJsonParameterCheckReport,
)
from .show_configuration_value_check.show_configuration_value_check_procedure import (
    apply_show_configuration_value_check,
)
from .show_configuration_logic_check.show_configuration_logic_check_procedure import (
    apply_show_configuration_logic_check_procedure,
)


def apply_show_configuration_check_procedure(
    drones_px4: DronesPx4,
    show_configuration: ShowConfiguration,
    frame_parameter: FrameParameter,
    iostar_json_configuration_parameter: IostarJsonConfigurationParameter,
    show_configuration_check_report: IostarJsonParameterCheckReport,
) -> None:
    apply_show_configuration_value_check(
        show_configuration,
        iostar_json_configuration_parameter,
        show_configuration_check_report.show_configuration_value_check_report,
    )
    apply_show_configuration_logic_check_procedure(
        drones_px4,
        show_configuration,
        frame_parameter,
        show_configuration_check_report.show_configuration_logic_check_report,
    )
    show_configuration_check_report.update()
