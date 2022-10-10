from .IJ_param_value_check_report import IostarJsonParameterValueCheckReport
from ....parameter.parameter import IostarJsonConfigurationParameter
from ....iostar_json.iostar_json import IostarJson


def apply_iostar_json_parameter_value_check(
    iostar_json_parameter: IostarJson,
    iostar_json_configuration_parameter: IostarJsonConfigurationParameter,
    iostar_json_parameter_value_check_report: IostarJsonParameterValueCheckReport,
) -> None:
    iostar_json_parameter_value_check_report.nb_x_value_check_report.validation = (
        iostar_json_configuration_parameter.nb_x_value_min
        <= iostar_json_parameter.show.nb_x
        and iostar_json_parameter.show.nb_x
        <= iostar_json_configuration_parameter.nb_x_value_max
    )
    iostar_json_parameter_value_check_report.nb_y_value_check_report.validation = (
        iostar_json_configuration_parameter.nb_y_value_min
        <= iostar_json_parameter.show.nb_y
        and iostar_json_parameter.show.nb_y
        <= iostar_json_configuration_parameter.nb_y_value_max
    )
    iostar_json_parameter_value_check_report.step_value_check_report.validation = (
        iostar_json_configuration_parameter.step_takeoff_value_min
        <= iostar_json_parameter.show.step
        and iostar_json_parameter.show.step
        <= iostar_json_configuration_parameter.step_takeoff_value_max
    )
    iostar_json_parameter_value_check_report.takeoff_angle_value_check_report.validation = (
        iostar_json_configuration_parameter.angle_takeoff_value_min
        <= iostar_json_parameter.show.angle_takeoff
        and iostar_json_parameter.show.angle_takeoff
        <= iostar_json_configuration_parameter.angle_takeoff_value_max
    )
    iostar_json_parameter_value_check_report.update()
