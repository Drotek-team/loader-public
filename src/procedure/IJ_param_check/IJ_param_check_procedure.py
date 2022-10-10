from ...drones_px4.drones_px4 import DronesPx4
from ...parameter.parameter import (
    IostarJsonConfigurationParameter,
    FrameParameter,
)
from ...iostar_json.iostar_json import IostarJson
from .IJ_param_check_report import (
    IostarJsonParameterCheckReport,
)
from .IJ_param_value_check.IJ_param_value_check_procedure import (
    apply_iostar_json_parameter_value_check,
)
from .IJ_param_logic_check.IJ_param_logic_check_procedure import (
    apply_iostar_json_parameter_logic_check_procedure,
)


def apply_iostar_json_parameter_check_procedure(
    drones_px4: DronesPx4,
    iostar_json_parameter: IostarJson,
    frame_parameter: FrameParameter,
    iostar_json_configuration_parameter: IostarJsonConfigurationParameter,
    iostar_json_parameter_check_report: IostarJsonParameterCheckReport,
) -> None:
    apply_iostar_json_parameter_value_check(
        iostar_json_parameter,
        iostar_json_configuration_parameter,
        iostar_json_parameter_check_report.iostar_json_parameter_value_check_report,
    )
    apply_iostar_json_parameter_logic_check_procedure(
        drones_px4,
        iostar_json_parameter,
        frame_parameter,
        iostar_json_parameter_check_report.iostar_json_parameter_logic_check_report,
    )
    iostar_json_parameter_check_report.update()
